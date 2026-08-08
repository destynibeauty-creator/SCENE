#!/usr/bin/env python3
"""Branded 1460x752 Skool classroom section covers (Skool's recommended size)."""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FONTS = os.path.join(ROOT, 'build', 'fonts')
LOGO = os.path.join(ROOT, 'build', 'assets', 'logo-lockup.jpg')
OUT = os.path.join(HERE, 'classroom')

CYAN = (0, 229, 255); MAG = (246, 0, 162); LIME = (198, 255, 0)
SILVER = (192, 195, 199); WHITE = (247, 247, 245)
W, H = 1460, 752


def font(name, size):
    return ImageFont.truetype(os.path.join(FONTS, f'{name}.ttf'), size)


def bracket(d, x, y, s, corner, color, w=8):
    if corner == 'tl':
        d.line([(x, y + s), (x, y), (x + s, y)], fill=color, width=w)
    else:
        d.line([(x, y - s), (x, y), (x - s, y)], fill=color, width=w)


def metal_text(canvas, cx, top, text, f):
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


def cover(fname, accent, ghost, kick, title_lines, desc, chip, lock=False):
    img = Image.new('RGB', (W, H), (0, 0, 0))
    d = ImageDraw.Draw(img)
    # ghost glyph, off-center left
    gf = font('Poppins-ExtraBold', 430 if len(ghost) <= 2 else 280)
    dark = tuple(int(c * 0.13) for c in accent)
    d.text((80, H // 2 - gf.size // 2 - 30), ghost, font=gf, fill=dark)
    # brackets pulled inside the mobile-safe zone
    bracket(d, 84, 84, 54, 'tl', MAG)
    bracket(d, W - 84, H - 84, 54, 'br', CYAN)
    # logo
    logo = Image.open(LOGO)
    lw = 225
    lh = int(lw * logo.height / logo.width)
    img.paste(logo.resize((lw, lh), Image.LANCZOS), (W // 2 - lw // 2, 62))
    d = ImageDraw.Draw(img)
    y = 62 + lh + 30
    # kicker
    kf = font('Poppins-SemiBold', 27)
    spaced = '  '.join(kick)
    kw = d.textlength(spaced, kf)
    d.text((W // 2 - kw / 2, y), spaced, font=kf, fill=accent)
    y += 56
    # title
    size = 100 if max(len(t) for t in title_lines) <= 16 else 78
    tf = font('Poppins-ExtraBold', size)
    for ln in title_lines:
        metal_text(img, W // 2, y, ln, tf)
        y += int(tf.size * 1.1)
    d = ImageDraw.Draw(img)
    y += 12
    gradient_bar(d, W // 2, y, 320, 7, accent, MAG if accent != MAG else CYAN)
    y += 38
    df = font('Poppins-Regular', 33)
    dw = d.textlength(desc, df)
    d.text((W // 2 - dw / 2, y), desc, font=df, fill=(226, 228, 231))
    # chip fully inside the safe zone
    cf = font('Poppins-Bold', 31)
    pad = 40 if lock else 0
    cw = d.textlength(chip, cf) + 70 + pad
    cy = H - 156
    d.rounded_rectangle([W // 2 - cw / 2, cy, W // 2 + cw / 2, cy + 60],
                        30, outline=accent, width=3)
    tx = W // 2 - (cw - 70) / 2 + pad
    if lock:
        lx, ly = tx - 40, cy + 17
        d.arc([lx + 3, ly - 10, lx + 21, ly + 9], 180, 360, fill=accent, width=4)
        d.rounded_rectangle([lx, ly + 3, lx + 25, ly + 25], 4, fill=accent)
    d.text((tx, cy + 11), chip, font=cf, fill=accent)
    os.makedirs(OUT, exist_ok=True)
    img.save(os.path.join(OUT, fname))
    print('wrote', fname)

cover('cover-01-start-here.png', LIME, '01', 'SECTION ONE',
      ['START HERE'], 'Your first locked character, today. Free.',
      'DO THIS FIRST')

cover('cover-02-build-your-character.png', CYAN, '02', 'SECTION TWO',
      ['BUILD YOUR', 'CHARACTER'], 'The road map + the core modules.',
      'INCLUDED WITH YOUR $9')

cover('cover-03-world-builder.png', MAG, '03', 'SECTION THREE',
      ['THE WORLD', 'BUILDER'], 'Styling · continuity · camera · realism · the vault.',
      'UNLOCK · $97 ONE-TIME', lock=True)

cover('cover-04-monthly-drops.png', CYAN, '04', 'SECTION FOUR',
      ['MONTHLY', 'DROPS'], '30 scenes. 10 looks. One master scene. Every month.',
      'DROP 001 IS LIVE')

cover('cover-05-work-with-me.png', SILVER, '05', 'SECTION FIVE',
      ['WORK', 'WITH ME'], "Don't want to build? I build & direct it for you.",
      'DONE FOR YOU')
