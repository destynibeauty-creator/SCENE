# THE SCENE AI — 15s Launch Ad ("ACTION.")

A copy-paste, shot-by-shot production package for a 9:16 cinematic ad.
Built for image-to-video tools (Sora 2, Kling 2.5, Runway Gen-4, Veo 3.1) —
lock the identity on a reference photo first, then feed that photo + each
shot prompt below into the tool so the same face survives all 8 cuts.
This doc does not render pixels; it is the exact input a video model needs.

**Reference identity image:** `scene-os/marketing/keyart/keyart-square-destyni.jpg`
already in this repo — deep brown skin, oval/full face, almond dark eyes,
long black body-wave hair, matches the brief. Use it as the MASTER. If you
want a fresh MASTER shot in the exact hoodie wardrobe below instead, run
the MASTER prompt in `scene-os/products/The-SCENE-AI_FREE_The-Character-Starter.pdf`
first, save that photo, then come back here.

---

## IDENTITY LOCK (paste into every shot that shows her face)

> Same woman in every shot, exact identity match to the reference photo:
> deep brown skin with warm undertones, oval/full face shape, almond dark
> eyes, full natural brows, long lashes, softly defined nose at realistic
> width, full glossy lips, natural cheek fullness, defined jawline and
> chin, natural facial asymmetry, realistic skin texture with visible
> pores and warm highlights, natural baby hairs at the hairline, long
> black body-wave hair. Do not lighten her skin. Do not alter her face
> shape or features. Do not idealize or over-beautify her. Skin reads as
> real skin, never waxy or plastic.

## WARDROBE LOCK (paste into every shot that shows her body)

> Black oversized "THE SCENE AI" hoodie, sleek black bottoms, glossy black
> thigh-high boots, silver jewelry, a heart necklace, soft glam makeup,
> long black body-wave hair with baby hairs. She stands on a white gaffer
> tape talent mark on the floor, like the lead of a series.

## MASTER STYLE BLOCK (paste at the end of every shot prompt)

