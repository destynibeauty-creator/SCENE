#!/usr/bin/env python3
"""
THE SCENE AI — Creator OS
Rebuilds the master bundle as separately branded PDFs matching the
SCENE AI brand kit: jet black, metallic silver, electric cyan #00E5FF,
vibrant magenta #F600A2, Poppins typography, corner-bracket motif.
"""
import json
import os
import re
import sys

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, Flowable, Frame, KeepTogether, NextPageTemplate,
    PageBreak, PageTemplate, Paragraph, Spacer, Table, TableStyle,
)

HERE = os.path.dirname(os.path.abspath(__file__))
FONTDIR = os.path.join(HERE, 'fonts')
OUTDIR = os.path.normpath(os.path.join(HERE, '..', 'pdfs'))
CONTENT = os.path.join(HERE, 'content.json')
LOGO = os.path.join(HERE, 'assets', 'logo-lockup.jpg')

# ----- brand palette -----
JET = HexColor('#000000')
CHARCOAL = HexColor('#0F0F12')
PANEL = HexColor('#0C0C11')
PANEL_EDGE = HexColor('#23232B')
SILVER = HexColor('#C0C3C7')
WHITE = HexColor('#F7F7F5')
CYAN = HexColor('#00E5FF')
MAGENTA = HexColor('#F600A2')
LIME = HexColor('#C6FF00')
BODY_TX = HexColor('#D9DBDE')
MUTED = HexColor('#83878F')
RULE = HexColor('#1B1B21')

PAGE_W, PAGE_H = letter
MARGIN = 0.82 * inch
AVAIL = PAGE_W - 2 * MARGIN

# one signature color per section — BRAND COLORS ONLY, rotating through the
# kit: Electric Cyan, Vibrant Magenta, Acid Lime, Metallic Silver
BRAND_CYCLE = ['#00E5FF', '#F600A2', '#C6FF00', '#C0C3C7']
DOC_ORDER = ['START HERE', 'MODULE 01', 'MODULE 02', 'MODULE 03', 'MODULE 04',
             'MODULE 05', 'MODULE 06', 'MODULE 07', 'MODULE 08', 'MODULE 09A',
             'MODULE 09B', 'MODULE 10A', 'MODULE 10B', 'MODULE 11', 'MODULE 12',
             'BONUS 01', 'BONUS 02', 'BONUS 03', 'BONUS 04']
DOC_ACCENT = {d: BRAND_CYCLE[i % 4] for i, d in enumerate(DOC_ORDER)}


def blend_black(hexcolor, frac):
    """Mix a hex color toward black; frac is how much color survives."""
    r = int(hexcolor[1:3], 16) * frac
    g = int(hexcolor[3:5], 16) * frac
    b = int(hexcolor[5:7], 16) * frac
    return HexColor(f'#{int(r):02X}{int(g):02X}{int(b):02X}')

FONTS = {
    'P': 'Poppins-Regular', 'P-M': 'Poppins-Medium', 'P-SB': 'Poppins-SemiBold',
    'P-B': 'Poppins-Bold', 'P-XB': 'Poppins-ExtraBold', 'P-I': 'Poppins-Italic',
    'MONO': 'JetBrainsMono', 'MONO-B': 'JetBrainsMono-Bold',
}


def register_fonts():
    m = {
        'Poppins-Regular': 'Poppins-Regular.ttf',
        'Poppins-Medium': 'Poppins-Medium.ttf',
        'Poppins-SemiBold': 'Poppins-SemiBold.ttf',
        'Poppins-Bold': 'Poppins-Bold.ttf',
        'Poppins-ExtraBold': 'Poppins-ExtraBold.ttf',
        'Poppins-Italic': 'Poppins-Italic.ttf',
        'JetBrainsMono': 'JetBrainsMono-1.ttf',
        'JetBrainsMono-Bold': 'JetBrainsMono-2.ttf',
        'NotoEmoji': 'NotoEmoji.ttf',
    }
    for name, fn in m.items():
        pdfmetrics.registerFont(TTFont(name, os.path.join(FONTDIR, fn)))


EMOJI_RE = re.compile(r'([\U0001F000-\U0001FAFF☀-➿]+)')


def esc(t):
    t = t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    return EMOJI_RE.sub(r'<font name="NotoEmoji">\1</font>', t)


# ---------------------------------------------------------------- drawing

def bracket(c, x, y, size, corner, color, weight=2.4):
    """Draw an L corner bracket. corner: tl, tr, bl, br. (x,y)=corner point."""
    c.saveState()
    c.setStrokeColor(color)
    c.setLineWidth(weight)
    c.setLineCap(0)
    s = size
    if corner == 'tl':
        c.line(x, y, x + s, y); c.line(x, y, x, y - s)
    elif corner == 'tr':
        c.line(x, y, x - s, y); c.line(x, y, x, y - s)
    elif corner == 'bl':
        c.line(x, y, x + s, y); c.line(x, y, x, y + s)
    elif corner == 'br':
        c.line(x, y, x - s, y); c.line(x, y, x, y + s)
    c.restoreState()


def gradient_bar(c, x, y, w, h):
    c.saveState()
    p = c.beginPath()
    p.rect(x, y, w, h)
    c.clipPath(p, stroke=0, fill=0)
    c.linearGradient(x, y, x + w, y, (CYAN, MAGENTA), extend=False)
    c.restoreState()


def tracked(c, x, y, text, font, size, color, track=1.6, center_at=None):
    c.saveState()  # Tc is graphics state: must not leak into later text
    c.setFont(font, size)
    c.setFillColor(color)
    if center_at is not None:
        w = pdfmetrics.stringWidth(text, font, size) + track * max(len(text) - 1, 0)
        x = center_at - w / 2
    tx = c.beginText(x, y)
    tx.setCharSpace(track)
    tx.textOut(text)
    c.drawText(tx)
    c.restoreState()
    return x


