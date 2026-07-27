#!/usr/bin/env python3
"""Extract structured content from the SCENE AI master bundle PDF."""
import json
import os
import pdfplumber
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
PDF = os.path.join(HERE, 'source', 'The_SCENE_AI_Creator_OS_Master_Bundle.pdf')
OUT = os.path.join(HERE, 'content.json')


def in_bbox(x, y, bbox, pad=2):
    x0, top, x1, bottom = bbox
    return (x0 - pad) <= x <= (x1 + pad) and (top - pad) <= y <= (bottom + pad)


def classify(fontname, size):
    f = fontname.split('+')[-1]
    if 'Mono' in f:
        return 'code'
    if f == 'Carlito-Bold':
        return 'h2' if size > 15 else 'h3'
    if f == 'LiberationSans-Bold':
        if size > 20:
            return 'h1'
        return 'label'
    if f == 'OpenSymbol':
        return 'bulletmark'
    # LiberationSans regular
    if size > 11:
        return 'sub'
    return 'body'


def extract():
    docs = []
    with pdfplumber.open(PDF) as pdf:
        pages_out = []
        for pi, page in enumerate(pdf.pages):
            tables = page.find_tables()
            tbboxes = [t.bbox for t in tables]
            telems = []
            for t in tables:
                data = t.extract()
                # clean cells
                rows = [[(c or '').replace('\n', ' ').strip() for c in row] for row in data]
                telems.append({'type': 'table', 'y': t.bbox[1], 'rows': rows})

            # group chars into lines, excluding chars inside table bboxes
            chars = []
            for ch in page.chars:
                cx = (ch['x0'] + ch['x1']) / 2
                cy = (ch['top'] + ch['bottom']) / 2
                if any(in_bbox(cx, cy, bb) for bb in tbboxes):
                    continue
                chars.append(ch)
            chars.sort(key=lambda c: ((c['top'] + c['bottom']) / 2, c['x0']))
            groups = []
            for ch in chars:
                cy = (ch['top'] + ch['bottom']) / 2
                if groups and abs(cy - groups[-1]['cy']) <= 3.5:
                    groups[-1]['chs'].append(ch)
                    n = len(groups[-1]['chs'])
                    groups[-1]['cy'] = ((groups[-1]['cy'] * (n - 1)) + cy) / n
                else:
                    groups.append({'cy': cy, 'chs': [ch]})

            line_items = []
            for g in groups:
                chs = sorted(g['chs'], key=lambda c: c['x0'])
                text = ''
                prev_x1 = None
                for c in chs:
                    if prev_x1 is not None and c['x0'] - prev_x1 > 1.0:
                        text += ' '
                    text += c['text']
                    prev_x1 = c['x1']
                text = text.strip()
                if not text:
                    continue
                fonts = Counter((c['fontname'], round(c['size'], 1)) for c in chs
                                if c['text'].strip())
                (fn, sz), _ = fonts.most_common(1)[0]
                top = min(c['top'] for c in chs)
                bottom = max(c['bottom'] for c in chs)
                x0 = min(c['x0'] for c in chs)
                # bullet detection: line starts with OpenSymbol char
                first = chs[0]
                is_bullet = 'OpenSymbol' in first['fontname']
                kind = classify(fn, sz)
                if is_bullet:
                    kind = 'bullet'
                    # strip the marker glyph
                    text = text[1:].strip() if text else text
                line_items.append({'type': kind, 'text': text, 'y': top,
                                   'bottom': bottom, 'x0': x0, 'size': sz})

            # drop header breadcrumb (top of page) and footer
            filtered = []
            for li in line_items:
                norm = ' '.join(li['text'].split())
                if li['y'] < 60 and norm.startswith('THE SCENE AI /'):
                    continue
                if li['y'] > page.height - 60 and norm.startswith('THE SCENE AI |'):
                    continue
                li['text'] = norm
                filtered.append(li)

            # merge consecutive lines of same type into blocks
            blocks = []
            for li in filtered:
                if blocks and blocks[-1]['type'] == li['type'] and li['type'] in (
                        'body', 'code', 'sub', 'label') and \
                        li['y'] - blocks[-1]['bottom'] < (7 if li['type'] == 'code' else 4.5):
                    blocks[-1]['lines'].append(li['text'])
                    blocks[-1]['bottom'] = li['bottom']
                else:
                    blocks.append({'type': li['type'], 'lines': [li['text']],
                                   'y': li['y'], 'bottom': li['bottom']})

            elems = blocks + telems
            elems.sort(key=lambda e: e['y'])
            for e in elems:
                e.pop('bottom', None)
            pages_out.append({'page': pi + 1, 'elems': elems})

    # figure out doc id per page from breadcrumb
    with pdfplumber.open(PDF) as pdf:
        for pi, page in enumerate(pdf.pages):
            txt = page.extract_text() or ''
            first = txt.split('\n')[0] if txt else ''
            docid = first.replace('THE SCENE AI /', '').strip() if first.startswith('THE SCENE AI /') else '?'
            pages_out[pi]['doc'] = docid

    json.dump(pages_out, open(OUT, 'w'), indent=1)
    print('pages:', len(pages_out))
    print('docs:', sorted(set(p['doc'] for p in pages_out)))


extract()
