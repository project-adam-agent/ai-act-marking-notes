# Article 50(2) evidence pack — Kestrel Copy SL (fictional example)

Generated 2026-08-25 by `genpack.py`. **This is a record of diligence, not a detection result.** Nothing here establishes that any output carries a mark; where that cannot be established, the pack says so and shows what was checked. Not legal advice.

## Step 0 — Scope determination

| Question | Answer | Basis |
|---|---|---|
| Provider of an AI system on the EU market under own name? | **Yes** | Sells under its own brand; underlying models are third-party. |
| Output leaves the organisation? | **Yes** | At least one route publishes generated content externally. |
| Deadline | **2026-12-02** | On the market since March 2026. |

Decided 2026-08-25 against product version 4.2. **Expires if the product changes** — a new modality or an internal-only mode requires re-running this step.

## Step 1 — Path inventory

| # | Feature | Upstream | Exact model / endpoint | Modality | Leaves org? |
|---|---|---|---|---|---|
| 1 | Copy generator | Anthropic (direct Messages API / Claude / Claude Code) | `claude-sonnet-4-5-20250929` | text | yes |
| 2 | Bulk rewrite | Anthropic via AWS Bedrock (resale route) | `bedrock model ID, same family` | text | yes |
| 3 | Product-image generator | Google Gemini (SynthID) | `Gemini image generation API` | image | yes |
| 4 | Background remover / restyler | Self-hosted open-weight model (FLUX, Llama, Mistral weights, etc.) | `FLUX open weights, self-hosted` | image | yes |
| 5 | Alt-text writer | Anthropic (direct Messages API / Claude / Claude Code) | `claude-haiku-4-5-20251001` | text | yes |

## Step 2 — Per-path verification records

### Path #1 — Copy generator

```
Path:                  #1 — Copy generator
Upstream:              Anthropic (direct Messages API / Claude / Claude Code)
Exact model/endpoint:  claude-sonnet-4-5-20250929
Modality:              text
Leaves organisation:   yes
Checked on:            2026-08-25
Provider claim:        Embedded watermarks apply to all generated text across the Claude Platform (API), Claude, Claude Code, Claude Cowork and Claude Tag, for models launched on or after 2 August 2026. Support for earlier models is 'in progress'. Supported generated files also receive signed C2PA provenance metadata.
Source:                https://support.claude.com/en/articles/16266773-how-claude-marks-ai-generated-content
                       https://www.anthropic.com/news/claude-text-watermark
Claim last verified:   2026-08-25
Detection available
to a third party?      [ ] yes  [ ] waitlist  [ ] text_only  [x] no
                       Detection is stated in the future tense with no date: 'We're also working to enable users and other third parties to detect Claude's embedded watermarks and provenance metadata.' 'We'll share details on detection mechanisms in forthcoming technical documentation.'
Verdict:               [x] NOT RELIABLE
```

- The pinned model snapshot (2025-09-29) pre-dates the provider's marking cutover (2026-08-02), so coverage is NOT established for this version even though the surface is named as covered.
- No detector is available to a third party. You cannot verify the mark you would be relying on. This fails the detection limb regardless of how good the marking is.
- Your pipeline applies heavy_edit, translation. provider names heavy editing as a step that can lose the mark; provider names translation as a step that can lose the mark. Whether the mark survives is unknown and, with no detector, unknowable today.
- *Upstream caveat:* The text mark is a statistical token-sampling watermark. It is not a header or a response field; inspecting the API response tells you nothing.
- *Upstream caveat:* Provider states marks may be lost through heavy editing, paraphrasing, translation or format conversion.
- *Upstream caveat:* Very short passages carry no reliable signal; detection does not work well on small samples.
- *Upstream caveat:* Where an exact output is required (deterministic / constrained decoding), the sampling watermark cannot be applied.

### Path #2 — Bulk rewrite

```
Path:                  #2 — Bulk rewrite
Upstream:              Anthropic via AWS Bedrock (resale route)
Exact model/endpoint:  bedrock model ID, same family
Modality:              text
Leaves organisation:   yes
Checked on:            2026-08-25
Provider claim:        The Anthropic support article states cloud partners AWS, Google Cloud and Microsoft Foundry 'support watermarks where applicable'. 'Where applicable' is not a commitment about a specific resale surface, and no cloud-partner-controlled page was found stating whether marking is applied on this route.
Source:                https://support.claude.com/en/articles/16266773-how-claude-marks-ai-generated-content
Claim last verified:   2026-08-25
Detection available
to a third party?      [ ] yes  [ ] waitlist  [ ] text_only  [x] no
                       Same as the direct route, and one further hop from the issuer.
Verdict:               [x] NOT RELIABLE
```

- This upstream's marking claim only covers models launched on or after 2026-08-02, and this route does not record a model launch date. Pin the snapshot and record its date; until then coverage is undetermined.
- This is a resale route. The marking announcement belongs to the model provider; the surface you call belongs to the reseller, and reseller coverage is not confirmed. Open a support ticket and record its reference here — an unanswered ticket, dated, is itself evidence of diligence.
- No detector is available to a third party. You cannot verify the mark you would be relying on. This fails the detection limb regardless of how good the marking is.
- *Upstream caveat:* Resale routes are the most under-examined rows in most inventories: the announcement you read belongs to the model provider, the surface you call belongs to the cloud partner.
- *Upstream caveat:* Open a support ticket with the cloud partner. An unanswered ticket, dated, is itself evidence of diligence.

### Path #3 — Product-image generator