def metal_text(c, cx, y, text, font, size, horiz_scale=93, slant=0.14):
    """Brand headline treatment: condensed, oblique, brushed-silver gradient
    (clip text, then paint a vertical metallic gradient through it)."""
    w = pdfmetrics.stringWidth(text, font, size) * horiz_scale / 100.0
    c.saveState()
    c.translate(cx - w / 2, y)
    c.transform(1, 0, slant, 1, 0, 0)
    t = c.beginText(0, 0)
    t.setTextRenderMode(7)  # add glyph outlines to clipping path
    t.setFont(font, size)
    t.setHorizScale(horiz_scale)
    t.textOut(text)
    c.drawText(t)
    c.linearGradient(0, -size * 0.05, 0, size * 0.78,
                     (HexColor('#8F9399'), HexColor('#FBFCFD')), extend=True)
    c.restoreState()
    return w


def wordmark(c, cx, y, scale=1.0):
    """Mini brand wordmark: THE SCENE AI with cyan/magenta AI."""
    s_the, s_main = 7 * scale, 21 * scale
    f_main = FONTS['P-XB']
    w_scene = pdfmetrics.stringWidth('SCENE', f_main, s_main)
    w_ai = pdfmetrics.stringWidth('AI', f_main, s_main)
    gap = 6 * scale
    total = w_scene + gap + w_ai
    x0 = cx - total / 2
    tracked(c, x0, y + s_main + 4 * scale, 'T H E', FONTS['P-SB'], s_the, WHITE, 2.5 * scale)
    c.setFont(f_main, s_main)
    c.setFillColor(WHITE)
    c.drawString(x0, y, 'SCENE')
    c.setFillColor(CYAN)
    c.drawString(x0 + w_scene + gap, y, 'A')
    c.setFillColor(MAGENTA)
    wA = pdfmetrics.stringWidth('A', f_main, s_main)
    c.drawString(x0 + w_scene + gap + wA, y, 'I')
    bs = 9 * scale
    bracket(c, x0 - 8 * scale, y + s_main + 10 * scale, bs, 'tl', MAGENTA, 1.6 * scale)
    bracket(c, x0 + total + 8 * scale, y - 6 * scale, bs, 'br', CYAN, 1.6 * scale)


# ---------------------------------------------------------------- flowables

class AccentHeading(Flowable):
    """H2 — white Poppins Bold with a section-color accent bar."""

    def __init__(self, text, accent=CYAN, width=AVAIL):
        super().__init__()
        self.text = text
        self.accent = accent
        self.width = width
        self.font, self.size, self.leading = FONTS['P-B'], 18, 22.5
        self.space_before, self.space_after = 0, 0

    def wrap(self, aw, ah):
        # naive wrap into lines
        words = self.text.split()
        lines, cur = [], ''
        maxw = self.width - 14
        for w in words:
            t = (cur + ' ' + w).strip()
            if pdfmetrics.stringWidth(t, self.font, self.size) <= maxw:
                cur = t
            else:
                lines.append(cur); cur = w
        if cur:
            lines.append(cur)
        self.lines = lines
        self.height = len(lines) * self.leading + 2
        return self.width, self.height

    def draw(self):
        c = self.canv
        c.setFillColor(self.accent)
        c.rect(0, 0, 3.5, self.height - 3, stroke=0, fill=1)
        c.setFillColor(WHITE)
        c.setFont(self.font, self.size)
        y = self.height - self.leading + 3
        for ln in self.lines:
            c.drawString(12, y, ln)
            y -= self.leading


class PanelLabel(Flowable):
    """Small tracked cyan mono label used above prompt panels."""

    def __init__(self, text='COPY + PASTE PROMPT'):
        super().__init__()
        self.text = text
        self.height = 13
        self.width = AVAIL

    def wrap(self, aw, ah):
        return self.width, self.height

    def draw(self):
        c = self.canv
        c.setFillColor(MAGENTA)
        c.rect(0, 3, 6, 6, stroke=0, fill=1)
        tracked(c, 13, 3, self.text, FONTS['MONO'], 7.6,
                HexColor('#B9BDC4'), 1.4)


