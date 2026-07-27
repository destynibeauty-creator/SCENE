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
    """H2 — white Poppins Bold with cyan accent bar."""

    def __init__(self, text, width=AVAIL):
        super().__init__()
        self.text = text
        self.width = width
        self.font, self.size, self.leading = FONTS['P-B'], 15.5, 19
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
        c.setFillColor(CYAN)
        c.rect(0, 0, 3, self.height - 3, stroke=0, fill=1)
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
        self.height = 11
        self.width = AVAIL

    def wrap(self, aw, ah):
        return self.width, self.height

    def draw(self):
        c = self.canv
        c.setFillColor(MAGENTA)
        c.rect(0, 3, 5, 5, stroke=0, fill=1)
        tracked(c, 11, 3, self.text, FONTS['MONO'], 6.3, MUTED, 1.4)


# ---------------------------------------------------------------- styles

def make_styles():
    S = {}
    S['body'] = ParagraphStyle('body', fontName=FONTS['P'], fontSize=9.3,
                               leading=14.6, textColor=BODY_TX, spaceAfter=8)
    S['lede'] = ParagraphStyle('lede', parent=S['body'], fontName=FONTS['P-M'],
                               fontSize=11, leading=17, textColor=SILVER,
                               spaceAfter=10)
    S['h3'] = ParagraphStyle('h3', fontName=FONTS['P-SB'], fontSize=11.5,
                             leading=15, textColor=CYAN, spaceBefore=10,
                             spaceAfter=5)
    S['label'] = ParagraphStyle('label', fontName=FONTS['P-SB'], fontSize=8.6,
                                leading=12.5, textColor=MAGENTA, spaceBefore=6,
                                spaceAfter=4)
    S['bullet'] = ParagraphStyle('bullet', parent=S['body'], leftIndent=15,
                                 bulletIndent=2, spaceAfter=4,
                                 bulletFontName=FONTS['P-B'], bulletFontSize=9.5,
                                 bulletColor=CYAN)
    S['item'] = ParagraphStyle('item', parent=S['body'], spaceAfter=3.6,
                               leading=13.6)
    S['mono'] = ParagraphStyle('mono', fontName=FONTS['MONO'], fontSize=7.4,
                               leading=11.2, textColor=HexColor('#E9E9E7'))
    S['cell'] = ParagraphStyle('cell', fontName=FONTS['P'], fontSize=8.3,
                               leading=12, textColor=BODY_TX)
    S['cellh'] = ParagraphStyle('cellh', fontName=FONTS['P-SB'], fontSize=7.6,
                                leading=10.5, textColor=CYAN)
    return S


# ---------------------------------------------------------------- builders

NUM_RE = re.compile(r'^(\d{1,3}\.)\s+(.*)$')


def para_body(text, S):
    m = NUM_RE.match(text)
    if m:
        return Paragraph(
            f'<font color="#00E5FF" name="{FONTS["P-SB"]}">{m.group(1)}</font> '
            f'{esc(m.group(2))}', S['item'])
    if text.lower().startswith('category:'):
        val = text.split(':', 1)[1].strip()
        return Paragraph(
            f'<font color="#F600A2" name="{FONTS["P-SB"]}" size="7.6">CATEGORY'
            f'</font>&nbsp;&nbsp;<font color="#C0C3C7" size="8.6">{esc(val.upper())}</font>',
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
    t = Table([[inner]], colWidths=[AVAIL])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), PANEL),
        ('BOX', (0, 0), (-1, -1), 0.7, PANEL_EDGE),
        ('LINEBEFORE', (0, 0), (0, -1), 2, CYAN),
        ('LEFTPADDING', (0, 0), (-1, -1), 13),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ]))
    return t


LABEL_RE = re.compile(r'^([A-Z][A-Z0-9 .+/&\'-]{3,}?)(?=\s+[A-Z][a-z])')


