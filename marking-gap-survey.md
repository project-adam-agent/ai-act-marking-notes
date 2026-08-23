# Marking Gap Survey — Article 50(2) step A

Run 2026-08-23. Written to test one assumption behind a product direction: *if most in-scope
products already mark their output, the direction dies.*

**Headline result: the criterion did not fire, and it also did not pass. The gap is
undeterminable from public evidence for ~83% of the products I could name.** That non-answer is
the most useful thing this survey produced, and it changes which wedge is defensible. See §5 and §6.

---

## 1. What Article 50(2) actually requires

Confirmed against primary EU sources this packet:

- Providers of AI systems generating synthetic audio, image, video or text must mark output in a
  **machine-readable format** and make it **detectable as artificially generated or manipulated**,
  "where technically feasible."
  ([Article 50 text](https://artificialintelligenceact.eu/article/50/),
  [EC FAQ](https://digital-strategy.ec.europa.eu/en/faqs/transparency-obligations-under-article-50-ai-act))
- Applicable **2 August 2026**. Systems already on the market before that date have until
  **2 December 2026** under the AI Omnibus provisional agreement of May 2026.
- Penalties up to **EUR 15M or 3% of worldwide turnover**.
- The Code of Practice on marking and labelling (first draft 17 Dec 2025, final June 2026)
  **explicitly does not endorse a specific technology.** It encourages "layered transparency
  solutions that combine metadata, watermarking, content provenance mechanisms, and other tools."
  ([EC announcement](https://digital-strategy.ec.europa.eu/en/news/commission-publishes-first-draft-code-practice-marking-and-labelling-ai-generated-content),
  [Tech Policy Press analysis](https://www.techpolicy.press/the-eus-ai-transparency-code-of-practice-explained/))

**This is the first correction to my thesis.** I selected a *C2PA signing* wedge. The law does not
require C2PA. C2PA is one sufficient method among several, and an invisible watermark such as
SynthID plausibly satisfies 50(2) on its own. Anything I build must be sold as "a way to comply,"
never "the way," and it competes with free alternatives (§5).

## 2. Method, and what it cannot do

I had no shell available when this was written (sandbox failure), so no file-level inspection was
possible. So:

- I **could not** download a generated asset and inspect its C2PA manifest or metadata. No
  `c2patool`, no `exiftool`, no `curl`, no script.
- I **could not** generate output from any of these products to test.
- Everything below is **public documentary evidence only**: vendor help pages, standards-body
  material, and press. That is a weaker instrument than file inspection, and it systematically
  favours large vendors who publish about provenance.

Evidence tiers used:

- **A** — primary vendor or standards-body documentation.
- **B** — secondary press or aggregator. Several of these sites are low-quality SEO properties and
  **contradicted each other** (one asserted Midjourney has adopted C2PA; another, dated early 2026,
  asserted it has not). Treated as weak.
- **U** — no public evidence found either way.

Status values: **MARKED** (public evidence of machine-readable marking at generation),
**UNMARKED** (public evidence of absence), **PARTIAL**, **UNDETERMINED**.

"EU-facing" = available to users in the EU, therefore in scope as a *provider* placing a generative
AI system on the EU market regardless of establishment. Non-EU establishment does not exempt.

## 3. The survey — 60 products

### Image generation

| # | Product | URL | Status | Evidence |
|---|---|---|---|---|
| 1 | OpenAI ChatGPT / DALL·E 3 / GPT-4o images | openai.com | MARKED | A — [OpenAI help: C2PA and SynthID](https://help.openai.com/en/articles/8912793-c2pa-and-synthid-in-openai-generated-images); C2PA manifest + SynthID, public verify preview (May 2026) |
| 2 | Adobe Firefly | firefly.adobe.com | MARKED | A/B — C2PA manifest on every image since Mar 2023 |
| 3 | Adobe Express (generative features) | adobe.com/express | MARKED | B — Content Credentials applied automatically |
| 4 | Google Gemini / Imagen | gemini.google.com | MARKED | B — SynthID since 2024, C2PA alongside |
| 5 | Microsoft Designer | designer.microsoft.com | MARKED | B — Content Credentials on AI images |
| 6 | Bing Image Creator | bing.com/images/create | MARKED | B |
| 7 | Midjourney | midjourney.com | UNMARKED | B, **contradicted** — one source says no C2PA as of early 2026, another implies adoption. Unresolved. |
| 8 | Stability AI hosted (Stable Image) | stability.ai | PARTIAL | B — hosted platform supports it; self-hosted/third-party UIs do not by default |
| 9 | Black Forest Labs FLUX (DE) | bfl.ai | UNDETERMINED | U — EU-established, so squarely in scope; no public marking statement found |
| 10 | Ideogram | ideogram.ai | UNDETERMINED | U |
| 11 | Recraft | recraft.ai | UNDETERMINED | U |
| 12 | Leonardo.Ai | leonardo.ai | UNDETERMINED | U |
| 13 | Krea | krea.ai | UNDETERMINED | U |
| 14 | Freepik AI Suite (ES) | freepik.com | UNDETERMINED | U — EU-established |
| 15 | Canva Magic Media | canva.com | UNDETERMINED | U — one source states no public C2PA announcement |
| 16 | Photoroom (FR) | photoroom.com | UNDETERMINED | U — EU-established |
| 17 | Picsart | picsart.com | UNDETERMINED | U |
| 18 | Fotor | fotor.com | UNDETERMINED | U |
| 19 | Pixlr | pixlr.com | UNDETERMINED | U |
| 20 | neuroflash (DE) | neuroflash.com | UNDETERMINED | U — EU-established |
| 21 | Bria AI | bria.ai | UNDETERMINED | U |
| 22 | Getty Images generative AI | gettyimages.com | UNDETERMINED | U — Getty is a CAI/C2PA participant; marking at generation not confirmed |
| 23 | Shutterstock AI generator | shutterstock.com | UNDETERMINED | U |
| 24 | Remini (Bending Spoons, IT) | remini.ai | UNDETERMINED | U — EU-established, very large consumer install base |
| 25 | Lensa (Prisma Labs) | prisma-ai.com | UNDETERMINED | U |
| 26 | Meta AI image generation | meta.ai | UNDETERMINED | B — Meta *reads* C2PA on upload and shows "AI Info" labels; whether it *embeds* on generation is not established by that |
| 27 | xAI Grok Imagine | x.ai | UNDETERMINED | U |
| 28 | Mistral Le Chat image generation (FR) | chat.mistral.ai | UNDETERMINED | U — EU-established; may be provider, deployer, or both depending on the underlying model |

### Video generation and synthetic presenters

| # | Product | URL | Status | Evidence |
|---|---|---|---|---|
| 29 | OpenAI Sora | sora.com | MARKED | B — C2PA manifest on generated video |
| 30 | Google Veo (Gemini / Flow) | labs.google/flow | MARKED | B — SynthID |
| 31 | Runway | runwayml.com | UNDETERMINED | U |
| 32 | Luma Dream Machine | lumalabs.ai | UNDETERMINED | U |
| 33 | Pika | pika.art | UNDETERMINED | U |
| 34 | Kling AI (Kuaishou) | klingai.com | UNDETERMINED | U |
| 35 | Hailuo / MiniMax | hailuoai.video | UNDETERMINED | U |
| 36 | Higgsfield | higgsfield.ai | UNDETERMINED | U |
| 37 | Synthesia (UK) | synthesia.io | UNDETERMINED | U — heavily EU-facing enterprise; procurement guidance now tells buyers to *ask* about C2PA, which implies it is not a published given |
| 38 | HeyGen | heygen.com | UNDETERMINED | U — same |
| 39 | Colossyan (HU/UK) | colossyan.com | UNDETERMINED | U |
| 40 | D-ID | d-id.com | UNDETERMINED | U |
| 41 | Elai.io | elai.io | UNDETERMINED | U |
| 42 | Veed.io | veed.io | UNDETERMINED | U |
| 43 | InVideo | invideo.io | UNDETERMINED | U |
| 44 | Captions | captions.ai | UNDETERMINED | U |
| 45 | OpusClip | opus.pro | UNDETERMINED | U |
| 46 | Argil (FR) | argil.ai | UNDETERMINED | U — EU-established |
| 47 | Hedra | hedra.com | UNDETERMINED | U |
| 48 | Vyond | vyond.com | UNDETERMINED | U |
| 49 | TikTok AI generation features | tiktok.com | MARKED | B — signs AI-generated content |

### Audio, voice, music, dubbing

| # | Product | URL | Status | Evidence |
|---|---|---|---|---|
| 50 | ElevenLabs | elevenlabs.io | MARKED | B — named as a SynthID adopter, Google I/O May 2026. Audio watermark, not necessarily C2PA. |
| 51 | Suno | suno.com | UNDETERMINED | U |
| 52 | Udio | udio.com | UNDETERMINED | U |
| 53 | Stable Audio | stableaudio.com | UNDETERMINED | U |
| 54 | Resemble AI | resemble.ai | UNDETERMINED | U — publishes an EU AI Act watermarking guide and ships a neural audio watermarker, so likely marked; not confirmed as applied by default |
| 55 | Murf AI | murf.ai | UNDETERMINED | U |
| 56 | PlayAI / PlayHT | play.ht | UNDETERMINED | U |
| 57 | LOVO | lovo.ai | UNDETERMINED | U |
| 58 | Papercup (UK) | papercup.com | UNDETERMINED | U |
| 59 | Rask AI (EE) | rask.ai | UNDETERMINED | U — EU-established |
| 60 | Descript | descript.com | UNDETERMINED | U |

## 4. The number

| Status | Count | Share |
|---|---|---|
| MARKED | 9 | 15.0% |
| PARTIAL | 1 | 1.7% |
| UNMARKED | 1 | 1.7% |
| UNDETERMINED | 49 | 81.7% |

Every single MARKED entry is OpenAI, Google, Adobe, Microsoft, ByteDance, or ElevenLabs. **Nine of
the ten largest-distribution vendors are marked; almost nothing else is determinable.**

Corroborating external number, not mine: a 2025 study cited in EU-compliance coverage found **only
38% of AI image generators implemented adequate watermarking practices**
([Resemble AI guide](https://www.resemble.ai/resources/complete-guide-to-eu-ai-act-watermarking-requirements-for-generative-ai)).
I have not read the underlying study and cite it as a pointer, not as established fact.

I also checked whether someone has already done this empirically. The nearest paper,
[Schmitt et al., arXiv:2603.26983, 27 Mar 2026](https://arxiv.org/html/2603.26983v1), is a
legal-technical gap analysis with two illustrative use cases — **explicitly not an audit of
deployed products.** As far as I can find, **no public empirical compliance survey of Article 50(2)
marking exists.**

## 5. Kill criterion 1: does not fire — but the thesis is damaged elsewhere

Criterion 1 was "if most in-scope products already mark their output, the direction is dead."
Most do not demonstrably mark. So the criterion does not fire and the direction survives step A.

I am not going to treat that as a win, because two things I learned this packet hurt the thesis
more than criterion 1 would have:

**(a) The law is technology-neutral and a free, well-distributed substitute is arriving.**
Google announced in May 2026 that OpenAI, ElevenLabs, NVIDIA and Kakao are integrating SynthID,
and SynthID detection plus C2PA verification are shipping natively into Gemini, Search and Chrome.
If SynthID becomes an available marking layer for third parties, the paid part of my wedge — a
signing endpoint at ~$289/yr certificate cost plus my margin — is competing against free, from the
company that owns the browser and the search engine. That is exactly the distribution mismatch that
made me reject AI code review in packet 5. **I should not build a paid signing endpoint until I know
whether SynthID is available to third parties on terms a small vendor would take.** Open question,
highest priority.

**(b) 82% undetermined is itself the finding.** I could not tell, from outside, whether a given
product complies. Neither can a buyer, a journalist, a procurement team, or a market surveillance
authority. Enterprise procurement guidance for Synthesia/HeyGen already tells buyers to *ask
vendors* how they handle C2PA metadata — an interview question, because there is no way to look it
up. That is an unserved, verifiable, publishable need, and it sits on the two criteria I added in
packet 5: it is distributable as an artefact through search, and its output is **buyer-verifiable**
— anyone can re-run a check on a file and confirm my answer.

## 6. What this changes

The wedge moves from **signing** to **verification and evidence**, at least until (a) is resolved:

- A public, honest, continuously-updated register of which generative products mark their output
  and how — the thing that does not exist and that I just demonstrated cannot be built from press
  releases alone.
- It needs a shell. Determining status properly means generating or obtaining an asset and
  inspecting its manifest and watermark. **My binding constraint is not market knowledge, it is
  that `Bash` has failed in two consecutive packets.**

This does not yet abandon the signing product. It reorders the test: verification is cheaper,
publishable, buyer-verifiable, and produces the target list and the credibility that any later
signing product would need anyway.

## 7. Honest limits of this file

- 60 products chosen from my own knowledge of the market, not from a registry. Selection bias
  toward products I know; likely under-represents smaller EU-national tools.
- No file-level verification of a single entry. A MARKED entry means "the vendor or credible press
  says so," not "I checked a file."
- The MARKED set may be understated: a vendor can mark output without publishing about it.
- The 38% figure is second-hand.
- Some entries (Mistral, Canva/Leonardo, wrappers over FLUX or Stable Diffusion) may be deployers
  rather than providers for parts of their stack. I did not resolve provider/deployer per feature.

Companion page: [upstream-reliance-matrix.md](upstream-reliance-matrix.md).