class SystemMap(Flowable):
    """Full road map: 9 numbered steps with arrows, START and POST pins."""

    STEPS = [
        ('1', 'CHARACTER FIRST', 'Pick who your audience will follow.', 'MODULE 01'),
        ('2', 'PROMPT PACK', 'Make your MASTER face and DNA photos.', 'MODULE 02'),
        ('3', 'OUTFIT + HAIR', 'Pick the look for this episode.', 'MODULES 09 + 10'),
        ('4', 'REFERENCE BLUEPRINT', 'Give every photo you upload one job.', 'MODULE 04'),
        ('5', 'THE SCENE METHOD', 'Direct the scene: story, cast, place.', 'MODULE 03'),
        ('6', 'CONTINUITY SYSTEM', 'Make Part 2 match Part 1.', 'MODULE 05'),
        ('7', 'CAMERA BIBLE', 'Put the camera in a spot that makes sense.', 'MODULE 07'),
        ('8', 'REALISM CHECK', 'Catch anything that looks fake.', 'MODULE 08'),
        ('9', 'GENERATE + POST + REVIEW', 'Post it. See what works. Repeat.', 'MODULES 06 + 12'),
    ]
    ROW, GAP = 46, 13

    def wrap(self, aw, ah):
        self.width = AVAIL
        self.height = 30 + len(self.STEPS) * self.ROW + \
            (len(self.STEPS) - 1) * self.GAP + 40
        return self.width, self.height

    def _chip(self, c, cx, cy, text, bg):
        w = pdfmetrics.stringWidth(text, FONTS['P-B'], 8.5) + 3.2 * len(text) + 20
        c.setFillColor(bg)
        c.roundRect(cx - w / 2, cy, w, 18, 9, stroke=0, fill=1)
        c.setFillColor(JET)
        tracked(c, 0, cy + 5.5, text, FONTS['P-B'], 8.5, JET, 1.6, center_at=cx)

    def draw(self):
        c = self.canv
        cycle = [CYAN, MAGENTA, LIME]
        bx, bw = 24, self.width - 48
        chip_cx = bx + 30
        y = self.height - 30
        self._chip(c, self.width / 2, y + 6, 'START HERE', LIME)
        for i, (n, name, desc, ref) in enumerate(self.STEPS):
            col = cycle[i % 3]
            top = y - i * (self.ROW + self.GAP)
            # connector arrow from previous
            if i > 0:
                ay = top + self.GAP
                c.setStrokeColor(HexColor('#3A3A44'))
                c.setLineWidth(1.4)
                c.line(chip_cx, ay + self.GAP - 2, chip_cx, ay - 8)
                c.setFillColor(HexColor('#3A3A44'))
                p = c.beginPath()
                p.moveTo(chip_cx - 4, ay - 7)
                p.lineTo(chip_cx + 4, ay - 7)
                p.lineTo(chip_cx, ay - 13)
                p.close()
                c.drawPath(p, stroke=0, fill=1)
            box_y = top - self.ROW
            c.setFillColor(HexColor('#0C0C11'))
            c.setStrokeColor(HexColor('#26262E'))
            c.setLineWidth(0.7)
            c.roundRect(bx, box_y, bw, self.ROW, 6, stroke=1, fill=1)
            c.setFillColor(col)
            c.rect(bx, box_y, 3, self.ROW, stroke=0, fill=1)
            # number chip
            c.setFillColor(col)
            c.circle(chip_cx, box_y + self.ROW / 2, 11, stroke=0, fill=1)
            c.setFillColor(JET)
            c.setFont(FONTS['P-XB'], 12)
            c.drawCentredString(chip_cx, box_y + self.ROW / 2 - 4.2, n)
            # text
            c.setFillColor(WHITE)
            c.setFont(FONTS['P-B'], 11.5)
            c.drawString(chip_cx + 24, box_y + self.ROW - 20, name)
            c.setFillColor(HexColor('#B9BDC4'))
            c.setFont(FONTS['P'], 9.5)
            c.drawString(chip_cx + 24, box_y + 8, desc)
            tracked(c, 0, box_y + self.ROW - 19, ref, FONTS['MONO'], 7, col,
                    1.2, center_at=bx + bw - 52)
        self._chip(c, self.width / 2, 2, 'POST IT', MAGENTA)


class MethodFlow(Flowable):
    """The SCENE Method: 5 blocks with arrows, left to right."""

    PARTS = ['STORY', 'CAST', 'ENVIRONMENT', 'NOW BUILD', 'END STAMP']

    def wrap(self, aw, ah):
        self.width = AVAIL
        self.height = 74
        return self.width, self.height

    def draw(self):
        c = self.canv
        cycle = [CYAN, MAGENTA, LIME, CYAN, MAGENTA]
        n = len(self.PARTS)
        arrow = 12
        bw = (self.width - arrow * (n - 1)) / n
        bh = 46
        y = 12
        for i, name in enumerate(self.PARTS):
            x = i * (bw + arrow)
            col = cycle[i]
            c.setFillColor(HexColor('#0C0C11'))
            c.setStrokeColor(col)
            c.setLineWidth(1)
            c.roundRect(x, y, bw, bh, 6, stroke=1, fill=1)
            c.setFillColor(col)
            c.setFont(FONTS['P-XB'], 10)
            c.drawCentredString(x + bw / 2, y + bh - 18, str(i + 1))
            c.setFillColor(WHITE)
            size = 8 if len(name) > 9 else 9
            c.setFont(FONTS['P-B'], size)
            c.drawCentredString(x + bw / 2, y + 9, name)
            if i < n - 1:
                ax = x + bw + arrow / 2
                c.setFillColor(HexColor('#4A4A55'))
                p = c.beginPath()
                p.moveTo(ax - 3.5, y + bh / 2 + 4.5)
                p.lineTo(ax - 3.5, y + bh / 2 - 4.5)
                p.lineTo(ax + 4, y + bh / 2)
                p.close()
                c.drawPath(p, stroke=0, fill=1)
        c.setFillColor(HexColor('#9AA0A8'))
        c.setFont(FONTS['P'], 8.5)
        c.drawCentredString(self.width / 2, 0, 'Do the five parts in this order, every episode.')


class StepFlow(Flowable):
    """Generic numbered-box arrow flow (left to right) with a caption."""

    def __init__(self, steps, caption=''):
        super().__init__()
        self.steps = steps          # list of [number, title]
        self.caption = caption

    def wrap(self, aw, ah):
        self.width = AVAIL
        self.height = 74 if self.caption else 62
        return self.width, self.height

    def draw(self):
        c = self.canv
        cycle = [CYAN, MAGENTA, LIME, CYAN, MAGENTA]
        n = len(self.steps)
        arrow = 14
        bw = (self.width - arrow * (n - 1)) / n
        bh = 46
        y = self.height - 46 - 12
        for i, (num, name) in enumerate(self.steps):
            x = i * (bw + arrow)
            col = cycle[i % len(cycle)]
            c.setFillColor(HexColor('#0C0C11'))
            c.setStrokeColor(col)
            c.setLineWidth(1)
            c.roundRect(x, y, bw, bh, 6, stroke=1, fill=1)
            c.setFillColor(col)
            c.setFont(FONTS['P-XB'], 10)
            c.drawCentredString(x + bw / 2, y + bh - 18, str(num))
            c.setFillColor(WHITE)
            words = name.split()
            if len(words) > 2 or pdfmetrics.stringWidth(name, FONTS['P-B'], 9) > bw - 8:
                half = (len(words) + 1) // 2
                l1, l2 = ' '.join(words[:half]), ' '.join(words[half:])
                c.setFont(FONTS['P-B'], 7.5)
                c.drawCentredString(x + bw / 2, y + 15, l1)
                c.drawCentredString(x + bw / 2, y + 6, l2)
            else:
                c.setFont(FONTS['P-B'], 9)
                c.drawCentredString(x + bw / 2, y + 9, name)
            if i < n - 1:
                ax = x + bw + arrow / 2
                c.setFillColor(HexColor('#4A4A55'))
                p = c.beginPath()
                p.moveTo(ax - 4, y + bh / 2 + 5)
                p.lineTo(ax - 4, y + bh / 2 - 5)
                p.lineTo(ax + 4.5, y + bh / 2)
                p.close()
                c.drawPath(p, stroke=0, fill=1)
        if self.caption:
            c.setFillColor(HexColor('#9AA0A8'))
            c.setFont(FONTS['P'], 8.5)
            c.drawCentredString(self.width / 2, 0, self.caption)


