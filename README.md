# THE FEMALE OUTFIT PACK™

Part of **THE OUTFIT SYSTEM™** — the Female Edition.

A print-ready style reference PDF with **21 categories × 10 complete looks = 210 outfits**.
Every look is broken down piece-by-piece in a shoppable, flat-lay-friendly format:

```
BRAND — item description
```

…ordered top → bottom / dress → layer → shoes → bag → accents, so each look
translates straight into a product grid or collage.

## The deliverable

- **`The-Female-Outfit-Pack.pdf`** — the finished 25-page pack (US Letter, 8.5×11").
  - Cover · Table of Contents · How-To-Use · 21 category pages · back cover.

## Categories

Business Attire · Vacation · Resort Wear · Airport · Lounging · Bedtime ·
Business Casual · Everyday Casual · Date Night · Nightlife · Luxury Shopping ·
Fitness · Streetwear · Brunch · Event Attire · Founder / Educator ·
Real Estate Professional · Beauty Professional · Travel Day · Winter & Fall ·
Spring & Summer

## Regenerating the PDF

The pack is generated from source so it's easy to edit or restyle.

```bash
cd build
python3 generate.py        # writes female_outfit_pack.html (fonts embedded)
# render to PDF with Chromium:
chrome --headless --no-pdf-header-footer \
  --print-to-pdf=female_outfit_pack.pdf female_outfit_pack.html
```

- **`build/data.py`** — all 210 looks (edit brands / pieces here).
- **`build/generate.py`** — layout + styling (feminine pink theme; Playfair Display,
  Bodoni Moda, Great Vibes, Poppins fonts embedded as base64).
- **`build/fonts/`** — the embedded font files.

### Note on styling

The looks are written as itemized **brand + piece** breakdowns (matching the labeled
reference style). They're built to be recreated as cut-out product flat-lays — swap in
your own product images to produce the collage layout.
