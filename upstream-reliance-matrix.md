# Upstream reliance matrix

**Question this answers:** an EU company builds a product on somebody else's generative model. Under
EU AI Act Article 50(2) it is the provider of its own system. It *may* rely on the upstream model's
marking — but per the Commission's final Guidelines (20 July 2026) reliance is permitted and
responsibility is not transferable: it must verify the inherited solution is effective,
interoperable, robust and reliable, and be able to demonstrate that it did. Article 50(2) separately
requires that a **corresponding means of detection is available**.

So: *for each realistic upstream choice, can a downstream provider rely on it, and can they prove
it?*

Deadline for systems already on the market: **2 December 2026**.

Source rule for this page: **the provider's own documentation only.** Third-party comparison tables
contradicted each other during an earlier survey and contradicted each other again while building
this page — two
searches returned confident and mutually incompatible claims about Runway. Where I could not reach a
provider-controlled page, the verdict is `undetermined`, not a guess.

Scope: this describes upstream providers' *published capabilities*. It does not assess any
downstream company's compliance status.

Evidence gathered 2026-08-23. Verdicts: `relyable` / `partial` / `not-relyable` / `undetermined`.

---

## The matrix

### 1. OpenAI — image API (`gpt-image-*`)
- **Marking:** OpenAI maintains a help-center article titled *"Provenance signals (Content
  Credentials, SynthID) in OpenAI-generated content"*
  (`help.openai.com/en/articles/8912793-...`), so both C2PA and SynthID are claimed somewhere in the
  product line.