class CommentCard(Flowable):
    """A pinned-comment mockup that looks like a social comment."""

    def __init__(self, note, text, accent):
        super().__init__()
        self.note = note
        self.text = text
        self.accent = accent

    def wrap(self, aw, ah):
        from reportlab.lib.utils import simpleSplit
        self.width = AVAIL
        self.tlines = simpleSplit(self.text, FONTS['P-M'], 11, self.width - 96)
        self.card_h = max(26 + len(self.tlines) * 15 + 12, 56)
        self.height = self.card_h + 18
        return self.width, self.height

    def draw(self):
        c = self.canv
        ch = self.card_h
        tracked(c, 0, ch + 6, self.note, FONTS['P-SB'], 8.5, self.accent, 2.2)
        c.setFillColor(HexColor('#0C0C11'))
        c.setStrokeColor(HexColor('#26262E'))
        c.setLineWidth(0.8)
        c.roundRect(0, 0, self.width, ch, 8, stroke=1, fill=1)
        # avatar
        c.setFillColor(self.accent)
        c.circle(28, ch - 26, 13, stroke=0, fill=1)
        c.setFillColor(JET)
        c.setFont(FONTS['P-XB'], 12)
        c.drawCentredString(28, ch - 30.5, 'Y')
        # handle + pin badge
        c.setFillColor(WHITE)
        c.setFont(FONTS['P-B'], 10.5)
        c.drawString(50, ch - 22, 'YOU  ·  Creator')
        bw = 58
        c.setFillColor(HexColor('#1C1C24'))
        c.roundRect(self.width - bw - 12, ch - 30, bw, 16, 8, stroke=0, fill=1)
        # little pin glyph
        c.setFillColor(self.accent)
        c.circle(self.width - bw - 2, ch - 22, 2.6, stroke=0, fill=1)
        c.setStrokeColor(self.accent)
        c.setLineWidth(1.2)
        c.line(self.width - bw - 2, ch - 25, self.width - bw - 2, ch - 29)
        c.setFillColor(HexColor('#B9BDC4'))
        c.setFont(FONTS['P-SB'], 7)
        c.drawString(self.width - bw + 6, ch - 25, 'PINNED')
        # comment text
        c.setFillColor(HexColor('#EFF0F2'))
        c.setFont(FONTS['P-M'], 11)
        ty = ch - 44
        for ln in self.tlines:
            c.drawString(50, ty, ln)
            ty -= 15


class WorksheetCard(Flowable):
    """Fill-in worksheet card: title chip + labeled write-in lines."""

    def __init__(self, title, fields, accent):
        super().__init__()
        self.title = title
        self.fields = fields
        self.accent = accent

    def wrap(self, aw, ah):
        self.width = AVAIL
        self.height = 40 + len(self.fields) * 27 + 10
        return self.width, self.height

    def draw(self):
        c = self.canv
        h = self.height
        c.setFillColor(HexColor('#0C0C11'))
        c.setStrokeColor(HexColor('#26262E'))
        c.setLineWidth(0.8)
        c.roundRect(0, 0, self.width, h - 6, 8, stroke=1, fill=1)
        c.setFillColor(self.accent)
        c.rect(0, 0, 3, h - 6, stroke=0, fill=1)
        # title chip
        tw = pdfmetrics.stringWidth(self.title, FONTS['P-B'], 9.5) + \
            2.0 * len(self.title) + 22
        c.setFillColor(self.accent)
        c.roundRect(14, h - 34, tw, 19, 9.5, stroke=0, fill=1)
        tracked(c, 25, h - 28.5, self.title, FONTS['P-B'], 9.5, JET, 2.0)
        y = h - 58
        for f in self.fields:
            c.setFillColor(HexColor('#D6D8DB'))
            c.setFont(FONTS['P-M'], 10)
            c.drawString(16, y, f)
            lw = pdfmetrics.stringWidth(f, FONTS['P-M'], 10)
            c.setStrokeColor(HexColor('#3A3A44'))
            c.setLineWidth(0.9)
            c.setDash(2, 3)
            c.line(24 + lw, y - 1, self.width - 16, y - 1)
            c.setDash()
            y -= 27


class NextStepBanner(Flowable):
    """End-of-document wayfinding: big arrow + where to go next."""

    def __init__(self, accent, line1, line2):
        super().__init__()
        self.accent = accent
        self.line1 = line1
        self.line2 = line2

    def wrap(self, aw, ah):
        self.width = AVAIL
        self.height = 62
        return self.width, self.height

    def draw(self):
        c = self.canv
        c.setFillColor(HexColor('#0C0C11'))
        c.setStrokeColor(self.accent)
        c.setLineWidth(1)
        c.roundRect(0, 4, self.width, 54, 7, stroke=1, fill=1)
        # arrow badge
        c.setFillColor(self.accent)
        c.circle(34, 31, 16, stroke=0, fill=1)
        c.setFillColor(JET)
        p = c.beginPath()
        p.moveTo(28, 38)
        p.lineTo(28, 24)
        p.lineTo(42, 31)
        p.close()
        c.drawPath(p, stroke=0, fill=1)
        tracked(c, 62, 38, self.line1, FONTS['P-SB'], 8.5, self.accent, 2.2)
        c.setFillColor(WHITE)
        c.setFont(FONTS['P-B'], 13.5)
        c.drawString(62, 16, self.line2)


