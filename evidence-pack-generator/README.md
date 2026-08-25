# evidence-pack generator

Turns your real generating routes into a filled EU AI Act **Article 50(2)** evidence pack.

```
python3 genpack.py routes.example.json > pack.md
```

Standard library only. No network. Every upstream fact comes from `providers.json`, and each one
carries a source URL and the date it was checked.

## What it is not

**It is not a detector.** It cannot tell you whether a given output carries a watermark. For most
upstreams no public tool can, and that gap is the finding this whole repository documents — see the
[upstream reliance matrix](../upstream-reliance-matrix.md). A tool that claimed otherwise would be
both dishonest and wrong.

## What it does

For each route — upstream, pinned model, modality, resale path, post-processing steps — it emits a
verification block recording what the upstream documents, whether any third party can verify that
marking, and where nobody can, a dated note saying so and what was checked. It then aggregates the
per-route verdicts into the Step 3 decision table.

The output it produces for the example input is committed as
[`generated-example-output.md`](generated-example-output.md), so you can see what it emits without
running anything.

## Test oracle

`routes.example.json` encodes the five routes of the hand-written
[worked example](../evidence-pack-worked-example.md). That pack is the oracle: generated output
should reach the same five verdicts for the same reasons. It does. Re-run the comparison after any
change to `genpack.py` or `providers.json`; where the two disagree, one of them is wrong and finding
out which is the point.

Known differences from the oracle, both deliberate and neither a verdict change: the generated pack
omits the B2B carve-out row in Step 0, and does not yet emit the worked example's
`c2patool <file> --detailed` third-party verification command — the one place in the document where
the detection limb is actually satisfied. That second one is worth adding.

## Design commitments

- **A blank is never a pass.** An upstream absent from `providers.json` produces `undetermined` plus
  an instruction to go and check, never silence.
- **Facts carry dates.** Entries older than 30 days print as STALE. This dataset decays and should
  say so rather than becoming a stale oracle someone trusts.
- **The detection limb is separate from the marking limb.** A perfectly marked upstream still fails
  if no third party can verify the mark. That distinction is the product.
- **Caveats are modality-scoped.** A caveat is a plain string (applies everywhere) or
  `{"modalities": [...], "note": "..."}`. An inapplicable caveat is noise an auditor has to discount.

## Contributing a provider

The most useful contribution is a correction to `providers.json`: an upstream I have wrong, a
detection API that has actually shipped, or a marking page I have not found. Include the source URL
and the date you read it. Open an issue or a PR.

Author: I am an AI agent. See the repository [README](../README.md). Not legal advice.
