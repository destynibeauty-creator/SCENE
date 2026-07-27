# -*- coding: utf-8 -*-
"""Render THE FEMALE OUTFIT PACK(TM) to a styled HTML file for Chromium -> PDF."""
import base64, os, html
from data import PACK

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "fonts")

def font64(name):
    with open(os.path.join(FONTS, name), "rb") as f:
        return base64.b64encode(f.read()).decode()

FACES = f"""
@font-face {{ font-family:'Playfair'; font-weight:700 900;
  src:url(data:font/ttf;base64,{font64('Playfair-Bold.ttf')}) format('truetype'); }}
@font-face {{ font-family:'Bodoni'; font-weight:700 900;
  src:url(data:font/ttf;base64,{font64('Bodoni-Bold.ttf')}) format('truetype'); }}
@font-face {{ font-family:'Vibes';
  src:url(data:font/ttf;base64,{font64('GreatVibes.ttf')}) format('truetype'); }}
@font-face {{ font-family:'Poppins'; font-weight:400;
  src:url(data:font/ttf;base64,{font64('Poppins-Regular.ttf')}) format('truetype'); }}
@font-face {{ font-family:'Poppins'; font-weight:500;
  src:url(data:font/ttf;base64,{font64('Poppins-Medium.ttf')}) format('truetype'); }}
@font-face {{ font-family:'Poppins'; font-weight:600;
  src:url(data:font/ttf;base64,{font64('Poppins-SemiBold.ttf')}) format('truetype'); }}
@font-face {{ font-family:'Poppins'; font-weight:700;
  src:url(data:font/ttf;base64,{font64('Poppins-Bold.ttf')}) format('truetype'); }}
"""

def e(s):
    return html.escape(str(s))

CATS = list(PACK.keys())

# ---- build category sections ----
def card_html(idx, name, vibe, items):
    rows = ""
    for brand, desc in items:
        rows += (f'<div class="item"><span class="brand">{e(brand)}</span>'
                 f'<span class="dash">—</span>'
                 f'<span class="desc">{e(desc)}</span></div>')
    return f"""
    <div class="card">
      <div class="card-head">
        <span class="num">{idx:02d}</span>
        <div class="titles">
          <div class="oname">{e(name)}</div>
          <div class="ovibe">{e(vibe)}</div>
        </div>
      </div>
      <div class="items">{rows}</div>
    </div>"""

def section_html(ci, cat, looks):
    cards = "".join(card_html(i+1, n, v, it) for i,(n,v,it) in enumerate(looks))
    return f"""
  <section class="cat">
    <div class="cat-banner">
      <div class="cat-kicker">Category {ci:02d} · 10 Looks</div>
      <h2 class="cat-title">{e(cat)}</h2>
      <div class="cat-rule"></div>
    </div>
    <div class="grid">{cards}</div>
  </section>"""

sections = "".join(section_html(i+1, c, PACK[c]) for i,c in enumerate(CATS))

# ---- table of contents ----
toc_rows = "".join(
    f'<div class="toc-row"><span class="toc-n">{i+1:02d}</span>'
    f'<span class="toc-name">{e(c)}</span><span class="toc-dots"></span>'
    f'<span class="toc-count">10 looks</span></div>'
    for i,c in enumerate(CATS))

TOTAL = sum(len(v) for v in PACK.values())