# ---------------------------------------------------------------- styles

def make_styles(accent=CYAN):
    """Large-print, high-contrast styles; the accent color is per-section."""
    S = {}
    S['body'] = ParagraphStyle('body', fontName=FONTS['P'], fontSize=11,
                               leading=17.5, textColor=HexColor('#EFF0F2'),
                               spaceAfter=9)
    S['lede'] = ParagraphStyle('lede', parent=S['body'], fontName=FONTS['P-M'],
                               fontSize=12.5, leading=19.5,
                               textColor=HexColor('#E2E4E7'), spaceAfter=11)
    S['h3'] = ParagraphStyle('h3', fontName=FONTS['P-SB'], fontSize=13.5,
                             leading=17.5, textColor=accent, spaceBefore=12,
                             spaceAfter=6)
    S['label'] = ParagraphStyle('label', fontName=FONTS['P-SB'], fontSize=10,
                                leading=14.5, textColor=MAGENTA, spaceBefore=7,
                                spaceAfter=5)
    S['bullet'] = ParagraphStyle('bullet', parent=S['body'], leftIndent=17,
                                 bulletIndent=2, spaceAfter=5,
                                 bulletFontName=FONTS['P-B'], bulletFontSize=11,
                                 bulletColor=accent)
    S['item'] = ParagraphStyle('item', parent=S['body'], spaceAfter=4.5,
                               leading=16.5)
    S['mono'] = ParagraphStyle('mono', fontName=FONTS['MONO'], fontSize=8.8,
                               leading=13.6, textColor=HexColor('#F2F2F0'))
    S['cell'] = ParagraphStyle('cell', fontName=FONTS['P'], fontSize=10,
                               leading=14.5, textColor=HexColor('#EFF0F2'))
    S['cellh'] = ParagraphStyle('cellh', fontName=FONTS['P-SB'], fontSize=9,
                                leading=12.5, textColor=accent)
    S['accent'] = accent
    S['accent_hex'] = accent.hexval().replace('0x', '#').upper()
    return S


# ---------------------------------------------------------------- builders

NUM_RE = re.compile(r'^(\d{1,3}\.)\s+(.*)$')


def para_body(text, S):
    m = NUM_RE.match(text)
    if m:
        return Paragraph(
            f'<font color="{S["accent_hex"]}" name="{FONTS["P-SB"]}">{m.group(1)}</font> '
            f'{esc(m.group(2))}', S['item'])
    if text.lower().startswith('category:'):
        val = text.split(':', 1)[1].strip()
        return Paragraph(
            f'<font color="#F600A2" name="{FONTS["P-SB"]}" size="9">CATEGORY'
            f'</font>&nbsp;&nbsp;<font color="#D6D8DB" size="10">{esc(val.upper())}</font>',
            S['item'])
    if '____' in text:
        text = re.sub(r'_{6,}', lambda m: f'<font color="#3A3A44">{m.group(0)}</font>', esc(text))
        return Paragraph(text, S['body'])
    return Paragraph(esc(text), S['body'])


def code_panel(code_elems, S):
    inner = []
    for i, el in enumerate(code_elems):
        txt = ' '.join(el['lines'])
        if i:
            inner.append(Spacer(1, 6))
        inner.append(Paragraph(esc(txt), S['mono']))
    hdr = Paragraph(
        f'<font color="{S["accent_hex"]}" name="{FONTS["P-B"]}" size="8.5">'
        f'COPY THIS PROMPT</font>'
        f'<font color="#8A8F98" name="{FONTS["P-SB"]}" size="8.5">'
        f' &nbsp;&#8594;&nbsp; PASTE IT INTO YOUR AI TOOL</font>',
        ParagraphStyle('codehdr', fontName=FONTS['P-B'], fontSize=8.5,
                       leading=11, textColor=S['accent']))
    t = Table([[hdr], [inner]], colWidths=[AVAIL])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#15151C')),
        ('BACKGROUND', (0, 1), (-1, 1), PANEL),
        ('BOX', (0, 0), (-1, -1), 0.7, PANEL_EDGE),
        ('LINEBELOW', (0, 0), (-1, 0), 0.7, PANEL_EDGE),
        ('LINEBEFORE', (0, 0), (0, -1), 2.5, S['accent']),
        ('LEFTPADDING', (0, 0), (-1, -1), 13),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, 0), 6),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('TOPPADDING', (0, 1), (-1, 1), 10),
        ('BOTTOMPADDING', (0, 1), (-1, 1), 10),
    ]))
    return t


LABEL_RE = re.compile(r'^([A-Z][A-Z0-9 .+/&\'-]{3,}?)(?=\s+[A-Z][a-z])')


def callout_row(txt, S):
    m = LABEL_RE.match(txt)
    if m:
        lbl, rest = m.group(1), txt[m.end():].strip()
        html = (f'<font color="#F600A2" name="{FONTS["P-SB"]}" size="9.5">'
                f'{esc(lbl)}</font><br/>{esc(rest)}')
    else:
        html = esc(txt)
    t = Table([[Paragraph(html, S['cell'])]], colWidths=[AVAIL])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), CHARCOAL),
        ('BOX', (0, 0), (-1, -1), 0.7, PANEL_EDGE),
        ('LINEBEFORE', (0, 0), (0, -1), 2.5, MAGENTA),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    return t