```
Path:                  #3 — Product-image generator
Upstream:              Google Gemini (SynthID)
Exact model/endpoint:  Gemini image generation API
Modality:              image
Leaves organisation:   yes
Checked on:            2026-08-25
Provider claim:        SynthID is applied to Gemini output per Google documentation. The marking limb is credible here.
Source:                https://deepmind.google/technologies/synthid/
Claim last verified:   2026-08-25
Detection available
to a third party?      [ ] yes  [x] waitlist  [ ] text_only  [ ] no
                       The SynthID Detector portal is not open to the public; access is via waitlist with journalists, media professionals and researchers reviewed first, and no published timeline for general availability. The openly published SynthID implementation is TEXT ONLY, so image marks cannot be checked by a downstream provider. Third parties cannot cryptographically verify the mark; that requires Google's keys.
Verdict:               [x] NOT RELIABLE
```

- Detection exists but is gated behind a waitlist, so it is not available to you. The mark may well be present and you still cannot rely on it.
- Your pipeline applies re_encode, resize. re-encoding a media container can drop C2PA manifests; resizing can disturb an image watermark and drops container metadata. Whether the mark survives is unknown and, with no detector, unknowable today.
- *Upstream caveat:* The image/audio/video mark is a pixel- or sample-domain watermark, not container metadata, so it survives some edits that strip metadata — but the openly published SynthID implementation is text-only, so you have no way to check either way.
- *Upstream caveat:* Answers 'was this generated by a participating model', not 'is this human'.

### Path #4 — Background remover / restyler

```
Path:                  #4 — Background remover / restyler
Upstream:              Self-hosted open-weight model (FLUX, Llama, Mistral weights, etc.)
Exact model/endpoint:  FLUX open weights, self-hosted
Modality:              image
Leaves organisation:   yes
Checked on:            2026-08-25
Provider claim:        None. Open weights inherit nothing. The Article 50(2) obligation is entirely yours.
Claim last verified:   2026-08-25
Detection available
to a third party?      [ ] yes  [ ] waitlist  [ ] text_only  [x] no
                       Not applicable — there is no upstream marking to detect.
Verdict:               [x] NOT RELIABLE
```

- Upstream applies no marking at all. Nothing is inherited; the obligation is entirely yours. Not a vendor failure — this path was never a reliance candidate.
- *Upstream caveat:* This path was never a reliance candidate. Recording it takes two minutes; omitting it leaves a hole in the inventory.

### Path #5 — Alt-text writer

```
Path:                  #5 — Alt-text writer
Upstream:              Anthropic (direct Messages API / Claude / Claude Code)
Exact model/endpoint:  claude-haiku-4-5-20251001
Modality:              text
Leaves organisation:   yes
Checked on:            2026-08-25
Provider claim:        Embedded watermarks apply to all generated text across the Claude Platform (API), Claude, Claude Code, Claude Cowork and Claude Tag, for models launched on or after 2 August 2026. Support for earlier models is 'in progress'. Supported generated files also receive signed C2PA provenance metadata.
Source:                https://support.claude.com/en/articles/16266773-how-claude-marks-ai-generated-content
                       https://www.anthropic.com/news/claude-text-watermark
Claim last verified:   2026-08-25
Detection available
to a third party?      [ ] yes  [ ] waitlist  [ ] text_only  [x] no
                       Detection is stated in the future tense with no date: 'We're also working to enable users and other third parties to detect Claude's embedded watermarks and provenance metadata.' 'We'll share details on detection mechanisms in forthcoming technical documentation.'
Verdict:               [x] NOT RELIABLE
```

- The pinned model snapshot (2025-10-01) pre-dates the provider's marking cutover (2026-08-02), so coverage is NOT established for this version even though the surface is named as covered.
- No detector is available to a third party. You cannot verify the mark you would be relying on. This fails the detection limb regardless of how good the marking is.
- This route produces very short outputs. Providers state short passages carry no reliable signal. This path stays unverifiable even after a detection API arrives.
- *Upstream caveat:* The text mark is a statistical token-sampling watermark. It is not a header or a response field; inspecting the API response tells you nothing.
- *Upstream caveat:* Provider states marks may be lost through heavy editing, paraphrasing, translation or format conversion.
- *Upstream caveat:* Very short passages carry no reliable signal; detection does not work well on small samples.
- *Upstream caveat:* Where an exact output is required (deterministic / constrained decoding), the sampling watermark cannot be applied.

## Step 3 — The decision

| Path | Decision | Reason | Date |
|---|---|---|---|
| 1 | **Mark at own boundary** | Reliance fails on the record above | 2026-08-25 |
| 2 | **Mark at own boundary** | Reliance fails on the record above | 2026-08-25 |
| 3 | **Mark at own boundary** | Reliance fails on the record above | 2026-08-25 |
| 4 | **Mark at own boundary** | Reliance fails on the record above | 2026-08-25 |
| 5 | **Mark at own boundary** | Reliance fails on the record above | 2026-08-25 |

**5 paths, 5 identical decisions.** That uniformity is itself the finding: on today's public record the upstream-reliance route is not practically available to this product.

Owner: Head of Engineering. Reviewed by external counsel: **no — recorded as a known gap, not glossed**.

## Step 4 — Re-verification triggers

Re-verify when any of: a pinned model snapshot moves; **a third-party detection API ships** (the highest-value trigger — it would reopen the reliance question); a gated detector leaves its waitlist; the post-processing pipeline changes; an aggregator or fallback upstream is added; the C2PA spec or `c2patool` updates; new Commission guidance lands.

Floor cadence: **quarterly.** Next scheduled: **2026-11-23**.

## Step 5 — Keep the artefacts

Store output samples for every undetermined path, even though they demonstrate only that nothing observable is present. When a detector exists, someone can run it against those stored artefacts and retroactively establish what you could not establish today. **Storing the artefact is what makes the current dead-end recoverable later.**

