#!/usr/bin/env python3
"""Generate an EU AI Act Article 50(2) evidence pack from a list of generating routes.

This is NOT a detector. It cannot tell you whether any particular output carries a
watermark; no public tool can do that today for most upstreams, which is the whole
point. What it produces is the record of diligence: per route, what the upstream
documents, whether a third party can verify it, and where nobody can, a dated note
saying so and what was checked.

Usage:
    python3 genpack.py routes.json > pack.md
    python3 genpack.py routes.json --providers providers.json

Standard library only. No network access: every fact comes from providers.json, and
anything not in there is emitted as `undetermined` with an instruction to go and check.
"""

import argparse
import datetime
import json
import os
import sys

STALE_AFTER_DAYS = 30

# Verdict values, worst first. A route's verdict is the worst finding across its checks.
NOT_RELIABLE = "not reliable"
UNDETERMINED = "undetermined"
RELIABLE = "reliable"
_RANK = {NOT_RELIABLE: 0, UNDETERMINED: 1, RELIABLE: 2}

# Post-processing steps the upstreams themselves name as mark-destroying.
DESTRUCTIVE_STEPS = {
    "translation": "provider names translation as a step that can lose the mark",
    "paraphrase": "provider names paraphrasing as a step that can lose the mark",
    "heavy_edit": "provider names heavy editing as a step that can lose the mark",
    "format_conversion": "provider names format conversion as a step that can lose the mark",
    "re_encode": "re-encoding a media container can drop C2PA manifests",
    "resize": "resizing can disturb an image watermark and drops container metadata",
}


def worst(a, b):
    return a if _RANK[a] <= _RANK[b] else b