- **API path:** the developer image-generation guide
  (<https://developers.openai.com/api/docs/guides/image-generation>) contains **no mention** of
  C2PA, content credentials, provenance, metadata or watermarking. Verified by fetch.
- **Detection:** if C2PA is present, open validators exist (c2patool, Content Credentials Verify) —
  detection limb satisfiable and locally executable.
- **Verdict: `partial`.** The consumer claim exists; the *API-path* claim is not in the developer
  documentation, which is where a downstream provider's compliance file would have to point.
- *Evidence limitation:* the help-center article returned HTTP 403 to my sandbox on two attempts. I
  have its title from search indexing, not its text.

### 2. OpenAI — Sora / video
- **Marking:** not established from a provider page in this pass.
- **Verdict: `undetermined`.**

### 3. Google — Gemini API image generation
- **Marking:** documented and unambiguous. <https://ai.google.dev/gemini-api/docs/image-generation>:
  *"All generated images include a SynthID watermark."*
- **Detection:** <https://deepmind.google/science/synthid/> — the SynthID Detector portal has
  limited access: *"We are currently collaborating with journalists and media professionals to test
  the portal and collect their feedback,"* with a *"Join the early tester waitlist"* form. The
  developer safeguards page (`ai.google.dev/responsible/docs/safeguards/synthid`) documents an
  open detector **for text only**: *"A Bayesian detector is provided with Hugging Face Transformers
  and on GitHub."* No public image/audio/video detector.
- **Verdict: `not-relyable` on the detection limb.** The marking is the best-documented in this
  table and the detection requirement is the one it cannot meet. A downstream provider relying
  solely on inherited SynthID for images has no third-party-available means of detection to point
  at. This is the sharpest finding on this page.

### 4. Google — Vertex AI Imagen
- **Marking:** the Vertex responsible-AI page for Imagen says *"We've applied metadata labeling to
  AI-generated images to help combat the risk of misinformation"* — **metadata labeling, not
  SynthID**, and it does not say whether the API path is covered or whether it is default-on.
- **Verdict: `undetermined`.** Note the divergence from entry 3: the same vendor documents two
  different things on two surfaces.

### 5. Google — Veo
- **Verdict: `undetermined`.** Not stated on the Vertex page fetched; no dedicated provider page
  reached this pass.

### 6. ElevenLabs — text-to-speech
- **Marking:** <https://elevenlabs.io/blog/synthid> — SynthID audio, *"started including SynthID in
  Text to Speech generations by free users"*, expanding *"to all ElevenLabs audio generations over
  the coming weeks."* The help-center watermarking page does not state API vs app scope.
- **Detection:** a *"free ElevenLabs Audio Detector webpage"*, public. This is the one non-C2PA case
  in the table where the detection limb is plausibly met.
- **Verdict: `partial`.** Detection exists but is **provider-hosted, not locally executable** — the
  Guidelines express a preference for local execution — and API coverage is a rollout statement with
  no completion date, which is exactly the kind of claim that has to be re-verified rather than
  cited once.

### 7. Black Forest Labs — FLUX API
- **Marking:** the FLUX.2 model cards on Hugging Face (provider-controlled surface) state the API
  applies cryptographically-signed C2PA metadata to downloaded output. BFL's knowledge base lists an
  article *"C2PA and Content Credentials in FLUX outputs."*
- **API path:** claimed for the API specifically — the strongest API-path claim found here.
- **Detection:** C2PA, open validators.
- **Verdict: `partial`.** Would be `relyable` on a retrievable canonical page; the knowledge-base
  article URL returned 404 to my sandbox and `docs.bfl.ai` index has no mention.

### 8. FLUX open weights (`FLUX.2-dev`, `klein`), self-hosted
- **Marking:** none inherited. The inference repo ships an *example* of pixel-layer watermarking.
- **Verdict: `not-relyable` — and correctly so.** Self-hosting makes the downstream company the
  marker. There is nothing upstream to rely on; the obligation lands entirely on them.

### 9. Stable Diffusion / other open weights, self-hosted
- **Verdict: `not-relyable`,** same reason as 8.

### 10. Stability AI — hosted platform API
- **Marking:** widely asserted by third parties to be C2PA-by-default. **No provider page confirming
  it was retrieved**; the API reference page returned only a title to my fetcher.
- **Verdict: `undetermined`.** Included deliberately as an example of a claim everyone repeats and
  nobody can cite from source.

### 11. Midjourney
- **Marking:** no C2PA per consistent third-party reporting; EXIF/IPTC fields including
  `DigitalSourceType: trainedAlgorithmicMedia`. **Unsigned**, therefore strippable with ExifTool.
- **Verdict: `not-relyable`.** Unsigned metadata does not meet "robust and reliable" on any reading,
  and there is no general API to build a product on regardless.

### 12. Adobe Firefly — web app
- **Marking:** <https://helpx.adobe.com/firefly/web/get-started/learn-the-basics/content-credentials-overview.html>
  — Content Credentials applied automatically where 100% of pixels are Firefly-generated, with a
  durable cloud copy recoverable via the public Inspect tool.
- **Detection:** C2PA plus Adobe's public Inspect tool.
- **Verdict: `relyable`** for the web app — the only `relyable` on this page.
- *Evidence limitation:* Adobe's page timed out on two fetch attempts; the wording above comes from
  the search engine's index of that Adobe URL, not from my own retrieval of it. Downgrade to
  `undetermined` if direct retrieval contradicts it.

### 13. Adobe Firefly Services — API
- **Marking:** the Firefly Services developer docs cover auth and generation parameters; Content
  Credentials handling on the API path is not stated there.
- **Verdict: `undetermined`.** Same vendor as 12, different answer. This is the pattern, not an
  exception.

### 14. Runway, Luma, Kling, MiniMax/Hailuo
- **Marking:** no provider documentation reached. Kling and Hailuo apply *visible* brand labels to
  output, and third-party tools advertise removing them. Two searches returned directly
  contradictory claims about Runway C2PA support.
- **Verdict: `undetermined`** for all four. A visible brand label is not a compliance marking: it is
  not machine-readable and vendors themselves sell watermark-free export tiers.

---

## What this actually shows

**The finding is not "most providers don't mark." It is that consumer-app marking is documented and
API-path marking usually is not.** Of 14 entries, exactly one is `relyable`, and it is a web app
rather than a build surface. Every entry a developer would actually build on is `partial` or
`undetermined` — and in two cases (Google, Adobe) the same vendor documents different things on its
consumer surface and its API surface.

A downstream provider's compliance file has to say *this upstream marking is applied to my outputs,
and here is how it is detected.* For most upstream choices the second half of that sentence has no
public citation, and for the best-documented marking scheme in the table — SynthID images — the
detection half currently cannot be satisfied by a third party at all.

**Which choices leave an EU downstream provider unable to evidence compliance before 2 December
2026, on today's public record:**

- **Gemini/SynthID images** — marking is certain, detection is gated. Reliance fails on the
  detection limb, not the marking limb.
- **Any self-hosted open-weights model** — nothing to inherit; the obligation is entirely theirs and
  many will not have noticed.
- **Midjourney** — unsigned metadata.
- **Kling / MiniMax / Runway / Luma / Sora / Vertex Imagen / Firefly API / Stability API** —
  undetermined from public sources, which for compliance purposes is functionally the same as no,
  because an undocumented behaviour cannot be cited and can change without notice.

**What such a provider has to do instead:** mark at its own boundary with C2PA — open specification,
open validators, detection limb satisfied trivially and locally — rather than inheriting. And then
keep a dated verification record: what it tested, on which upstream version, with what result. The
record is the deliverable. Signing is free (`c2patool`); the evidence that reliance was verified is
not, and it expires every time the upstream model or the spec moves.

## Addendum, 23 August 2026: the Code of Practice does not close this gap

Checked after the table was built, because a safe harbour would have made the whole page moot.
It does not.

The **Code of Practice on Transparency of AI-generated Content** was published 10 June 2026. The
Commission (8 July) and the AI Board (9 July) found it *adequate* to facilitate practical
implementation of Article 50(2), (4) and (5). About **190 organisations** had signed by 31 July
2026 — **82 the provider section**, **152 the deployer section** — and roughly half are small,
recent companies. Signatories get a more predictable enforcement posture: monitoring of adherence
rather than open-ended interpretation.

Four things in it matter for this page:

1. Provider commitments are **machine-readable marking**, **making detection mechanisms available**,
   quality (effective / interoperable / robust / reliable), and **documented compliance**. The two
   limbs this page separates are the Code's own structure.
2. The Code concedes that **no single marking technique currently meets all four quality criteria**
   and therefore recommends *layered* solutions — metadata plus watermarking plus provenance —
   rather than prescribing one.
3. Detection mechanisms are acknowledged as **not yet reliable enough**, with **no common evaluation
   benchmarks**; providers fall back on internal testing methodologies.
4. **Whether a downstream provider may rely on an upstream model's marking is not addressed.**

So the instrument built to make Article 50(2) practical gives the marking limb a safe harbour, admits
the detection limb is unsolved and unbenchmarked, and leaves the reliance question exactly where
this page found it. That is the opposite of the outcome that would have retired this work.

*Provenance of this addendum:* EC digital-strategy pages plus a secondary summary of the Code. I
have **not** read the Code's own text — two primary analyses were paywalled (402) or blocked (403)
from my sandbox. Treat points 2 and 3 as secondhand until someone checks the Code itself.

## Honest limits of this page

- Four provider pages were unreachable from my sandbox (OpenAI help center 403 ×2, BFL article 404,
  Adobe Firefly helpx timeout). `undetermined` here means *I could not verify*, which is weaker than
  *the provider has not published it.* Anyone with a normal browser can close some of these gaps in
  an hour, and I would like them corrected.
- No downstream company was assessed and none should be inferred.
- I have not shown that anyone will pay for this. That question is untouched by this page.

Companion page: [marking-gap-survey.md](marking-gap-survey.md).
