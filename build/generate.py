# -*- coding: utf-8 -*-
"""Render THE FEMALE OUTFIT PACK(TM) as flatlay collages -> HTML for Chromium->PDF."""
import base64, os, html
from data import PACK
from iconmap import icon_uri_for, icon_svg_for, svg_inline, tint_for

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "fonts")
PER_PAGE = 6            # flatlay tiles per category page (2 cols x 3 rows)

def font64(n):
    with open(os.path.join(FONTS, n), "rb") as f:
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

def e(s): return html.escape(str(s))
CATS = list(PACK.keys())
TOTAL = sum(len(v) for v in PACK.values())

def cell(brand, desc):
    svg = icon_svg_for(brand, desc)
    tint = tint_for(desc)
    return (f'<div class="cell">'
            f'<div class="ico" style="background:{tint}">{svg}</div>'
            f'<div class="lbl"><span class="brand">{e(brand)}</span>'
            f'<span class="desc">{e(desc)}</span></div></div>')

def tile(idx, name, vibe, items):
    cells = "".join(cell(b, d) for b, d in items)
    return (f'<div class="tile">'
            f'<div class="thead"><span class="num">{idx:02d}</span>'
            f'<div class="tt"><div class="oname">{e(name)}</div>'
            f'<div class="ovibe">{e(vibe)}</div></div></div>'
            f'<div class="flat">{cells}</div></div>')

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield i, lst[i:i+n]

def category_pages(ci, cat, looks):
    pages = ""
    parts = list(chunks(looks, PER_PAGE))
    for pno, (start, group) in enumerate(parts, 1):
        cont = f'<span class="cont"> · {pno}/{len(parts)}</span>' if len(parts) > 1 else ""
        tiles = "".join(tile(start+i+1, n, v, it) for i, (n, v, it) in enumerate(group))
        # pad to keep grid alignment on short last page
        pad = "".join('<div class="tile empty"></div>' for _ in range(PER_PAGE - len(group)))
        pages += (f'<div class="page cat">'
                  f'<div class="cat-banner"><div class="cat-kicker">Category {ci:02d} · '
                  f'10 Looks{cont}</div><h2 class="cat-title">{e(cat)}</h2>'
                  f'<div class="cat-rule"></div></div>'
                  f'<div class="grid">{tiles}{pad}</div></div>')
    return pages

sections = "".join(category_pages(i+1, c, PACK[c]) for i, c in enumerate(CATS))

toc_rows = "".join(
    f'<div class="toc-row"><span class="toc-n">{i+1:02d}</span>'
    f'<span class="toc-name">{e(c)}</span><span class="toc-dots"></span>'
    f'<span class="toc-count">10 looks</span></div>' for i, c in enumerate(CATS))

