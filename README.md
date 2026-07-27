# THE FEMALE OUTFIT PACK™

Part of **THE OUTFIT SYSTEM™** — the Female Edition.

A print-ready **flatlay lookbook**: **21 categories × 10 complete looks = 210 outfits**.
Every look is laid out as a labeled flatlay — each piece shown as a graphic with its
**brand** and **exact item**, ordered top → bottom / dress → layer → shoes → bag → accents.

## The deliverable

- **`The-Female-Outfit-Pack.pdf`** — the finished 46-page pack (US Letter, 8.5×11").
  - Cover · Table of Contents · How-To-Use · 21 category sections (2 flatlay pages each) · back cover.

## Categories

Business Attire · Vacation · Resort Wear · Airport · Lounging · Bedtime ·
Business Casual · Everyday Casual · Date Night · Nightlife · Luxury Shopping ·
Fitness · Streetwear · Brunch · Event Attire · Founder / Educator ·
Real Estate Professional · Beauty Professional · Travel Day · Winter & Fall ·
Spring & Summer

## About the flatlay art

The outfit graphics are **Microsoft Fluent Emoji (MIT-licensed)**, so the pack is free
to share, print, and sell. Each piece in a look is auto-matched to the right clothing or
accessory icon (dress, blazer, legging, heel, tote, sunglasses, lipstick, ring, watch…)
by its description, and sits on a **whisper-faint color chip** tinted to match the color
named in the piece (navy → soft blue, camel → warm tan, blush → pink…). Icons are
stylized stand-ins — **drop in your own product photos to turn any look into a
photographic flatlay** in the same layout.

> Photographic flatlays from Google/Pinterest couldn't be sourced directly: this
> environment's network policy blocks image hosts, and those pins are third-party
> copyrighted content. The MIT-licensed icons give a clean, distributable result you own.

## Regenerating the PDF

```bash
cd build
python3 generate.py        # writes female_outfit_pack.html (fonts + icons inlined)
# render to PDF with the pre-installed Chromium:
chrome --headless --no-pdf-header-footer \
  --print-to-pdf=female_outfit_pack.pdf female_outfit_pack.html
```

Source files:
- **`build/data.py`** — all 210 looks (edit brands / pieces here).
- **`build/iconmap.py`** — maps each piece to a flatlay icon (keyword rules).
- **`build/icons_used.json`** — the 32 vendored icons, so the pack rebuilds offline.
- **`build/generate.py`** — layout + styling (feminine pink theme; Playfair Display,
  Bodoni Moda, Great Vibes, Poppins fonts embedded).
- **`build/fonts/`** — embedded font files.
- **`build/iconpkg/`** — npm manifest for the full Fluent Emoji set (run `npm install`
  inside it only if you add icons beyond the vendored subset).

### Note

Chromium's `--print-to-pdf` renders **inline `<svg>`** but silently drops SVG `<img>`
data-URIs — the generator inlines every icon for this reason.