def themed_table(rows, S):
    """Returns a list of flowables: leading single-cell rows become callout
    boxes above the real table (pdfplumber sometimes merges an adjacent
    callout into the table grid)."""
    ncols = max(len(r) for r in rows)
    rows = [r + [''] * (ncols - len(r)) for r in rows]
    lead = []
    while rows and sum(1 for c in rows[0] if c.strip()) == 1:
        lead.append(next(c for c in rows[0] if c.strip()))
        rows = rows[1:]
    pre = []
    for txt in lead:
        pre.append(callout_row(txt, S))
        pre.append(Spacer(1, 8))
    if not rows:
        return pre
    span_rows = set()
    for ri, r in enumerate(rows):
        if sum(1 for c in r if c.strip()) == 1 and ri > 0:
            span_rows.add(ri)

    # column widths: never narrower than the longest single word,
    # remaining space shared by content volume (span rows excluded)
    pad = 16
    minw, weights = [], []
    for ci in range(ncols):
        cells = [r[ci] for ri, r in enumerate(rows) if ri not in span_rows]
        words = [w for c in cells for w in c.split()] or ['x']
        longest = max(pdfmetrics.stringWidth(w, FONTS['P'], 10) for w in words)
        minw.append(longest + pad)
        weights.append(max(max((min(len(c), 42) for c in cells), default=4), 4))
    spare = AVAIL - sum(minw)
    if spare > 0:
        total = sum(weights)
        widths = [m + spare * w / total for m, w in zip(minw, weights)]
    else:
        widths = [m * AVAIL / sum(minw) for m in minw]

    header = [Paragraph(esc(c.upper()), S['cellh']) for c in rows[0]]
    data = [header]
    for ri, r in enumerate(rows[1:], 1):
        if ri in span_rows:
            txt = next(c for c in r if c.strip())
            m = LABEL_RE.match(txt)
            if m:
                lbl, rest = m.group(1), txt[m.end():].strip()
                html = (f'<font color="#F600A2" name="{FONTS["P-SB"]}" size="8">'
                        f'{esc(lbl)}</font><br/>{esc(rest)}')
            else:
                html = esc(txt)
            data.append([Paragraph(html, S['cell'])] + [''] * (ncols - 1))
        else:
            data.append([Paragraph(esc(c), S['cell']) for c in r])
    t = Table(data, colWidths=widths, repeatRows=1)
    style = [
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#14141B')),
        ('LINEBELOW', (0, 0), (-1, 0), 1, S['accent']),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#202028')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 7),
        ('RIGHTPADDING', (0, 0), (-1, -1), 7),
        ('TOPPADDING', (0, 0), (-1, -1), 5.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5.5),
    ]
    for i in range(1, len(data)):
        style.append(('BACKGROUND', (0, i), (-1, i),
                      HexColor('#050508') if i % 2 else HexColor('#0A0A0F')))
    for ri in span_rows:
        style.append(('SPAN', (0, ri), (-1, ri)))
        style.append(('BACKGROUND', (0, ri), (-1, ri), CHARCOAL))
    t.setStyle(TableStyle(style))
    return pre + [t]


# ---------------------------------------------------------------- document