def load_json(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def days_since(iso_date, today):
    try:
        d = datetime.date.fromisoformat(iso_date)
    except (TypeError, ValueError):
        return None
    return (today - d).days


def assess(route, prov, today):
    """Return (verdict, findings). Each finding is a plain sentence explaining itself."""
    findings = []
    verdict = RELIABLE

    if prov.get("marking") == "none":
        return NOT_RELIABLE, ["Upstream applies no marking at all. Nothing is inherited; "
                              "the obligation is entirely yours. Not a vendor failure — "
                              "this path was never a reliance candidate."]

    if prov.get("marking_claim") is None:
        verdict = worst(verdict, UNDETERMINED)
        findings.append("No verified marking claim on record for this upstream in this dataset. "
                        "Find the provider's own marking page, record its URL and the date you "
                        "read it, and paste both into this block. A blank is not a pass.")

    # Marking limb: does the claim actually reach this model version?
    cutover = prov.get("cutover_date")
    launched = route.get("model_launch_date")
    if cutover and launched:
        if launched < cutover:
            verdict = worst(verdict, UNDETERMINED)
            findings.append(
                "The pinned model snapshot (%s) pre-dates the provider's marking cutover (%s), "
                "so coverage is NOT established for this version even though the surface is named "
                "as covered." % (launched, cutover))
    elif cutover and not launched:
        verdict = worst(verdict, UNDETERMINED)
        findings.append(
            "This upstream's marking claim only covers models launched on or after %s, and this "
            "route does not record a model launch date. Pin the snapshot and record its date; "
            "until then coverage is undetermined." % cutover)

    if prov.get("resale"):
        verdict = worst(verdict, UNDETERMINED)
        findings.append(
            "This is a resale route. The marking announcement belongs to the model provider; the "
            "surface you call belongs to the reseller, and reseller coverage is not confirmed. "
            "Open a support ticket and record its reference here — an unanswered ticket, dated, "
            "is itself evidence of diligence.")

    # Detection limb: Article 50(2) needs the mark to be verifiable, not merely present.
    det = prov.get("detection_third_party", "undetermined")
    if det == "no":
        verdict = worst(verdict, NOT_RELIABLE)
        findings.append("No detector is available to a third party. You cannot verify the mark "
                        "you would be relying on. This fails the detection limb regardless of how "
                        "good the marking is.")
    elif det == "waitlist":
        verdict = worst(verdict, NOT_RELIABLE)
        findings.append("Detection exists but is gated behind a waitlist, so it is not available "
                        "to you. The mark may well be present and you still cannot rely on it.")
    elif det == "text_only":
        if route.get("modality", "text") != "text":
            verdict = worst(verdict, NOT_RELIABLE)
            findings.append("The published detector covers text only; this route is %s output, "
                            "so no detection path exists for it."
                            % route.get("modality"))
    elif det == "undetermined":
        verdict = worst(verdict, UNDETERMINED)
        findings.append("Whether any third party can detect this upstream's mark is unverified "
                        "in this dataset. Check and record it.")

    # Survival through your own pipeline.
    steps = [s for s in route.get("post_processing", []) if s in DESTRUCTIVE_STEPS]
    if steps:
        verdict = worst(verdict, UNDETERMINED)
        findings.append(
            "Your pipeline applies %s. %s. Whether the mark survives is unknown and, with no "
            "detector, unknowable today." % (
                ", ".join(steps),
                "; ".join(DESTRUCTIVE_STEPS[s] for s in steps)))

    # Route shapes that stay dark even after a detector ships.
    if route.get("deterministic_output"):
        verdict = worst(verdict, NOT_RELIABLE)
        findings.append("This route requires exact/deterministic output. A sampling watermark "
                        "cannot be applied where the output is constrained, so there is likely "
                        "no mark to rely on — and this does not improve when detection ships.")
    if route.get("short_output"):
        verdict = worst(verdict, UNDETERMINED)
        findings.append("This route produces very short outputs. Providers state short passages "
                        "carry no reliable signal. This path stays unverifiable even after a "
                        "detection API arrives.")

    if not findings:
        findings.append("No blocking finding recorded. Re-read the raw provider claim before "
                        "acting on this; a clean result from a small tool is not a legal opinion.")
    return verdict, findings


def caveats_for(prov, modality):
    """Caveats that actually apply to this route's modality.

    A caveat is either a plain string (applies to every route) or an object with a
    `note` and a `modalities` list. Printing a text-watermark caveat under an image
    route was a real defect: it makes the pack look careless to the one reader who
    matters, and a caveat that does not apply is noise an auditor has to discount.
    """
    modality = modality or "text"
    out = []
    for c in prov.get("caveats", []):
        if isinstance(c, dict):
            mods = c.get("modalities")
            if mods and modality not in mods:
                continue
            out.append(c.get("note", ""))
        else:
            out.append(c)
    return [c for c in out if c]


def fmt_route_block(idx, route, prov, verdict, findings, today):
    lines = []
    lines.append("### Path #%d — %s" % (idx, route.get("feature", "unnamed route")))
    lines.append("")
    lines.append("```")
    lines.append("Path:                  #%d — %s" % (idx, route.get("feature", "unnamed")))
    lines.append("Upstream:              %s" % prov.get("display", route.get("upstream")))
    lines.append("Exact model/endpoint:  %s" % route.get("model", "NOT RECORDED — record it"))
    lines.append("Modality:              %s" % route.get("modality", "text"))
    lines.append("Leaves organisation:   %s" % ("yes" if route.get("leaves_org", True) else "no"))
    lines.append("Checked on:            %s" % today.isoformat())

    claim = prov.get("marking_claim")
    lines.append("Provider claim:        %s" % (claim if claim else "none on record — go and find it"))
    if prov.get("source_url"):
        lines.append("Source:                %s" % prov["source_url"])
    if prov.get("source_url_2"):
        lines.append("                       %s" % prov["source_url_2"])
    if prov.get("last_checked"):
        age = days_since(prov["last_checked"], today)
        stale = " (STALE — re-check before relying on it)" if (
            age is not None and age > STALE_AFTER_DAYS) else ""
        lines.append("Claim last verified:   %s%s" % (prov["last_checked"], stale))

    det = prov.get("detection_third_party", "undetermined")
    boxes = []
    for opt in ("yes", "waitlist", "text_only", "no"):
        boxes.append("[%s] %s" % ("x" if det == opt else " ", opt))
    lines.append("Detection available")
    lines.append("to a third party?      %s" % "  ".join(boxes))
    if prov.get("detection_note"):
        lines.append("                       %s" % prov["detection_note"])

    lines.append("Verdict:               [x] %s" % verdict.upper())
    lines.append("```")
    lines.append("")
    for f in findings:
        lines.append("- %s" % f)
    for c in caveats_for(prov, route.get("modality")):
        lines.append("- *Upstream caveat:* %s" % c)
    lines.append("")
    return "\n".join(lines)


def build(routes_doc, providers_doc, today):
    org = routes_doc.get("organisation", {})
    providers = providers_doc["providers"]
    out = []

    out.append("# Article 50(2) evidence pack — %s" % org.get("name", "UNNAMED ORGANISATION"))
    out.append("")
    out.append("Generated %s by `genpack.py`. **This is a record of diligence, not a detection "
               "result.** Nothing here establishes that any output carries a mark; where that "
               "cannot be established, the pack says so and shows what was checked. Not legal "
               "advice." % today.isoformat())
    out.append("")

    # Step 0
    out.append("## Step 0 — Scope determination")
    out.append("")
    out.append("| Question | Answer | Basis |")
    out.append("|---|---|---|")
    out.append("| Provider of an AI system on the EU market under own name? | **%s** | %s |" % (
        "Yes" if org.get("provider_under_own_name", True) else "No",
        org.get("scope_basis", "Reselling model access under your own brand counts.")))
    any_leaves = any(r.get("leaves_org", True) for r in routes_doc.get("routes", []))
    out.append("| Output leaves the organisation? | **%s** | %s |" % (
        "Yes" if any_leaves else "No",
        "At least one route publishes generated content externally." if any_leaves
        else "Check the B2B/industrial carve-out conditions cumulatively."))
    out.append("| Deadline | **%s** | %s |" % (
        org.get("deadline", "NOT RECORDED"),
        org.get("deadline_basis", "Set by when the system was placed on the market.")))
    out.append("")
    out.append("Decided %s against %s. **Expires if the product changes** — a new modality or an "
               "internal-only mode requires re-running this step." % (
                   today.isoformat(), org.get("product_version", "the current product version")))
    out.append("")

    # Step 1
    out.append("## Step 1 — Path inventory")
    out.append("")
    out.append("| # | Feature | Upstream | Exact model / endpoint | Modality | Leaves org? |")
    out.append("|---|---|---|---|---|---|")
    for i, r in enumerate(routes_doc.get("routes", []), 1):
        prov = providers.get(r.get("upstream"), providers["unknown"])
        out.append("| %d | %s | %s | `%s` | %s | %s |" % (
            i, r.get("feature", "unnamed"), prov.get("display", r.get("upstream")),
            r.get("model", "NOT RECORDED"), r.get("modality", "text"),
            "yes" if r.get("leaves_org", True) else "no"))
    out.append("")

    # Step 2
    out.append("## Step 2 — Per-path verification records")
    out.append("")
    verdicts = []
    for i, r in enumerate(routes_doc.get("routes", []), 1):
        key = r.get("upstream")
        prov = providers.get(key, providers["unknown"])
        if key not in providers:
            out.append("> Upstream `%s` is not in the provider dataset; treated as unknown."
                       % key)
            out.append("")
        v, findings = assess(r, prov, today)
        verdicts.append((i, r, v))
        out.append(fmt_route_block(i, r, prov, v, findings, today))

    # Step 3
    out.append("## Step 3 — The decision")
    out.append("")
    out.append("| Path | Decision | Reason | Date |")
    out.append("|---|---|---|---|")
    for i, r, v in verdicts:
        decision = ("**Rely on upstream**" if v == RELIABLE else "**Mark at own boundary**")
        reason = {
            NOT_RELIABLE: "Reliance fails on the record above",
            UNDETERMINED: "Reliance undetermined — treated as not reliable",
            RELIABLE: "Upstream marking and third-party detection both established",
        }[v]
        out.append("| %d | %s | %s | %s |" % (i, decision, reason, today.isoformat()))
    out.append("")
    n_own = sum(1 for _, _, v in verdicts if v != RELIABLE)
    if verdicts and n_own == len(verdicts):
        out.append("**%d paths, %d identical decisions.** That uniformity is itself the finding: "
                   "on today's public record the upstream-reliance route is not practically "
                   "available to this product." % (len(verdicts), n_own))
        out.append("")
    out.append("Owner: %s. Reviewed by external counsel: **%s**." % (
        org.get("owner", "NOT NAMED — name someone"),
        "yes" if org.get("counsel_reviewed") else "no — recorded as a known gap, not glossed"))
    out.append("")

    # Step 4
    out.append("## Step 4 — Re-verification triggers")
    out.append("")
    out.append("Re-verify when any of: a pinned model snapshot moves; **a third-party detection "
               "API ships** (the highest-value trigger — it would reopen the reliance question); "
               "a gated detector leaves its waitlist; the post-processing pipeline changes; an "
               "aggregator or fallback upstream is added; the C2PA spec or `c2patool` updates; "
               "new Commission guidance lands.")
    out.append("")
    out.append("Floor cadence: **quarterly.** Next scheduled: **%s**." % (
        (today + datetime.timedelta(days=90)).isoformat()))
    out.append("")

    # Step 5
    out.append("## Step 5 — Keep the artefacts")
    out.append("")
    out.append("Store output samples for every undetermined path, even though they demonstrate "
               "only that nothing observable is present. When a detector exists, someone can run "
               "it against those stored artefacts and retroactively establish what you could not "
               "establish today. **Storing the artefact is what makes the current dead-end "
               "recoverable later.**")
    out.append("")
    return "\n".join(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Generate an Article 50(2) evidence pack.")
    ap.add_argument("routes", help="JSON file describing your generating routes")
    ap.add_argument("--providers", default=None,
                    help="provider dataset (default: providers.json beside this script)")
    ap.add_argument("--date", default=None, help="override the check date (ISO), for testing")
    args = ap.parse_args(argv)

    providers_path = args.providers or os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "providers.json")
    try:
        routes_doc = load_json(args.routes)
        providers_doc = load_json(providers_path)
    except (OSError, ValueError) as exc:
        sys.stderr.write("could not read input: %s\n" % exc)
        return 2

    if not routes_doc.get("routes"):
        sys.stderr.write("routes file contains no routes; nothing to assess\n")
        return 2

    # An unknown upstream must degrade to the 'unknown' record, never to a blank or a
    # traceback, so the dataset is required to carry that record.
    if "unknown" not in providers_doc.get("providers", {}):
        sys.stderr.write("provider dataset must contain an 'unknown' entry; "
                         "unrecognised upstreams fall back to it\n")
        return 2

    try:
        today = datetime.date.fromisoformat(args.date) if args.date else datetime.date.today()
    except ValueError:
        sys.stderr.write("--date must be an ISO date, e.g. 2026-08-25\n")
        return 2

    sys.stdout.write(build(routes_doc, providers_doc, today) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
