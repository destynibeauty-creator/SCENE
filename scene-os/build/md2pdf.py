#!/usr/bin/env python3
"""CLASSROOM-COPY.md -> clean branded PDF (light, readable, Poppins)."""
import os, re, html
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate,
                                Paragraph, Spacer, Table, TableStyle,
                                KeepTogether)
from reportlab.lib.styles import ParagraphStyle

ROOT = '/home/user/SCENE/scene-os'
F = os.path.join(ROOT, 'build', 'fonts')
SRC = os.path.join(ROOT, 'CLASSROOM-COPY.md')
OUT = os.path.join(ROOT, 'CLASSROOM-COPY.pdf')

for name, fn in [('Pop', 'Poppins-Regular.ttf'), ('Pop-B', 'Poppins-Bold.ttf'),
                 ('Pop-SB', 'Poppins-SemiBold.ttf'),
                 ('Pop-XB', 'Poppins-ExtraBold.ttf'),
                 ('Emoji', 'NotoEmoji.ttf')]:
    pdfmetrics.registerFont(TTFont(name, os.path.join(F, fn)))

CYAN = HexColor('#0099AA'); MAG = HexColor('#C4007F')
INK = HexColor('#17181C'); MUT = HexColor('#5A5E66')
BOX = HexColor('#F4F5F7'); LINE = HexColor('#DDDFE4')

EMOJI = re.compile('([\U0001F000-\U0001FAFF☀-➿⬀-⯿'
                   '←-⇿ -⁯️✅❌☐-☒]+)')

def fmt(t):
    t = html.escape(t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    t = re.sub(r'\*(.+?)\*', r'<i>\1</i>', t)
    t = re.sub(r'`(.+?)`', r'<font face="Pop-SB" color="#C4007F">\1</font>', t)
    t = t.replace('️', '')
    t = EMOJI.sub(lambda m: f'<font face="Emoji">{m.group(1)}</font>', t)
    return t

S = {
    'title': ParagraphStyle('t', fontName='Pop-XB', fontSize=20, leading=25,
                            textColor=INK, spaceAfter=4),
    'meta': ParagraphStyle('m', fontName='Pop', fontSize=9.5, leading=14,
                           textColor=MUT, spaceAfter=10),
    'h2': ParagraphStyle('h2', fontName='Pop-XB', fontSize=14.5, leading=19,
                         textColor=INK, spaceBefore=18, spaceAfter=6),
    'h3': ParagraphStyle('h3', fontName='Pop-B', fontSize=11.5, leading=16,
                         textColor=MAG, spaceBefore=12, spaceAfter=3),
    'body': ParagraphStyle('b', fontName='Pop', fontSize=10, leading=15,
                           textColor=INK, spaceAfter=5),
    'paste': ParagraphStyle('p', fontName='Pop', fontSize=9.5, leading=14.5,
                            textColor=INK),
    'cell': ParagraphStyle('c', fontName='Pop', fontSize=8.5, leading=12.5,
                           textColor=INK),
    'cellh': ParagraphStyle('ch', fontName='Pop-B', fontSize=8.5, leading=12.5,
                            textColor=INK),
}

story = []
lines = open(SRC).read().split('\n')
i = 0
quote, table = [], []

def flush_quote():
    global quote
    if not quote: return
    paras = []
    buf = []
    for q in quote:
        if q.strip() == '':
            if buf: paras.append(Paragraph(fmt(' '.join(buf)), S['paste'])); buf = []
            paras.append(Spacer(1, 5))
        else:
            buf.append(q)
    if buf: paras.append(Paragraph(fmt(' '.join(buf)), S['paste']))
    t = Table([[paras]], colWidths=[6.4 * inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), BOX),
        ('LINEBEFORE', (0, 0), (0, -1), 2.5, CYAN),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8)]))
    story.append(t); story.append(Spacer(1, 6))
    quote = []

def flush_table():
    global table
    if not table: return
    rows = []
    for r, raw in enumerate(table):
        cells = [c.strip() for c in raw.strip().strip('|').split('|')]
        rows.append([Paragraph(fmt(c), S['cellh' if r == 0 else 'cell'])
                     for c in cells])
    ncol = len(rows[0])
    widths = {3: [2.0, 1.35, 3.05], 2: [2.2, 4.2]}.get(ncol, None)
    if widths: widths = [w * inch for w in widths]
    t = Table(rows, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, LINE),
        ('BACKGROUND', (0, 0), (-1, 0), BOX),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4)]))
    story.append(t); story.append(Spacer(1, 6))
    table = []

while i < len(lines):
    ln = lines[i]
    if ln.startswith('> '):
        table and flush_table()
        quote.append(ln[2:])
    elif ln.strip() == '>':
        quote.append('')
    elif ln.startswith('|'):
        quote and flush_quote()
        if not set(ln.replace('|', '').strip()) <= set('-: '):
            table.append(ln)
    else:
        flush_quote(); flush_table()
        s = ln.strip()
        if not s:
            pass
        elif s.startswith('# '):
            story.append(Paragraph(fmt(s[2:]), S['title']))
        elif s.startswith('## '):
            story.append(Paragraph(fmt(s[3:]), S['h2']))
        elif s.startswith('### '):
            story.append(Paragraph(fmt(s[4:]), S['h3']))
        elif s == '---':
            story.append(Spacer(1, 8))
        else:
            style = 'meta' if i < 8 else 'body'
            story.append(Paragraph(fmt(s), S[style]))
    i += 1
flush_quote(); flush_table()

def deco(c, doc):
    c.saveState()
    c.setFillColor(CYAN); c.rect(0, letter[1] - 6, letter[0] * .5, 6, 0, 1)
    c.setFillColor(MAG); c.rect(letter[0] * .5, letter[1] - 6, letter[0] * .5, 6, 0, 1)
    c.setFont('Pop-SB', 7.5); c.setFillColor(MUT)
    c.drawString(0.75 * inch, 0.45 * inch, 'THE SCENE AI  ·  CLASSROOM COPY')
    c.drawRightString(letter[0] - 0.75 * inch, 0.45 * inch, str(doc.page))
    c.restoreState()

doc = BaseDocTemplate(OUT, pagesize=letter,
                      leftMargin=0.75 * inch, rightMargin=0.75 * inch,
                      topMargin=0.7 * inch, bottomMargin=0.7 * inch)
fr = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='f')
doc.addPageTemplates([PageTemplate(id='p', frames=[fr], onPage=deco)])
doc.build(story)
print('wrote', OUT)