> Cinematic, dark, expensive, futuristic production-set energy,
> ultra-realistic, high contrast, neon-lit. Deep black studio (#000000),
> glossy reflective black floor with real reflections, chrome film
> equipment. Electric cyan (#00E5FF) neon on one side, vibrant magenta
> (#F600A2) neon on the other side, subtle fog in the air. Realistic lens
> blur, shallow cinematic depth of field, physically accurate light and
> reflections. 9:16 vertical, shot on a cinema camera, 24fps, luxury
> trailer pacing — fast but smooth, every movement intentional. No
> cartoon style, no anime, no waxy or plastic skin, no face drift, no
> distorted hands, no extra fingers, no broken jewelry, no warped face,
> no blurry facial features, no random or unreadable text, no messy
> background, no corporate office, no classroom, no cheap AI look.

---

## Shot-by-shot (8 clips, ~2s each → 15s timeline)

### Shot 1 — 0:00–0:02 · "NOT RANDOM AI."
> Black screen. A single small acid-lime (#C6FF00) indicator light clicks
> on in extreme close-up, sharp focus, tiny lens flare, black background
> falling away into darkness on all sides. Low cinematic bass hit on the
> click. + MASTER STYLE BLOCK
**On-screen text:** `NOT RANDOM AI.` (off-white, appears as the light clicks on)

### Shot 2 — 0:02–0:04 · "A PRODUCTION SYSTEM."
> Fast smooth camera whip-pan into a dark production studio. Chrome film
> gear — tripods, lens cases, a boom arm — catches streaks of cyan light
> from the left and magenta light from the right as the camera moves. A
> giant director's monitor in the center of the room powers on, its glow
> spilling across the wet-look black floor. + MASTER STYLE BLOCK
**On-screen text:** `A PRODUCTION SYSTEM.`

### Shot 3 — 0:04–0:07 · "THE FACE MATCHES."
> The giant center-frame director's monitor displays a sharp close-up of
> the female lead's face, locked and realistic. Camera UI overlays on the
> monitor glass: "FPS 24.000" top left, a small pulsing red "REC" dot top
> right, thin white frame guides at the corners, a focus reticle centered
> on her eyes, a running timecode bottom left, "WB 3200K" bottom right.
> + IDENTITY LOCK + MASTER STYLE BLOCK
**On-screen text:** `THE FACE MATCHES.`

### Shot 4 — 0:07–0:09 · "THE WORLD MATCHES."
> Cut to the real female lead standing on a white-taped talent mark on
> the glossy black studio floor. She slowly lifts her chin and looks
> directly into the lens. Cyan rim light traces one side of her hair,
> magenta rim light traces the other side. Slight hair movement, subtle
> fog drifting behind her, slow push-in. + IDENTITY LOCK + WARDROBE LOCK
> + MASTER STYLE BLOCK
**On-screen text:** `THE WORLD MATCHES.`

### Shot 5 — 0:09–0:11 · "EVERY DETAIL LOCKED."
> Cut to a laptop screen glowing in the dark, showing a character-profile
> UI in clean off-white and chrome type on black: "CHARACTER: LEAD 01",
> "LOCKED", and a checklist reading "FACE ✓", "HAIR ✓", "BODY ✓",
> "STYLE ✓", "WORLD ✓". A quick glitch-style scan line sweeps once across
> the screen left to right. + MASTER STYLE BLOCK
**On-screen text:** `EVERY DETAIL LOCKED.`

### Shot 6 — 0:11–0:13 · "ONE CHARACTER. A WHOLE WORLD."
> Camera pushes forward through the glow of the director's monitor,
> transitioning like stepping through the screen, and emerges into a
> finished cinematic night-city world: wet reflective streets, luxury
> neon signage, cinematic bokeh in the deep background. The same woman
> now stands in that world — same face, same hair, same energy, same
> wardrobe — as if she stepped off the production set directly into her
> world. + IDENTITY LOCK + WARDROBE LOCK + MASTER STYLE BLOCK
**On-screen text:** `ONE CHARACTER.` then `A WHOLE WORLD.`

### Shot 7 — 0:13–0:14 · "THE SCENE AI"
> Cut back to the production studio. A director leans forward in frame
> at the edge of shot. The female lead stands on her mark, center frame.
> The director's monitor, a laptop on a nearby cart, and the real talent
> are all visible in one frame, all showing the same woman. + IDENTITY
> LOCK + WARDROBE LOCK + MASTER STYLE BLOCK
**On-screen text:** large chrome-metallic logo lockup `THE SCENE AI`,
subtitle beneath in off-white: `CREATE CINEMATIC CONTENT. BUILD YOUR DIGITAL WORLD.`

### Shot 8 — 0:14–0:15 · "ACTION."
> Clean black frame. Thin cyan neon corner bracket top-left, thin
> magenta neon corner bracket bottom-right, matching the logo's bracket
> motif. Nothing else in frame. + MASTER STYLE BLOCK
**On-screen text:** `ACTION.` (centered, off-white, holds on the final black frame)

---

## On-screen text — exact strings, nothing else
```
NOT RANDOM AI.
A PRODUCTION SYSTEM.
THE FACE MATCHES.
THE WORLD MATCHES.
EVERY DETAIL LOCKED.
ONE CHARACTER. A WHOLE WORLD.
THE SCENE AI
CREATE CINEMATIC CONTENT. BUILD YOUR DIGITAL WORLD.
ACTION.
```
Off-white text, no drop shadows that muddy legibility, generous margins —
vertical safe zone is the middle 80% of the 1080×1920 frame (avoid the top
~250px and bottom ~350px where app UI overlaps on TikTok/Reels/Shorts).

## Negative prompt (paste into every generation's negative/exclude field)
```
cartoon, anime, waxy skin, plastic skin, face drift, lighter skin tone,
different woman, distorted hands, extra fingers, broken jewelry, warped
face, blurry facial features, random text, misspelled text, unreadable
logo, messy background, corporate office, classroom, cheap AI look,
fantasy girlfriend energy, over-sexualized posing, cluttered composition
```

## Assembly
1. Generate all 8 clips as 9:16, 24fps, ~2s each from the reference
   MASTER photo (image-to-video mode keeps the face locked far better
   than text-to-video alone).
2. Cut together in order in CapCut/Premiere/Resolve — hard cuts, no
   crossfades, matches the "no chaotic transitions" note in the brief.
3. Add the on-screen text as a separate overlay layer (not baked into
   the generation) so every letter is guaranteed correct — the negative
   prompt above still applies to keep AI-rendered text out of frame.
4. Sound: low cinematic bass hit on Shot 1's light-click, a soft
   whoosh on the Shot 2 whip-pan and the Shot 6 push-through-the-monitor
   transition, silence (or a single low sub-hit) on the final black frame.
5. Export 1080×1920, H.264, target under 15s total runtime.