class SceneDoc(BaseDocTemplate):
    def __init__(self, path, meta, **kw):
        super().__init__(path, pagesize=letter, **kw)
        self.meta = meta
        frame = Frame(MARGIN, 0.9 * inch, AVAIL, PAGE_H - 1.18 * inch - 0.9 * inch,
                      leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        cover_frame = Frame(MARGIN, MARGIN, AVAIL, PAGE_H - 2 * MARGIN)
        self.addPageTemplates([
            PageTemplate(id='cover', frames=[cover_frame], onPage=self.draw_cover),
            PageTemplate(id='content', frames=[frame], onPage=self.draw_page),
        ])

    # ---- cover page
    def draw_cover(self, c, doc):
        m = self.meta
        c.setFillColor(JET)
        c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)

        cx = PAGE_W / 2

        # ghost module numeral behind the title block
        kick = m['kicker'].upper().split()
        ghost = kick[-1] if kick[-1] not in ('HERE',) else 'OS'
        gsize = 300 if len(ghost) <= 2 else 215
        c.saveState()
        c.translate(cx, PAGE_H - 385)
        c.transform(1, 0, 0.14, 1, 0, 0)
        c.setFont(FONTS['P-XB'], gsize)
        c.setFillColor(blend_black(m['accent_hex'], 0.12))
        c.drawCentredString(0, 0, ghost)
        c.restoreState()
        # frame brackets
        bracket(c, 58, PAGE_H - 58, 46, 'tl', MAGENTA, 3)
        bracket(c, PAGE_W - 58, PAGE_H - 58, 46, 'tr', HexColor('#2A2A31'), 2)
        bracket(c, 58, 58, 46, 'bl', HexColor('#2A2A31'), 2)
        bracket(c, PAGE_W - 58, 58, 46, 'br', CYAN, 3)

        tracked(c, 0, PAGE_H - 96, 'THE SCENE AI  /  CREATOR OS', FONTS['P-SB'],
                7.5, MUTED, 2.6, center_at=cx)

        # kicker
        y = PAGE_H - 300
        tracked(c, 0, y + 66, m['kicker'], FONTS['P-SB'], 12.5, m['accent'],
                4.2, center_at=cx)

        # title (up to 2 lines) — brushed-silver brand headline
        title = m['title']
        size = 42
        f = FONTS['P-XB']
        lines = [title]
        if pdfmetrics.stringWidth(title, f, size) > AVAIL + 40:
            words = title.split()
            half = len(words) // 2 + len(words) % 2
            lines = [' '.join(words[:half]), ' '.join(words[half:])]
        while max(pdfmetrics.stringWidth(l, f, size) for l in lines) > AVAIL + 40:
            size -= 2
        ty = y
        for ln in lines:
            metal_text(c, cx, ty, ln, f, size)
            ty -= size * 1.12
        ty += size * 1.12

        # gradient bar: section color into brand magenta
        c.saveState()
        p = c.beginPath()
        p.rect(cx - 80, ty - 26, 160, 3.4)
        c.clipPath(p, stroke=0, fill=0)
        c.linearGradient(cx - 80, ty - 26, cx + 80, ty - 26,
                         (m['accent'], MAGENTA), extend=False)
        c.restoreState()

        # subtitle
        sub = m.get('sub') or ''
        if sub:
            c.setFont(FONTS['P'], 13)
            c.setFillColor(HexColor('#E2E4E7'))
            # wrap
            words, cur, subls = sub.split(), '', []
            for w in words:
                t = (cur + ' ' + w).strip()
                if pdfmetrics.stringWidth(t, FONTS['P'], 13) < 400:
                    cur = t
                else:
                    subls.append(cur); cur = w
            if cur:
                subls.append(cur)
            sy = ty - 56
            for ln in subls:
                c.drawCentredString(cx, sy, ln)
                sy -= 19
        else:
            sy = ty - 56

        # tagline in three colors
        tag = m.get('tagline') or ''
        if tag:
            parts = [p.strip() + '.' for p in tag.split('.') if p.strip()]
            fs, gap = 9, 12
            fnt = FONTS['P-SB']
            track = 1.8
            widths = [pdfmetrics.stringWidth(p, fnt, fs) + track * (len(p) - 1)
                      for p in parts]
            total = sum(widths) + gap * (len(parts) - 1)
            x = cx - total / 2
            ty2 = sy - 26
            cols = [WHITE, m['accent'], MAGENTA]
            for i, p in enumerate(parts):
                tracked(c, x, ty2, p, fnt, fs, cols[i % 3], track)
                x += widths[i] + gap

        # progress strip: PART n / 19 with tick marks — "you are here"
        part = m.get('part', 0)
        total = m.get('total', 19)
        py = 205
        tracked(c, 0, py + 16, f'PART {part:02d} OF {total}', FONTS['P-SB'],
                8.5, HexColor('#9AA0A8'), 2.4, center_at=cx)
        tick_w, gap = 14, 5
        row_w = total * tick_w + (total - 1) * gap
        tx = cx - row_w / 2
        for i in range(total):
            c.setFillColor(m['accent'] if i == part - 1 else HexColor('#26262E'))
            c.rect(tx + i * (tick_w + gap), py, tick_w, 5, stroke=0, fill=1)
        if part > 0:
            hx = tx + (part - 1) * (tick_w + gap) + tick_w / 2
            c.setFillColor(m['accent'])
            p = c.beginPath()
            p.moveTo(hx - 4, py + 12)
            p.lineTo(hx + 4, py + 12)
            p.lineTo(hx, py + 7)
            p.close()
            c.drawPath(p, stroke=0, fill=1)

        # bottom: official logo lockup (includes tagline)
        img = ImageReader(LOGO)
        iw, ih = img.getSize()
        lw = 250.0
        lh = lw * ih / iw
        c.drawImage(img, cx - lw / 2, 76, lw, lh)

    # ---- content pages
    def draw_page(self, c, doc):
        m = self.meta
        c.setFillColor(JET)
        c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)

        # header
        hy = PAGE_H - 0.62 * inch
        bracket(c, MARGIN, hy + 12, 8, 'tl', MAGENTA, 1.6)
        x = tracked(c, MARGIN + 14, hy, 'THE SCENE AI', FONTS['P-SB'], 8,
                    m['accent'], 1.8)
        w1 = pdfmetrics.stringWidth('THE SCENE AI', FONTS['P-SB'], 8) + 1.8 * 11
        tracked(c, MARGIN + 14 + w1 + 8, hy, '/  ' + m['kicker'].upper(),
                FONTS['P-SB'], 8, HexColor('#8A8F98'), 1.8)
        tw = pdfmetrics.stringWidth(m['title'].upper(), FONTS['P-SB'], 8) + 1.6 * len(m['title'])
        tracked(c, PAGE_W - MARGIN - tw, hy, m['title'].upper(), FONTS['P-SB'],
                8, HexColor('#8A8F98'), 1.6)
        c.setStrokeColor(RULE)
        c.setLineWidth(0.7)
        c.line(MARGIN, hy - 9, PAGE_W - MARGIN, hy - 9)

        # footer
        fy = 0.55 * inch
        c.setStrokeColor(RULE)
        c.line(MARGIN, fy + 12, PAGE_W - MARGIN, fy + 12)
        tracked(c, MARGIN, fy, 'THE SCENE AI  —  CREATOR OS', FONTS['P'], 7.4,
                HexColor('#9AA0A8'), 1.6)
        pn = f'PAGE {doc.page - 1:02d}'
        pw = pdfmetrics.stringWidth(pn, FONTS['P-SB'], 8) + 1.8 * len(pn)
        tracked(c, PAGE_W - MARGIN - pw, fy, pn, FONTS['P-SB'], 8,
                m['accent'], 1.8)
        bracket(c, PAGE_W - MARGIN + 4, fy - 4, 5, 'br', MAGENTA, 1.2)


# ---------------------------------------------------------------- assembly