def themed_table(rows, S):
    ncols = max(len(r) for r in rows)
    rows = [r + [''] * (ncols - len(r)) for r in rows]
    span_rows = set()
    for ri, r in enumerate(rows):
        if sum(1 for c in r if c.strip()) == 1 and ri > 0:
            span_rows.add(ri)

    # column widths weighted by content length (span rows excluded, capped)
    weights = []
    for ci in range(ncols):
        vals = [min(len(r[ci]), 42) for ri, r in enumerate(rows)
                if ri not in span_rows]
        weights.append(max(max(vals or [4]), 4))
    total = sum(weights)
    widths = [max(AVAIL * w / total, 42) for w in weights]
    f = AVAIL / sum(widths)
    widths = [w * f for w in widths]

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
        ('LINEBELOW', (0, 0), (-1, 0), 1, CYAN),
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
    return t


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
        c.setFillColor(HexColor('#101016'))
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
        tracked(c, 0, y + 66, m['kicker'], FONTS['P-SB'], 12, CYAN, 4.2, center_at=cx)

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

        # gradient bar
        gradient_bar(c, cx - 80, ty - 26, 160, 3.4)

        # subtitle
        sub = m.get('sub') or ''
        if sub:
            c.setFont(FONTS['P'], 11.5)
            c.setFillColor(SILVER)
            # wrap
            words, cur, subls = sub.split(), '', []
            for w in words:
                t = (cur + ' ' + w).strip()
                if pdfmetrics.stringWidth(t, FONTS['P'], 11.5) < 380:
                    cur = t
                else:
                    subls.append(cur); cur = w
            if cur:
                subls.append(cur)
            sy = ty - 56
            for ln in subls:
                c.drawCentredString(cx, sy, ln)
                sy -= 17
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
            cols = [WHITE, CYAN, MAGENTA]
            for i, p in enumerate(parts):
                tracked(c, x, ty2, p, fnt, fs, cols[i % 3], track)
                x += widths[i] + gap

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
        bracket(c, MARGIN, hy + 11, 7, 'tl', MAGENTA, 1.5)
        x = tracked(c, MARGIN + 13, hy, 'THE SCENE AI', FONTS['P-SB'], 7, CYAN, 1.8)
        w1 = pdfmetrics.stringWidth('THE SCENE AI', FONTS['P-SB'], 7) + 1.8 * 11
        tracked(c, MARGIN + 13 + w1 + 8, hy, '/  ' + m['kicker'].upper(),
                FONTS['P-SB'], 7, HexColor('#5A5E66'), 1.8)
        tw = pdfmetrics.stringWidth(m['title'].upper(), FONTS['P-SB'], 7) + 1.6 * len(m['title'])
        tracked(c, PAGE_W - MARGIN - tw, hy, m['title'].upper(), FONTS['P-SB'],
                7, HexColor('#5A5E66'), 1.6)
        c.setStrokeColor(RULE)
        c.setLineWidth(0.7)
        c.line(MARGIN, hy - 9, PAGE_W - MARGIN, hy - 9)

        # footer
        fy = 0.55 * inch
        c.setStrokeColor(RULE)
        c.line(MARGIN, fy + 12, PAGE_W - MARGIN, fy + 12)
        tracked(c, MARGIN, fy, 'THE SCENE AI  —  CREATOR OS', FONTS['P'], 6.2,
                MUTED, 1.6)
        pn = f'PAGE {doc.page - 1:02d}'
        pw = pdfmetrics.stringWidth(pn, FONTS['P-SB'], 6.6) + 1.8 * len(pn)
        tracked(c, PAGE_W - MARGIN - pw, fy, pn, FONTS['P-SB'], 6.6, CYAN, 1.8)
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
            flow.append(themed_table(e['rows'], S))
            flow.append(Spacer(1, 12))
        elif t == 'h2':
            flow.append(Spacer(1, 14))
            flow.append(AccentHeading(' '.join(e['lines'])))
            flow.append(Spacer(1, 8))
        elif t == 'h3':
            h3txt = ' '.join(e['lines'])
            if h3txt.lower().startswith('copy-and-paste'):
                flow.append(Spacer(1, 3))
                flow.append(PanelLabel(h3txt.upper()))
                flow.append(Spacer(1, 4))
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
        elif t == 'h1':
            flow.append(Spacer(1, 14))
            flow.append(AccentHeading(' '.join(e['lines'])))
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
    doc.build(story)


def main():
    register_fonts()
    os.makedirs(OUTDIR, exist_ok=True)
    S = make_styles()
    pages = json.load(open(CONTENT))

    # group pages by doc, preserving order
    docs = []
    for p in pages:
        if docs and docs[-1][0] == p['doc']:
            docs[-1][1].append(p)
        else:
            docs.append((p['doc'], [p]))

    for idx, (docid, dpages) in enumerate(docs):
        # cover metadata from the first page containing an h1
        cover = None
        meta = {'kicker': docid, 'title': docid, 'sub': '', 'tagline': ''}
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
