# Defense deck review — Session 1 (Slides 1–5: s0–s4)

Reviewed against `thesis.tex` (final draft) and `docs/rejoinder.md` in the mau-thesis folder, so the notes below check the slides against what the thesis actually says, not just against the slide text itself.

---

## Slide 1 (s0) — Title

**What's there:** Full thesis title, subtitle, name, programme, supervisor, hero image placeholder (missing).

**Verified against thesis:** Title, author, programme, and supervisor name all match the thesis cover page exactly. Good — no drift between document and deck.

**What I'd change:**
- The hero image is a placeholder right now (`figures/hero-title.jpg` doesn't exist yet). A generic "Swedish skyline at dusk" stock photo is fine but generic — it doesn't say anything about *this* thesis. Since I can't fetch or generate a photorealistic stock image in this session, I'd rather build a custom vector graphic directly in the HTML: a stylised dot-grid map of Sweden, sparse dots in the north, denser in the south, echoing the coverage map you'll show later in the deck (s20/s21). It's on-theme, fully reproducible, and doesn't depend on sourcing a license-clean photo.
- Missing: Department ("Department of Technology and Society") is on the thesis cover page but not the slide — minor, optional to add.
- Missing: no examiner/opponent name or defense date/room on the slide. Most defense title slides include this. I don't have this information — see question below.

---

## Slide 2 (s1) — The problem

**What's there:** SMHI network is sparse, gaps are unmonitored, IoT sensors get placed by convenience not analysis, thesis builds the missing decision rule.

**Verified against thesis:** Matches the Introduction almost point for point — "positioned to characterise regional background concentrations... separated by margins that can span tens of kilometres" and "placement of such networks is frequently driven by property access, convenience, or local intuition." Accurate, not overstated.

**What I'd change:** Nothing structurally — this is a clean three-beat setup (sparse network → unmonitored gap → no principled placement) that lands the thesis's whole premise in one slide. I'd leave it text-only rather than adding a map here; the actual station map lands later (s15) and repeating it here would blunt that reveal.

---

## Slide 3 (s2) — Why it matters

**What's there:** PM2.5/NO2 health risk even at Swedish concentrations, Stockholm/Gothenburg/Umeå mortality studies, within-city exposure variation.

**Verified against thesis:** Matches Segersson et al. (2017) as cited in the Introduction — "contribute substantially to attributable cardiovascular and respiratory mortality... at concentrations that may remain formally below EU limit values." No invented statistics here, which is good discipline — the thesis itself doesn't cite a specific death count, so the slide correctly doesn't either.

**What I'd change:**
- Optional: add a small citation chip under the bullets — "Segersson et al., 2017" — since a defense committee will want to see you can source a health claim on sight, not just in the written thesis. Low cost, adds credibility, easy to skip if you'd rather keep slides citation-free and only cite verbally.

---

## Slide 4 (s3) — Three existing approaches

**What's there:** IDW, LUR (ESCAPE, 20 study areas), ML — three cards.

**Verified against thesis:** Accurate. The "20 study areas" figure for ESCAPE is correct (Eeftens et al. 2012 for PM2.5, Wang et al. 2013 for NO2, both cross-validated across the same 20 areas). The ML card's "often beats LUR" is a fair compression of the Agbehadji & Obagbuwa review cited in Background.

**What I'd change:**
- Add one bridging line under the three cards, something like *"But which one wins depends entirely on how you test it — and that's where this gets interesting."* Right now the jump from "here are three methods" (s3) straight into "random split lies to you" (s4) is a hard cut. A one-line bridge would make the pivot feel intentional rather than abrupt.

---

## Slide 5 (s4) — The random-split trap

**What's there:** Warns that random train/test splits leak information through nearby stations; cites Roberts et al. (2017); previews the buffered-neighborhood fix.

**Verified against thesis:** This is a precise summary of the Background section's spatial-autocorrelation discussion, and it's the right slide to introduce this concept — it explains *why* the accuracy numbers you'll show in s16/s17 can be trusted, before the audience has any reason to doubt them.

**What I'd change:** Nothing content-wise. One sequencing note (not a defect, just flagging my reasoning): I checked whether this slide would work better folded into the methodology section (around s11, "Buffered spatial leave-one-out") instead of appearing here in the motivation section — but placing it here does real work: it sets up the "gap" slide (s5, next chunk) which claims nobody has combined an honest accuracy-distance relationship with placement. Keep it here.

---

## Cross-cutting notes for this chunk

1. **No factual errors found.** Every number and claim I could check against `thesis.tex` (title, supervisor, health-effect cities, ESCAPE's 20 study areas, Roberts et al. framing) matches the final thesis text and the rejoinder to examiner comments.
2. **Heads-up for a later chunk, not acted on now:** your examiner specifically flagged that the 64 km / 6 km distance figures (used later on slide 19/s18) must not be called a "reliable prediction distance" without qualification — the thesis now says "estimated prediction-distance threshold under the adopted 50% criterion" throughout. Slide s18 currently uses the old, unqualified phrasing ("PM2.5 reliable prediction distance"). I'll flag this again with a specific fix when we reach that chunk (slides 16–20) so it doesn't slip through.
3. **Pacing:** these 5 slides are motivation-only (problem → stakes → prior art → methodological caveat), no results yet. That's a reasonable amount of ground to cover before RQs (s6) — but if your defense has a hard time limit, let me know it and I'll sanity-check total slide count against it as we go.

---

## Image needed for this chunk

**Only one**, for Slide 1 (s0), the hero image. Three options, ranked by what I can actually deliver in this session:

1. **(Recommended) I build a custom SVG dot-map of Sweden** directly in the HTML — no external file needed, on-theme, ties visually to your own results slides later. I can do this now.
2. **You send me a candidate photo** (skyline, satellite shot of Sweden, anything) and I'll fit it into the existing `md-img-wrap` frame — drop it in chat or tell me where it lives in your `mau-thesis` folder.
3. **Skip the hero image for now** and keep the title slide text-only/minimalist — some defense committees prefer this anyway.

No other images are needed for slides 1–5; the rest of this chunk is text/callout-only by design.