def build_doc(docid, pages, meta, outpath, S):
    doc = SceneDoc(outpath, meta,
                   leftMargin=MARGIN, rightMargin=MARGIN,
                   topMargin=MARGIN, bottomMargin=MARGIN,
                   title=f"THE SCENE AI — {meta['kicker']} — {meta['title'].title()}",
                   author='THE SCENE AI')
    story = [NextPageTemplate('content'), PageBreak()]

    # flatten elems across pages (skipping the cover page elems)
    elems = []
    for p in pages:
        if p is meta['cover_page']:
            continue
        elems.extend(p['elems'])

    i = 0
    flow = []
    did_map = did_method = False
    while i < len(elems):
        e = elems[i]
        t = e['type']
        if t == 'code':
            group = []
            while i < len(elems) and elems[i]['type'] == 'code':
                group.append(elems[i]); i += 1
            flow.append(Spacer(1, 2))
            flow.append(code_panel(group, S))
            flow.append(Spacer(1, 10))
            continue
        if t == 'table':
            flow.append(Spacer(1, 4))
            flow.extend(themed_table(e['rows'], S))
            flow.append(Spacer(1, 12))
            if docid == 'START HERE' and not did_map:
                did_map = True
                flow.append(Spacer(1, 6))
                flow.append(AccentHeading('Your road map', S['accent']))
                flow.append(Spacer(1, 10))
                flow.append(SystemMap())
                flow.append(Spacer(1, 14))
        elif t == 'flow':
            flow.append(Spacer(1, 6))
            flow.append(StepFlow(e['steps'], e.get('caption', '')))
            flow.append(Spacer(1, 10))
        elif t == 'ccard':
            flow.append(Spacer(1, 6))
            flow.append(CommentCard(e['note'], e['text'], S['accent']))
            flow.append(Spacer(1, 4))
        elif t == 'wcard':
            flow.append(Spacer(1, 8))
            flow.append(WorksheetCard(e['title'], e['fields'], S['accent']))
            flow.append(Spacer(1, 8))
        elif t == 'h2':
            flow.append(Spacer(1, 14))
            flow.append(AccentHeading(' '.join(e['lines']), S['accent']))
            flow.append(Spacer(1, 8))
        elif t == 'h3':
            h3txt = ' '.join(e['lines'])
            if h3txt.lower().startswith('copy-and-paste'):
                pass  # the prompt panel's own COPY THIS header replaces it
            else:
                flow.append(Paragraph(esc(h3txt), S['h3']))
        elif t == 'label':
            flow.append(Paragraph(esc(' '.join(e['lines']).upper()), S['label']))
        elif t == 'bullet':
            for ln in e['lines']:
                if ln.strip():
                    flow.append(Paragraph(esc(ln), S['bullet'], bulletText='›'))
        elif t in ('body', 'sub'):
            style_key = 'lede' if t == 'sub' else 'body'
            txt = ' '.join(e['lines'])
            if style_key == 'lede':
                flow.append(Paragraph(esc(txt), S['lede']))
            else:
                flow.append(para_body(txt, S))
            if docid == 'MODULE 03' and not did_method:
                did_method = True
                flow.append(Spacer(1, 8))
                flow.append(MethodFlow())
                flow.append(Spacer(1, 12))
        elif t == 'h1':
            flow.append(Spacer(1, 14))
            flow.append(AccentHeading(' '.join(e['lines']), S['accent']))
            flow.append(Spacer(1, 8))
        i += 1

    # keep headings attached to following block
    merged = []
    j = 0
    while j < len(flow):
        f = flow[j]
        if isinstance(f, (AccentHeading, PanelLabel)) or (
                isinstance(f, Paragraph) and f.style.name in ('h3', 'label')):
            group = [f]
            k = j + 1
            while k < len(flow) and isinstance(flow[k], Spacer):
                group.append(flow[k]); k += 1
            if k < len(flow):
                group.append(flow[k]); k += 1
            merged.append(KeepTogether(group))
            j = k
        else:
            merged.append(f)
            j += 1

    story.extend(merged)
    nxt = meta.get('next')
    if nxt:
        story.append(Spacer(1, 22))
        story.append(NextStepBanner(S['accent'], 'NEXT STEP',
                                    f'Go to {nxt[0]} — {nxt[1]}'))
    else:
        story.append(Spacer(1, 22))
        story.append(NextStepBanner(S['accent'], 'YOU FINISHED THE SYSTEM',
                                    'Now go make your first episode.'))
    doc.build(story)


def main():
    register_fonts()
    os.makedirs(OUTDIR, exist_ok=True)
    final = os.path.join(HERE, 'content_final.json')
    simple = os.path.join(HERE, 'content_simple.json')
    src = final if os.path.exists(final) else (
        simple if os.path.exists(simple) else CONTENT)
    pages = json.load(open(src))

    # group pages by doc, preserving order
    docs = []
    for p in pages:
        if docs and docs[-1][0] == p['doc']:
            docs[-1][1].append(p)
        else:
            docs.append((p['doc'], [p]))

    # doc titles up-front so each doc can point to the next one
    titles = {}
    for docid, dpages in docs:
        for p in dpages:
            h1s = [e for e in p['elems'] if e['type'] == 'h1']
            if h1s:
                titles[docid] = ' '.join(' '.join(h['lines']) for h in h1s)
                break
        titles.setdefault(docid, docid)

    for idx, (docid, dpages) in enumerate(docs):
        accent_hex = DOC_ACCENT.get(docid, '#00E5FF')
        S = make_styles(HexColor(accent_hex))
        # cover metadata from the first page containing an h1
        cover = None
        nxt = None
        if idx + 1 < len(docs):
            nd = docs[idx + 1][0]
            nxt = (nd, titles[nd])
        meta = {'kicker': docid, 'title': docid, 'sub': '', 'tagline': '',
                'accent': HexColor(accent_hex), 'accent_hex': accent_hex,
                'part': idx + 1, 'total': len(docs), 'next': nxt}
        for p in dpages:
            types = [e['type'] for e in p['elems']]
            if 'h1' in types:
                cover = p
                labels = [e for e in p['elems'] if e['type'] == 'label']
                h1s = [e for e in p['elems'] if e['type'] == 'h1']
                subs = [e for e in p['elems'] if e['type'] == 'sub']
                meta['kicker'] = ' '.join(labels[0]['lines']) if labels else docid
                meta['title'] = ' '.join(' '.join(h['lines']) for h in h1s)
                meta['sub'] = ' '.join(subs[0]['lines']) if subs else ''
                if len(labels) > 1:
                    meta['tagline'] = ' '.join(labels[-1]['lines'])
                break
        meta['cover_page'] = cover

        def fname_part(s):
            s = re.sub(r'[‘’\']', '', s).title()
            for w, r in (('Scene', 'SCENE'), ('Os', 'OS'), ('Ai', 'AI')):
                s = re.sub(rf'\b{w}\b', r, s)
            return re.sub(r'[^A-Za-z0-9]+', '-', s).strip('-')

        safe_title = fname_part(meta['title'])
        safe_kick = fname_part(meta['kicker'])
        fname = f'{idx:02d}_The-SCENE-AI_{safe_kick}_{safe_title}.pdf'
        outpath = os.path.join(OUTDIR, fname)
        build_doc(docid, dpages, meta, outpath, S)
        print('wrote', fname)


if __name__ == '__main__':
    main()
