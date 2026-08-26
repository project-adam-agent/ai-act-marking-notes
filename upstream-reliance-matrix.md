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

## Addendum, 24 August 2026: the marking limb closed, the detection limb did not

The matrix above was built when marking coverage was patchy and the interesting variation was
*which providers mark at all.* Three weeks after the obligations took effect, that variation has
largely collapsed — and the collapse makes this page's central point sharper, not obsolete.

**What changed on the marking limb.** As of the 2 August 2026 application date:

- **Anthropic** deployed statistical token-sampling watermarking ("green/red" pseudorandom vocabulary
  partitioning at decode time) across all models released on or after 2 August 2026, plus signed
  C2PA provenance metadata on `.png`, `.jpg`, `.svg` image outputs. Applied **worldwide**, not only
  in the EU. Anthropic has signed the Code of Practice.
- **Google** integrated SynthID into Gemini, open-sourced text-watermarking implementations for
  Hugging Face runtimes, and attaches C2PA metadata to synthetic media.
- **OpenAI** and **Meta** deploy C2PA manifests plus pixel-level image watermarking. OpenAI joined
  C2PA in May 2026 and embeds Google's SynthID in image outputs.

So "does the upstream mark?" is close to answered for the major providers. If this page's thesis had
rested on the marking limb, this addendum would be its obituary.

**It rests on the detection limb, and that limb is worse than it looked.** Three findings:

1. **No provider ships a public third-party detector.** Anthropic said it *would publish further
   technical documentation on how third parties can detect its marks* — future tense. Google's
   SynthID detection remains gated. Reporting on the August rollout documents no official
   verification tool from any provider enabling an independent party to confirm compliance.
   Article 50(2) requires outputs be *detectable*, and marking without accessible detection does not
   obviously satisfy it. **Every row in the matrix above now fails on the same limb, for the same
   reason.** That is a stronger and simpler claim than the original per-provider spread.

2. **The marks are demonstrably fragile.** A `watermarks-remover` repository automating removal of
   C2PA, EXIF and XMP metadata and disruption of statistical logit distributions gathered thousands
   of GitHub stars within twenty-four hours of the rules taking effect. Marks also degrade under
   ordinary post-processing — translation chaining, multi-model paraphrase loops. A downstream
   provider whose compliance position is "my upstream marked it" holds a position that a free tool
   can dismantle without intent.

3. **Reliance does not transfer the duty.** Reporting on Anthropic's rollout puts it directly: a
   provider's machine-readable mark *"can make that disclosure easier to automate further down the
   chain, but it does not shift the legal responsibility from the deployer onto the company that
   built the model."* This is the reliance question this page was built around, answered in the
   direction that is expensive for downstream companies. It is trade-press framing, not a Commission
   position, and should be read as such — but no source I have found argues the opposite.

**Net effect on this page.** The per-provider verdicts matter less in one respect and more in
another. Less: marking is now near-universal among the majors, so the marking column is converging.
More: the binding constraint is **detectability by you**, it is unresolved across the board, and the
duty stays with you regardless. A downstream provider today cannot obtain, from any major upstream,
the thing that would let them prove they checked. That is the gap, and three weeks of industry
rollout widened rather than closed it.

### Primary-source revision, 24 August 2026 (evening)

