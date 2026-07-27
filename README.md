# THE SCENE AI — Creator OS (brand-redesigned module PDFs)

The master bundle (`scene-os/build/source/`) rebuilt as **19 separate PDFs** —
one per module/bonus — restyled to the SCENE AI brand kit: jet-black pages,
Poppins typography, metallic-silver headings, electric-cyan `#00E5FF` +
vibrant-magenta `#F600A2` accents, and the corner-bracket motif from the logo.

- **`scene-os/pdfs/`** — the 19 finished PDFs (Start Here, Modules 01–12
  incl. 09A/09B + 10A/10B, Bonus 01–04). US Letter, fonts embedded.
Each section has its own signature color, and the text is set large and
high-contrast in plain, 6th-grade-level language so it is easy on the eyes
for readers of any age. Copy-paste AI prompts are preserved word-for-word.

- **`scene-os/build/extract.py`** — parses the original master bundle into
  structured content (`content.json`): headings, body, bullets, prompt blocks,
  tables (classified by font/size).
- **`scene-os/build/content_simple.json`** — the same content rewritten in
  plain language (prompt blocks untouched). Used automatically when present.
- **`scene-os/build/render.py`** — renders each module as a branded PDF
  (ReportLab; cover pages with corner brackets + gradient bar, dark prompt
  panels, themed tables, per-section accent colors in `DOC_ACCENT`).

```bash
cd scene-os/build
python3 extract.py     # source PDF -> content.json
python3 render.py      # content_simple.json (or content.json) -> ../pdfs/*.pdf
```

---

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