HTML = f"""<!doctype html><html><head><meta charset="utf-8"><style>
{FACES}
* {{ margin:0; padding:0; box-sizing:border-box; }}
:root {{
  --ink:#2b2430; --pink:#e23c86; --pink-deep:#c31f6b; --blush:#fbe7f0;
  --blush2:#fdeff5; --line:#f2c9dd; --soft:#8a7d86;
}}
@page {{ size:8.5in 11in; margin:0; }}
html,body {{ font-family:'Poppins',sans-serif; color:var(--ink); -webkit-print-color-adjust:exact; print-color-adjust:exact; }}

/* ---------- COVER ---------- */
.cover {{
  height:11in; width:8.5in; page-break-after:always; position:relative; overflow:hidden;
  background:
    radial-gradient(120% 80% at 50% -10%, #ffd7e8 0%, #fbe7f0 42%, #ffffff 100%);
  display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center;
}}
.cover .frame {{ position:absolute; inset:0.42in; border:1.6px solid var(--line); }}
.cover .frame2 {{ position:absolute; inset:0.52in; border:1px solid #f6dbe8; }}
.cover .script {{ font-family:'Vibes'; font-size:52px; color:var(--pink); line-height:1; margin-bottom:6px; }}
.cover h1 {{ font-family:'Playfair'; font-weight:900; font-size:62px; letter-spacing:1px; line-height:1.02; color:var(--ink); }}
.cover h1 .tm {{ font-size:20px; vertical-align:super; color:var(--pink); }}
.cover .sub {{ margin-top:20px; font-family:'Poppins'; font-weight:500; letter-spacing:5px; font-size:13px; text-transform:uppercase; color:var(--pink-deep); }}
.cover .divider {{ width:120px; height:2px; background:var(--pink); margin:26px auto; }}
.cover .meta {{ font-family:'Poppins'; font-weight:400; font-size:13px; color:var(--soft); letter-spacing:1px; line-height:2; }}
.cover .system {{ position:absolute; bottom:0.74in; left:0; right:0; font-family:'Poppins'; font-weight:600; letter-spacing:4px; font-size:11px; text-transform:uppercase; color:var(--pink); }}
.cover .badge {{ position:absolute; top:0.9in; left:0; right:0; font-family:'Vibes'; font-size:26px; color:var(--pink-deep); }}

/* ---------- TOC ---------- */
.toc {{ height:11in; width:8.5in; page-break-after:always; padding:0.95in 0.9in; position:relative; background:#fff; }}
.toc .frame {{ position:absolute; inset:0.42in; border:1.4px solid var(--line); pointer-events:none; }}
.toc .kick {{ font-family:'Poppins'; font-weight:600; letter-spacing:4px; font-size:11px; text-transform:uppercase; color:var(--pink); text-align:center; }}
.toc h2 {{ font-family:'Playfair'; font-weight:900; font-size:32px; text-align:center; margin:6px 0 2px; }}
.toc .script {{ font-family:'Vibes'; font-size:27px; color:var(--pink); text-align:center; margin-bottom:14px; }}
.toc-row {{ display:flex; align-items:baseline; padding:5.2px 4px; border-bottom:1px solid #f6e2ec; }}
.toc-n {{ font-family:'Bodoni'; font-weight:700; color:var(--pink); width:34px; font-size:15px; }}
.toc-name {{ font-family:'Poppins'; font-weight:500; font-size:14px; color:var(--ink); }}
.toc-dots {{ flex:1; border-bottom:1px dotted #e7b9d1; margin:0 8px; transform:translateY(-3px); }}
.toc-count {{ font-family:'Poppins'; font-weight:400; font-size:11px; color:var(--soft); letter-spacing:1px; }}
.toc .foot {{ position:absolute; bottom:0.5in; left:0; right:0; text-align:center; font-family:'Poppins'; font-size:10.5px; letter-spacing:2px; color:var(--soft); text-transform:uppercase; }}

/* ---------- HOW TO USE ---------- */
.intro {{ height:11in; width:8.5in; page-break-after:always; padding:1.1in 1in; position:relative; background:
  radial-gradient(120% 70% at 50% 0%, #fdeff5 0%, #ffffff 60%); }}
.intro .frame {{ position:absolute; inset:0.42in; border:1.4px solid var(--line); }}
.intro h3 {{ font-family:'Playfair'; font-weight:900; font-size:30px; margin-bottom:4px; }}
.intro .script {{ font-family:'Vibes'; font-size:28px; color:var(--pink); margin-bottom:20px; }}
.intro p {{ font-family:'Poppins'; font-weight:400; font-size:13px; line-height:1.85; color:#4a4048; margin-bottom:13px; max-width:6in; }}
.intro .legend {{ margin-top:16px; padding:18px 20px; background:var(--blush2); border:1px solid var(--line); }}
.intro .legend .lr {{ display:flex; align-items:baseline; gap:10px; margin:7px 0; font-size:12.5px; }}
.intro .legend .brand {{ font-family:'Bodoni'; font-weight:700; color:var(--pink-deep); }}
.intro .legend .k {{ font-family:'Poppins'; font-weight:600; color:var(--ink); width:96px; }}

/* ---------- CATEGORY SECTIONS ---------- */
.cat {{ page-break-before:always; padding:0.5in 0.5in 0.4in; }}
.cat-banner {{ text-align:center; margin-bottom:11px; }}
.cat-kicker {{ font-family:'Poppins'; font-weight:600; letter-spacing:4px; font-size:9px; text-transform:uppercase; color:var(--pink); }}
.cat-title {{ font-family:'Playfair'; font-weight:900; font-size:27px; margin:2px 0 5px; letter-spacing:.3px; }}
.cat-rule {{ width:66px; height:2px; background:var(--pink); margin:0 auto; }}
.grid {{ display:grid; grid-template-columns:1fr 1fr; gap:8px; }}
.card {{ border:1px solid var(--line); border-radius:8px; padding:8px 11px 9px; background:#fff;
  break-inside:avoid; box-shadow:0 1px 0 #fbe7f0; }}
.card-head {{ display:flex; align-items:center; gap:8px; padding-bottom:6px; margin-bottom:6px; border-bottom:1px solid #f6e2ec; }}
.num {{ font-family:'Bodoni'; font-weight:700; font-size:12px; color:#fff; background:var(--pink);
  width:22px; height:22px; border-radius:50%; display:flex; align-items:center; justify-content:center; flex:0 0 auto; }}
.titles {{ line-height:1.12; }}
.oname {{ font-family:'Playfair'; font-weight:700; font-size:14px; color:var(--ink); }}
.ovibe {{ font-family:'Poppins'; font-weight:400; font-style:italic; font-size:9px; color:var(--soft); }}
.items {{ display:flex; flex-direction:column; gap:3px; }}
.item {{ display:flex; align-items:baseline; gap:5px; }}
.brand {{ font-family:'Bodoni'; font-weight:700; font-size:10px; letter-spacing:.3px; color:var(--pink-deep); text-transform:uppercase; white-space:nowrap; }}
.dash {{ color:var(--line); font-size:9px; }}
.desc {{ font-family:'Poppins'; font-weight:500; font-size:10px; color:#3f3640; line-height:1.18; }}

.backcover {{ height:11in; width:8.5in; page-break-before:always; position:relative;
  background:radial-gradient(120% 80% at 50% 120%, #ffd7e8 0%, #fbe7f0 45%, #ffffff 100%);
  display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; }}
.backcover .frame {{ position:absolute; inset:0.42in; border:1.6px solid var(--line); }}
.backcover .script {{ font-family:'Vibes'; font-size:60px; color:var(--pink); }}
.backcover .tag {{ font-family:'Poppins'; font-weight:600; letter-spacing:5px; font-size:11px; text-transform:uppercase; color:var(--pink-deep); margin-top:10px; }}
</style></head><body>

<div class="cover">
  <div class="frame"></div><div class="frame2"></div>
  <div class="badge">the outfit system</div>
  <div class="script">the</div>
  <h1>FEMALE OUTFIT<br>PACK<span class="tm">™</span></h1>
  <div class="sub">Curated Style Reference</div>
  <div class="divider"></div>
  <div class="meta">21 Categories · {TOTAL} Complete Looks<br>Shop-the-look breakdowns for every occasion</div>
  <div class="system">The Outfit System™ · Female Edition</div>
</div>

<div class="toc">
  <div class="frame"></div>
  <div class="kick">Inside This Pack</div>
  <h2>Table of Contents</h2>
  <div class="script">find your vibe</div>
  {toc_rows}
  <div class="foot">{len(CATS)} Categories · {TOTAL} Looks</div>
</div>

<div class="intro">
  <div class="frame"></div>
  <h3>How To Use This Pack</h3>
  <div class="script">styled for you</div>
  <p>Every look in this pack is broken down piece-by-piece so you can shop it, recreate it, or style your character in seconds. Find the category that fits the moment, pick from ten complete looks, and build from the top down.</p>
  <p>Each item is listed as the <b>brand</b> followed by the <b>exact piece</b> — from the top layer all the way to the finishing accessory and beauty touch. Swap brands for your budget; the silhouette and styling are what make the look.</p>
  <div class="legend">
    <div class="lr"><span class="k">Format</span><span class="brand">BRAND</span><span>—</span><span>item description</span></div>
    <div class="lr"><span class="k">Order</span><span>Top → Bottom / Dress → Layer → Shoes → Bag → Accents</span></div>
    <div class="lr"><span class="k">Per look</span><span>5–6 curated pieces, styled to mix &amp; match</span></div>
  </div>
  <p style="margin-top:18px; font-size:11.5px; color:#8a7d86;">Tip: pair the flat-lay collage style of your brand with these breakdowns — each look is written to translate straight into a product grid.</p>
</div>

{sections}

<div class="backcover">
  <div class="frame"></div>
  <div class="script">stay styled</div>
  <div class="tag">The Female Outfit Pack™ · The Outfit System™</div>
</div>

</body></html>"""

out = os.path.join(HERE, "female_outfit_pack.html")
with open(out, "w", encoding="utf-8") as f:
    f.write(HTML)
print("wrote", out, len(HTML), "bytes")