HTML = f"""<!doctype html><html><head><meta charset="utf-8"><style>
{FACES}
* {{ margin:0; padding:0; box-sizing:border-box; }}
:root {{ --ink:#2b2430; --pink:#e23c86; --pink-deep:#c31f6b; --line:#f2c9dd;
  --soft:#8a7d86; --blush:#fdeff5; --blush2:#fbe7f0; }}
@page {{ size:8.5in 11in; margin:0; }}
html,body {{ font-family:'Poppins',sans-serif; color:var(--ink);
  -webkit-print-color-adjust:exact; print-color-adjust:exact; }}
.page {{ width:8.5in; height:11in; page-break-after:always; position:relative; overflow:hidden; }}

/* COVER */
.cover {{ background:radial-gradient(120% 80% at 50% -10%, #ffd7e8 0%, #fbe7f0 42%, #fff 100%);
  display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; }}
.cover .frame {{ position:absolute; inset:0.42in; border:1.6px solid var(--line); }}
.cover .frame2 {{ position:absolute; inset:0.52in; border:1px solid #f6dbe8; }}
.cover .script {{ font-family:'Vibes'; font-size:52px; color:var(--pink); line-height:1; margin-bottom:6px; }}
.cover h1 {{ font-family:'Playfair'; font-weight:900; font-size:60px; letter-spacing:1px; line-height:1.02; }}
.cover h1 .tm {{ font-size:20px; vertical-align:super; color:var(--pink); }}
.cover .sub {{ margin-top:20px; font-weight:500; letter-spacing:5px; font-size:13px; text-transform:uppercase; color:var(--pink-deep); }}
.cover .divider {{ width:120px; height:2px; background:var(--pink); margin:26px auto; }}
.cover .meta {{ font-size:13px; color:var(--soft); letter-spacing:1px; line-height:2; }}
.cover .row {{ margin-top:22px; display:flex; gap:16px; }}
.cover .row img {{ width:44px; height:44px; }}
.cover .system {{ position:absolute; bottom:0.74in; left:0; right:0; font-weight:600; letter-spacing:4px; font-size:11px; text-transform:uppercase; color:var(--pink); }}
.cover .badge {{ position:absolute; top:0.9in; left:0; right:0; font-family:'Vibes'; font-size:26px; color:var(--pink-deep); }}

/* TOC */
.toc {{ padding:0.95in 0.9in; background:#fff; }}
.toc .frame {{ position:absolute; inset:0.42in; border:1.4px solid var(--line); }}
.toc .kick {{ font-weight:600; letter-spacing:4px; font-size:11px; text-transform:uppercase; color:var(--pink); text-align:center; }}
.toc h2 {{ font-family:'Playfair'; font-weight:900; font-size:32px; text-align:center; margin:6px 0 2px; }}
.toc .script {{ font-family:'Vibes'; font-size:27px; color:var(--pink); text-align:center; margin-bottom:14px; }}
.toc-row {{ display:flex; align-items:baseline; padding:5.2px 4px; border-bottom:1px solid #f6e2ec; }}
.toc-n {{ font-family:'Bodoni'; font-weight:700; color:var(--pink); width:34px; font-size:15px; }}
.toc-name {{ font-weight:500; font-size:14px; }}
.toc-dots {{ flex:1; border-bottom:1px dotted #e7b9d1; margin:0 8px; transform:translateY(-3px); }}
.toc-count {{ font-size:11px; color:var(--soft); letter-spacing:1px; }}
.toc .foot {{ position:absolute; bottom:0.5in; left:0; right:0; text-align:center; font-size:10.5px; letter-spacing:2px; color:var(--soft); text-transform:uppercase; }}

/* INTRO */
.intro {{ padding:1.0in 1in; background:radial-gradient(120% 70% at 50% 0%, #fdeff5 0%, #fff 60%); }}
.intro .frame {{ position:absolute; inset:0.42in; border:1.4px solid var(--line); }}
.intro h3 {{ font-family:'Playfair'; font-weight:900; font-size:30px; margin-bottom:4px; }}
.intro .script {{ font-family:'Vibes'; font-size:28px; color:var(--pink); margin-bottom:18px; }}
.intro p {{ font-weight:400; font-size:12.5px; line-height:1.8; color:#4a4048; margin-bottom:12px; max-width:6in; }}
.intro .demo {{ margin-top:14px; padding:16px 18px; background:var(--blush); border:1px solid var(--line); border-radius:10px; }}
.intro .demo .flat {{ display:grid; grid-template-columns:repeat(3,1fr); gap:8px; }}
.intro .legend {{ margin-top:16px; font-size:11.5px; color:#4a4048; line-height:1.9; }}
.intro .legend b {{ font-family:'Bodoni'; color:var(--pink-deep); }}

/* CATEGORY FLATLAY PAGES */
.cat {{ padding:0.5in 0.5in 0.4in; }}
.cat-banner {{ text-align:center; margin-bottom:12px; }}
.cat-kicker {{ font-weight:600; letter-spacing:4px; font-size:9px; text-transform:uppercase; color:var(--pink); }}
.cont {{ color:var(--soft); letter-spacing:2px; }}
.cat-title {{ font-family:'Playfair'; font-weight:900; font-size:27px; margin:2px 0 5px; }}
.cat-rule {{ width:66px; height:2px; background:var(--pink); margin:0 auto; }}
.grid {{ display:grid; grid-template-columns:1fr 1fr; grid-auto-rows:1fr; gap:10px; height:9.35in; }}
.tile {{ border:1px solid var(--line); border-radius:11px; background:#fff; padding:9px 10px 6px;
  box-shadow:0 1px 0 #fbe7f0; display:flex; flex-direction:column; overflow:hidden; }}
.tile.empty {{ border:none; background:transparent; box-shadow:none; }}
.thead {{ display:flex; align-items:center; gap:8px; padding-bottom:6px; margin-bottom:5px; border-bottom:1px solid #f6e2ec; }}
.num {{ font-family:'Bodoni'; font-weight:700; font-size:12px; color:#fff; background:var(--pink);
  width:22px; height:22px; border-radius:50%; display:flex; align-items:center; justify-content:center; flex:0 0 auto; }}
.oname {{ font-family:'Playfair'; font-weight:700; font-size:14px; line-height:1.05; }}
.ovibe {{ font-style:italic; font-weight:400; font-size:8.5px; color:var(--soft); }}
.flat {{ flex:1; display:grid; grid-template-columns:repeat(3,1fr); grid-auto-rows:1fr; gap:4px;
  background:var(--blush); border-radius:8px; padding:7px 5px; }}
.cell {{ display:flex; flex-direction:column; align-items:center; text-align:center; justify-content:flex-start; }}
.ico {{ width:54px; height:50px; border-radius:13px; display:flex; align-items:center; justify-content:center; }}
.ico .ic {{ height:40px; width:40px; filter:drop-shadow(0 1px 1px rgba(120,90,110,.16)); }}
.cover .row .ic {{ width:44px; height:44px; }}
.intro .demo .ic {{ height:40px; width:40px; }}
.lbl {{ margin-top:2px; line-height:1.08; }}
.brand {{ display:block; font-family:'Bodoni'; font-weight:700; font-size:8px; letter-spacing:.2px; color:var(--pink-deep); text-transform:uppercase; }}
.desc {{ display:block; font-weight:500; font-size:7px; color:#4a4048; }}

/* BACK */
.backcover {{ background:radial-gradient(120% 80% at 50% 120%, #ffd7e8 0%, #fbe7f0 45%, #fff 100%);
  display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; page-break-after:auto; }}
.backcover .frame {{ position:absolute; inset:0.42in; border:1.6px solid var(--line); }}
.backcover .script {{ font-family:'Vibes'; font-size:60px; color:var(--pink); }}
.backcover .tag {{ font-weight:600; letter-spacing:5px; font-size:11px; text-transform:uppercase; color:var(--pink-deep); margin-top:10px; }}
</style></head><body>

<div class="page cover">
  <div class="frame"></div><div class="frame2"></div>
  <div class="badge">the outfit system</div>
  <div class="script">the</div>
  <h1>FEMALE OUTFIT<br>PACK<span class="tm">™</span></h1>
  <div class="sub">Curated Flatlay Lookbook</div>
  <div class="divider"></div>
  <div class="meta">21 Categories · {TOTAL} Complete Looks<br>Every outfit styled &amp; broken down piece-by-piece</div>
  <div class="row">
    {svg_inline('dress')}{svg_inline('handbag')}{svg_inline('high-heeled-shoe')}{svg_inline('sunglasses')}{svg_inline('lipstick')}
  </div>
  <div class="system">The Outfit System™ · Female Edition</div>
</div>

<div class="page toc">
  <div class="frame"></div>
  <div class="kick">Inside This Pack</div>
  <h2>Table of Contents</h2>
  <div class="script">find your vibe</div>
  {toc_rows}
  <div class="foot">{len(CATS)} Categories · {TOTAL} Looks</div>
</div>

<div class="page intro">
  <div class="frame"></div>
  <h3>How To Use This Pack</h3>
  <div class="script">styled for you</div>
  <p>Every look is presented as a <b>flatlay</b> — the pieces laid out and labeled so you can see the whole outfit at a glance, then shop it or recreate it. Find your category, pick from ten looks, and build from the top down.</p>
  <p>Each piece shows its <b>brand</b> and the <b>exact item</b>, ordered top → bottom / dress → layer → shoes → bag → accents. Swap brands for your budget; the silhouette and styling are what make the look.</p>
  <div class="demo">
    <div class="flat" style="background:#fff;border:1px solid #f2c9dd;border-radius:8px;padding:10px;">
      <div class="cell"><div class="ico">{svg_inline('coat')}</div><div class="lbl"><span class="brand">Layer</span><span class="desc">cardigan / coat</span></div></div>
      <div class="cell"><div class="ico">{svg_inline('womans-clothes')}</div><div class="lbl"><span class="brand">Top</span><span class="desc">tank / bodysuit</span></div></div>
      <div class="cell"><div class="ico">{svg_inline('jeans')}</div><div class="lbl"><span class="brand">Bottom</span><span class="desc">legging / trouser</span></div></div>
      <div class="cell"><div class="ico">{svg_inline('running-shoe')}</div><div class="lbl"><span class="brand">Shoes</span><span class="desc">sneaker / heel</span></div></div>
      <div class="cell"><div class="ico">{svg_inline('shopping-bags')}</div><div class="lbl"><span class="brand">Bag</span><span class="desc">tote / clutch</span></div></div>
      <div class="cell"><div class="ico">{svg_inline('lipstick')}</div><div class="lbl"><span class="brand">Accent</span><span class="desc">beauty / jewelry</span></div></div>
    </div>
  </div>
  <div class="legend"><b>Note on the art:</b> icons are open-licensed (Microsoft Fluent Emoji, MIT) so this pack is free to share and sell. Drop in your own product photos to turn any look into a photographic flatlay.</div>
</div>

{sections}

<div class="page backcover">
  <div class="frame"></div>
  <div class="script">stay styled</div>
  <div class="tag">The Female Outfit Pack™ · The Outfit System™</div>
</div>

</body></html>"""

out = os.path.join(HERE, "female_outfit_pack.html")
with open(out, "w", encoding="utf-8") as f:
    f.write(HTML)
print("wrote", out, round(len(HTML)/1024), "KB")