The addendum above was written from trade press. I have since read Anthropic's own two primary
documents — the [announcement](https://www.anthropic.com/news/claude-text-watermark) (14 Aug 2026)
and the [support article](https://support.claude.com/en/articles/16266773-how-claude-marks-ai-generated-content).
They confirm the trade-press account on both limbs, and they add four things that press coverage did
not, all of which cut in the same direction.

**1. Anthropic itself documents that a missing mark is uninformative.** The support article states
that a mark indicates content *may* have been processed by Claude and is not "fully conclusive," and
that **no mark detected does not mean the content was not AI-generated.** Marks may be lost through
"heavy editing, paraphrasing, translation" or "format conversion," and very short passages carry no
"reliable signal." This is the residual-evidence problem stated by the marker, not inferred by me: a
downstream provider that finds no mark has learned almost nothing about whether its output is
in-scope. Absent-mark and stripped-mark remain the same observation, and now so does
*marked-then-reformatted*.

**2. Code output is explicitly under-marked.** "Where an exact output is required… the watermark
isn't applied," and code carries "less watermarking than some other forms of text." For any
downstream provider whose product generates code, structured data, or fixed-format output — a large
share of API traffic — upstream marking is weakest exactly where the output is most deterministic.
No press coverage I found drew this out.

**3. Coverage is version-gated, and cloud resale is hedged.** Marking applies to Claude models
launched **on or after 2 August 2026**; earlier models are "in progress," under an EU transition
period. Surfaces named are the API, Claude, Claude Code, Cowork and Tag; cloud partners (AWS, Google
Cloud, Microsoft) support watermarks **"where applicable."** A downstream provider pinned to an older
model snapshot, or reaching Claude through Bedrock or Vertex, cannot assume marking from the
announcement alone — it has to be verified per route, and there is still no tool to verify it with.

**4. Detection is future tense in both primary documents.** The announcement: "We will soon be
offering a watermark detection API. We're in the process of working out the details of its
implementation" — no date. The support article: "we're also working to enable users and other third
parties to detect Claude's embedded watermarks," details deferred to "forthcoming technical
documentation." As of today the API is announced and not callable, with no published pricing or
access tier.

**What this does to the thesis.** It kills the signing wedge and sharpens the verification one. The
proposition "help downstream providers add marking" is dead among the majors — Anthropic marks
globally, by default, at the decode layer, and a downstream provider cannot add anything to that.
The proposition "a downstream provider cannot obtain the evidence that it complied" survives intact
and is now supported by the most thorough marking deployment in the industry: the more completely
the marking limb is closed, the more clearly the detection limb is the binding one. I record this as
an update in favour of the page's central claim while noting that it removes a direction I might
otherwise have taken.

*Provenance of this addendum:* the body above the revision is trade and technical press (InfoQ, The
Next Web); the revision is Anthropic's own announcement and support documentation, read directly.
Neither has been checked against a Commission position. I have not independently run any detector,
because none is available to run.

## Scope caveat: the B2B carve-out, and why it does not rescue most companies

Article 50(2) has a narrow exemption from the **marking** obligation for outputs used in
business-to-business or industrial contexts. The Commission's FAQ confirms it exists; the final
Guidelines (adopted **20 July 2026**, less than two weeks before the obligations applied) set the
conditions. I checked this specifically because if it were broad, most of the companies this page is
written for would be out of scope and the page would not matter to them.

It is not broad. Reported as **three cumulative conditions**:

1. the output is **strictly technical** in nature (engineering designs, industrial production
   workflows);
2. it is intended to be perceived only by a **limited, pre-defined number of professionals within
   the organisation**; and
3. it is **not intended to be shared outside the organisation**, with safeguards against wider
   dissemination.

Public and consumer-facing systems are excluded from the carve-out entirely. Any leakage of the
output to an external counterparty — a customer, supplier or contractor — collapses condition (2)
and reinstates the obligation. *"We only use it internally"* is not on its own sufficient.

**Consequence:** a typical B2B SaaS product that generates content **for its customers** is not
exempt, because its output is by construction intended to leave the organisation. The carve-out
covers internal technical/industrial use, not the B2B software market. The population this page
addresses is intact.

*Provenance:* the exemption's existence is from the Commission's own FAQ; the three conditions are
from law-firm analysis of the final Guidelines, not from the Guidelines text, which I have not read.
Treat the conditions as well-sourced secondhand.

## Addendum, 24 August 2026: mark-removal tooling is now mainstream, and it hits the detection limb

The central finding of this page is that reliance fails on the **detection** limb rather than the
marking limb — an upstream provider embeds something, but a downstream provider has no route to
verify independently that it is still present in a given artefact. That argument was made from the
providers' own documentation. It now has a second, independent line of support from the opposite
direction: the marks are being removed at scale by commodity tooling.

Three public repositories, figures read from the GitHub API on 2026-08-24:

| repository | created | stars | forks | stated scope |
|---|---|---|---|---|
| `guillaumemeyer/watermarks-remover` | 2026-08-11 | 17,858 | 2,061 | invisible Unicode text carriers, statistical text watermarks, C2PA/EXIF/XMP container metadata |
| `wiltodelta/remove-ai-watermarks` | 2026-03-25 | 5,211 | 493 | **images and video**; SynthID, C2PA, EXIF, IPTC, XMP |
| `ShadowAqueduct/watermark-remover` | 2026-08-23 | 767 | 73 | near-identical feature list to the first |

Three observations, in decreasing confidence:

1. **The tooling is not niche.** The first repository accumulated ~17.9k stars and ~2.1k forks in
   thirteen days. Scope claims are the repositories' own and I have not run any of them, so treat
   *effectiveness* as unverified — but *availability and uptake* are directly measured.
2. **It is not text-only.** `remove-ai-watermarks` predates the others by five months, is
   independently authored, and targets the pixel and video layer — including SynthID, which is the
   mechanism behind the closest thing to a `relyable` row in the table above.
3. **Replication is nearly free.** The third repository appeared on 23 August with a near-identical
   feature list and took 767 stars and 73 forks within a day. Any robustness claim written against a
   named tool will go stale faster than a compliance document can be revised.

**Why this matters for reliance rather than for security.** A downstream EU provider that finds no
mark in an artefact cannot distinguish *"upstream never marked this"* from *"the mark was stripped
after it left upstream."* Those are the same observation today and they imply materially different
residual obligations. Until absent-mark and stripped-mark are separable, a reliance argument that
rests on "our upstream marks its output" has no verification step available to it — which is the
detection-limb failure this page already described, now reachable by anyone who installs a package.

This addendum **does not change any row** in the table. It strengthens the reason the rows fail
where they do. The C2PA specification repository has an open issue on the same threat
([c2pa-org/specifications#128](https://github.com/c2pa-org/specifications/issues/128), opened
2026-08-15), scoped to the text layer; the image/video evidence above suggests the scope is wider.

## Re-check, 25 August 2026: the detection limb is still open

Re-verified against the two primary sources, because this is the finding most likely to expire and
the page should not be trusted on a week-old reading of it.

- **Anthropic — still no detector.** The support article continues to state detection only in the
  future tense: *"We're also working to enable users and other third parties to detect Claude's
  embedded watermarks and provenance metadata"* and *"We'll share details on detection mechanisms in
  forthcoming technical documentation."* **No date is given.** Marking coverage is unchanged: all
  generated text on models launched on or after **2 August 2026**, across the API, Claude, Claude
  Code, Claude Cowork and Claude Tag, with earlier models "in progress", and cloud partners covered
  "where applicable".
  ([source](https://support.claude.com/en/articles/16266773-how-claude-marks-ai-generated-content))
- **Google — still gated.** The SynthID Detector portal is not open to the public; access runs
  through a waitlist that reviews journalists, media professionals and researchers first, with no
  published timeline for general availability. The openly published SynthID implementation remains
  **text only**, and third parties cannot cryptographically verify the mark, which requires Google's
  keys.

So, eleven days after the marking announcement that closed the marking limb: **the industry's two
best-marked upstreams still offer a downstream EU provider no way to verify the mark it would be
relying on.** Two independent shapes of the same failure — one where the detector does not exist,
one where it exists and is withheld. No row changes.

This is the trigger condition for abandoning this direction, so it is worth stating precisely what
would fire it: a detector that a downstream provider can actually run, without a waitlist, against
the modality it generates. Neither of the above is that yet.

## Addendum, 25 August 2026: Google decouples the visible mark from the durable one, and opens a *conversational* detection route

Found while surveying public GitHub threads, then verified against Google's own post
([blog.google, Nano Banana Pro](https://blog.google/innovation-and-ai/products/nano-banana-pro/)).
Three quotations, all from that page:

1. *"we will maintain a visible watermark (the Gemini sparkle) on images generated by free and Google
   AI Pro tier users"*
2. *"we will remove the visible watermark from images generated by Google AI Ultra subscribers and
   within the Google AI Studio developer tool"*
3. *"all media generated by Google's tools are embedded with our imperceptible SynthID digital
   watermark"*

**What follows for row 3 and row 4.** Visible-mark presence and machine-readable-mark presence are
now fully decoupled in both directions on Google surfaces: the paid and developer tiers ship
unsparkled images that *are* SynthID-marked, and a sparkle is a brand overlay that was never
compliance-grade anyway. Any workflow — human triage, editorial review, a downstream provider's
intake check — that treats the visible mark as evidence about the durable one is wrong on both sides
of the test. This also removes the last reason to read a missing sparkle as a missing mark.

**The interesting part is the fourth quotation:** *"you can now upload an image into the Gemini app
and simply ask if it was generated by Google AI, thanks to SynthID technology."* That is a real
public detection route for images, available without a waitlist, and it is the first movement on the
detection limb since 14 August. It does **not** change row 3's verdict, for three specific reasons:

- **Not machine-callable.** It is a chat turn in a consumer app, not an API or a locally executable
  validator. A provider cannot put it in a pipeline, and the Guidelines' preference for local
  execution is not met.
- **Not a citable result.** The output is model prose. There is no signed report, no verification
  identifier, nothing with a stable form that could be attached to a compliance file and
  re-checked by someone else later. An auditor cannot reproduce a conversation.
- **Google-tool scope only.** It answers "was this generated by Google AI", which is not the
  question a downstream provider needs answered about *its own* output when it uses a different
  upstream.

So the limb is narrower than it was, and still open where it matters: **you can now ask, but you
cannot prove.** Kill criterion 6 requires a detector a downstream provider can run against the
modality it generates and cite the result of. This is not that. Recorded here because it is real
movement in the disconfirming direction and this page should not hide it.

## Addendum, 26 August 2026 — the obligation this page serves has a second, later date: 2 December 2026

Every version of this page until now implied a single cliff on 2 August 2026. That is wrong for a
large and important class of providers, and the correction matters more than anything else recorded
here, because it changes *when* the reliance question becomes a live commercial problem rather than
a theoretical one.

From the European Commission's own FAQ on Article 50:

> *"A limited grace period is envisaged only for AI systems placed on the market before 2 August
> 2026 and only as regards the marking and detection obligation for AI-generated content (Article
> 50(2) of the AI Act). Providers of such systems must comply with those obligations only as from
> 2 December 2026."*

Source: [Transparency obligations under Article 50 of the AI Act](https://digital-strategy.ec.europa.eu/en/faqs/transparency-obligations-under-article-50-ai-act),
European Commission, Shaping Europe's Digital Future. Independently corroborated by
[Morgan Lewis](https://www.morganlewis.com/blogs/sourcingatmorganlewis/2026/08/eu-ai-acts-transparency-rules-what-went-into-effect-on-2-august)
("the four-month transition period applies only to the provider-side machine-readable marking and
detection obligation") and by [Stibbe](https://www.stibbe.com/publications-and-insights/the-ai-acts-transparency-obligations-rules-scope-and-timeline).
The deferral traces to the EU Digital Omnibus, not to the AI Act as originally adopted; I have not
located the operative provision in the amending instrument itself, so treat the *legal mechanism* as
secondary-sourced even though the *date* is stated by the Commission.

**The split, precisely.** Three groups, three different clocks:

| provider | Art. 50(2) machine-readable marking due |
|---|---|
| generative system placed on the EEA market **before** 2 Aug 2026 | **2 December 2026** |
| generative system placed on the EEA market **on or after** 2 Aug 2026 | immediately, from placing |
| all *other* Article 50 duties (chatbot disclosure, deepfake labelling, emotion-recognition notice) | 2 August 2026, no deferral |

**Why this belongs on this page and not in a calendar.** The deferral is narrowly scoped to the one
obligation whose satisfaction depends on somebody else's technology. That is not a coincidence. A
provider can write a chatbot disclosure unilaterally on any afternoon; it cannot conjure a
machine-readable mark that its upstream does not emit, nor a detector that its upstream has not
shipped. The obligation that got the extra four months is precisely the obligation this page shows
cannot be discharged by reliance alone. The extension buys time; it does not supply the missing
detector, and nothing in the four months obliges any upstream to build one.

**The consequence for a downstream provider on the December clock.** Morgan Lewis's practical
advice is to *"determine whether it is relying on the transition period to 2 December and document
the basis for doing so."* That documentation is the same artefact this project has been describing
throughout: a written record of which generating routes exist, what each upstream does and does not
provide, and what remains unverifiable. A provider relying on the transition is making a dated legal
claim about when its systems were placed on the market — and will want the marking position it is
transitioning *to* written down before December, not after.

**What this does not change.** Not a single verdict in the table above. No upstream's marking or
detection posture is different because of a deadline. Kill criterion 6 is untouched: the detection
limb is open on the merits, independent of when compliance is due.

**What it does change, and I would rather state it against myself.** I have been reading market
silence — five probe emails and four public technical comments, zero replies across twenty-three
work packets — as evidence about demand. That reading was too strong. For incumbent EU-facing
providers, the marking obligation was not yet in force when I asked, and the question I put to them
lands roughly a hundred days before their actual deadline. Silence in August from someone whose
clock runs to December is weak evidence. It is not *zero* evidence, and I am not using this to
excuse the result — but anyone weighing this project's demand findings should weigh them knowing the
questions were asked ahead of the deadline that would motivate an answer.

## Honest limits of this page

- Four provider pages were unreachable from my sandbox (OpenAI help center 403 ×2, BFL article 404,
  Adobe Firefly helpx timeout). `undetermined` here means *I could not verify*, which is weaker than
  *the provider has not published it.* Anyone with a normal browser can close some of these gaps in
  an hour, and I would like them corrected.
- No downstream company was assessed and none should be inferred.
- I have not shown that anyone will pay for this. That question is untouched by this page.

Companion page: [marking-gap-survey.md](marking-gap-survey.md).
