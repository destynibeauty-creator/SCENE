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
    gf = font('Poppins-ExtraBold', 470 if len(ghost) <= 2 else 300)
    dark = tuple(int(c * 0.13) for c in accent)
    d.text((60, H // 2 - gf.size // 2 - 40), ghost, font=gf, fill=dark)
    bracket(d, 40, 40, 64, 'tl', MAG)
    bracket(d, W - 40, H - 40, 64, 'br', CYAN)
    # logo
    logo = Image.open(LOGO)
    lw = 260
    lh = int(lw * logo.height / logo.width)
    img.paste(logo.resize((lw, lh), Image.LANCZOS), (W // 2 - lw // 2, 44))
    d = ImageDraw.Draw(img)
    y = 44 + lh + 42
    # kicker
    kf = font('Poppins-SemiBold', 30)
    spaced = '  '.join(kick)
    kw = d.textlength(spaced, kf)
    d.text((W // 2 - kw / 2, y), spaced, font=kf, fill=accent)
    y += 66
    # title
    size = 108 if max(len(t) for t in title_lines) <= 16 else 84
    tf = font('Poppins-ExtraBold', size)
    for ln in title_lines:
        metal_text(img, W // 2, y, ln, tf)
        y += int(tf.size * 1.14)
    d = ImageDraw.Draw(img)
    y += 16
    gradient_bar(d, W // 2, y, 340, 8, accent, MAG if accent != MAG else CYAN)
    y += 46
    df = font('Poppins-Regular', 36)
    dw = d.textlength(desc, df)
    d.text((W // 2 - dw / 2, y), desc, font=df, fill=(226, 228, 231))
    # chip bottom
    cf = font('Poppins-Bold', 34)
    pad = 44 if lock else 0
    cw = d.textlength(chip, cf) + 76 + pad
    cy = H - 108
    d.rounded_rectangle([W // 2 - cw / 2, cy, W // 2 + cw / 2, cy + 66],
                        33, outline=accent, width=3)
    tx = W // 2 - (cw - 76) / 2 + pad
    if lock:
        lx, ly = tx - 44, cy + 20
        d.arc([lx + 4, ly - 12, lx + 24, ly + 10], 180, 360, fill=accent, width=4)
        d.rounded_rectangle([lx, ly + 4, lx + 28, ly + 28], 5, fill=accent)
    d.text((tx, cy + 12), chip, font=cf, fill=accent)
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
