#!/usr/bin/env python3
"""Branded 1080x1080 Stan store thumbnails for the SCENE AI product ladder."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import pypdfium2 as pdfium

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FONTS = os.path.join(ROOT, 'build', 'fonts')
LOGO = os.path.join(ROOT, 'build', 'assets', 'logo-lockup.jpg')

CYAN = (0, 229, 255); MAG = (246, 0, 162); LIME = (198, 255, 0)
SILVER = (192, 195, 199); MUT = (138, 143, 152); WHITE = (247, 247, 245)


def font(name, size):
    return ImageFont.truetype(os.path.join(FONTS, f'{name}.ttf'), size)


def bracket(d, x, y, s, corner, color, w=9):
    if corner == 'tl':
        d.line([(x, y + s), (x, y), (x + s, y)], fill=color, width=w)
    else:
        d.line([(x, y - s), (x, y), (x - s, y)], fill=color, width=w)


def metal_text(canvas, cx, top, text, f):
    """Vertical silver-gradient text via mask."""
    d = ImageDraw.Draw(canvas)
    w = int(d.textlength(text, f))
    h = sum(f.getmetrics())
    mask = Image.new('L', (w + 20, h + 20), 0)
    ImageDraw.Draw(mask).text((10, 10), text, font=f, fill=255)
    grad = Image.new('RGB', mask.size)
    gd = ImageDraw.Draw(grad)
    for y in range(mask.size[1]):
        t = y / mask.size[1]
        c = tuple(int(a + (b - a) * t) for a, b in
                  zip((250, 251, 253), (143, 147, 153)))
        gd.line([(0, y), (mask.size[0], y)], fill=c)
    canvas.paste(grad, (int(cx - mask.size[0] / 2), top - 10), mask)


def gradient_bar(d, cx, y, w, h, c1, c2):
    for x in range(w):
        t = x / w
        c = tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))
        d.rectangle([cx - w // 2 + x, y, cx - w // 2 + x + 1, y + h], fill=c)


def base_card(accent, ghost):
    img = Image.new('RGB', (1080, 1080), (0, 0, 0))
    d = ImageDraw.Draw(img)
    # ghost glyph
    gf = font('Poppins-ExtraBold', 620 if len(ghost) <= 2 else 430)
    gw = d.textlength(ghost, gf)
    dark = tuple(int(c * 0.13) for c in accent)
    d.text((540 - gw / 2, 210), ghost, font=gf, fill=dark)
    bracket(d, 44, 44, 74, 'tl', MAG)
    bracket(d, 1036, 1036, 74, 'br', CYAN)
    return img, d


def add_logo(img, cx=540, top=64, width=360):
    logo = Image.open(LOGO)
    lh = int(width * logo.height / logo.width)
    img.paste(logo.resize((width, lh), Image.LANCZOS), (cx - width // 2, top))
    return top + lh


def chipline(d, cx, y, text, color):
    f = font('Poppins-SemiBold', 30)
    w = d.textlength(text, f)
    d.text((cx - w / 2, y), text, font=f, fill=color)


def kicker(d, cx, y, text, color):
    f = font('Poppins-SemiBold', 34)
    spaced = '  '.join(text)
    w = d.textlength(spaced, f)
    d.text((cx - w / 2, y), spaced, font=f, fill=color)


def badge(d, cx, y, text, bg):
    f = font('Poppins-Bold', 40)
    w = d.textlength(text, f) + 70
    d.rounded_rectangle([cx - w / 2, y, cx + w / 2, y + 74], 37, fill=bg)
    d.text((cx - (w - 70) / 2, y + 12), text, font=f, fill=(0, 0, 0))


def card(fname, accent, ghost, kick, title_lines, desc, chips, badge_txt=None):
    img, d = base_card(accent, ghost)
    add_logo(img)
    d = ImageDraw.Draw(img)
    y = 330
    if badge_txt:
        badge(d, 540, y, badge_txt, accent)
        y += 120
    kicker(d, 540, y, kick, accent)
    y += 76
    tf = font('Poppins-ExtraBold', 96 if max(len(t) for t in title_lines) <= 16 else 76)
    for ln in title_lines:
        metal_text(img, 540, y, ln, tf)
        y += int(tf.size * 1.16)
    d = ImageDraw.Draw(img)
    y += 18
    gradient_bar(d, 540, y, 300, 8, accent, MAG if accent != MAG else CYAN)
    y += 52
    df = font('Poppins-Regular', 38)
    w = d.textlength(desc, df)
    d.text((540 - w / 2, y), desc, font=df, fill=(226, 228, 231))
    chipline(d, 540, 975, chips, accent)
    img.save(os.path.join(HERE, fname))
    print('wrote', fname)


# 1 · FREE starter drop
card('thumb-free-starter-1080.png', LIME, '1H', 'THE STARTER DROP',
     ['YOUR FIRST', 'AI CHARACTER'], 'One prompt. One hook. One pinned comment.',
     'COMMENT  SCENE  TO GET IT', badge_txt='FREE')

# 2 · $17 mini pack
card('thumb-mini-pack-1080.png', CYAN, '20', 'THE MINI-PACK',
     ['IDENTITY LOCK', 'MINI-PACK'], 'Same face. Every photo. 20 prompts.',
     'HIM + HER  ·  COPY-PASTE')

# 3 · THE SCENE AI membership
card('thumb-scene-society-1080.png', MAG, 'S', 'THE MEMBERSHIP',
     ['THE SCENE', 'AI'], 'New scenes, packs and drops every month.',
     'MONTHLY  ·  COMMUNITY  ·  FIRST ACCESS')

# 4 · SCENE Studio bonus
card('thumb-scene-studio-1080.png', CYAN, '</>', 'INCLUDED WITH THE OS',
     ['SCENE', 'STUDIO'], 'Answer the questions. It writes your prompts.',
     'PROMPT BUILDER  ·  HIM + HER', badge_txt='BONUS')

# 5 · Female Outfit Pack (real cover art, framed on brand black)
img = Image.new('RGB', (1080, 1080), (0, 0, 0))
d = ImageDraw.Draw(img)
bracket(d, 44, 44, 74, 'tl', MAG)
bracket(d, 1036, 1036, 74, 'br', CYAN)
cov = pdfium.PdfDocument(os.path.join(ROOT, '..', 'The-Female-Outfit-Pack.pdf'))[0] \
    .render(scale=1.5).to_pil().convert('RGB')
cov.thumbnail((470, 610))
t = cov.rotate(-5, expand=True, resample=Image.BICUBIC, fillcolor=(0, 0, 0))
bordered = Image.new('RGB', (t.width + 6, t.height + 6), (35, 35, 43))
bordered.paste(t, (3, 3))
sh = Image.new('RGBA', (bordered.width + 80, bordered.height + 80), (0, 0, 0, 0))
ImageDraw.Draw(sh).rectangle([40, 40, 40 + bordered.width, 40 + bordered.height],
                             fill=(246, 0, 162, 70))
sh = sh.filter(ImageFilter.GaussianBlur(30))
img.paste(Image.alpha_composite(Image.new('RGBA', sh.size, (0, 0, 0, 255)),
          sh).convert('RGB'), (540 - sh.width // 2, 150), None)
img.paste(bordered, (540 - bordered.width // 2, 190))
add_logo(img, 540, 44, 300)
d = ImageDraw.Draw(img)
tf = font('Poppins-ExtraBold', 66)
metal_text(img, 540, 880, 'THE FEMALE OUTFIT PACK', tf)
d = ImageDraw.Draw(img)
chipline(d, 540, 985, '210 LOOKS  ·  21 CATEGORIES  ·  SHOPPABLE', MAG)
img.save(os.path.join(HERE, 'thumb-outfit-pack-1080.png'))
print('wrote thumb-outfit-pack-1080.png')
