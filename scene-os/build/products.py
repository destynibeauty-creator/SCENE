#!/usr/bin/env python3
"""
Standalone funnel products, rendered with the same brand system:
  1. FREE — The Starter Drop: "Your First AI Character" (lead magnet)
  2. $17 — The Identity Lock Mini-Pack: 20 photo prompts, him + her
Outputs to ../products/.
"""
import json
import os

from reportlab.lib.colors import HexColor

import render
from render import make_styles, build_doc

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, '..', 'products'))

LIME = '#C6FF00'
CYAN = '#00E5FF'

ID_LOCK = ('Use the uploaded image as the exact identity reference. Same '
           'person, same face, same skin tone, same body proportions. '
           'No identity drift.')
REAL = ('Real skin texture, believable shadows and lighting. No plastic '
        'skin, no extra fingers, no warped background.')


def E(t, *lines, **kw):
    d = {'type': t, 'y': 0}
    if lines:
        d['lines'] = list(lines)
    d.update(kw)
    return d


def master_prompts():
    """Pull Prompt 1F and 1M code blocks verbatim from the OS content."""
    pages = json.load(open(os.path.join(HERE, 'content_final.json')))
    blocks = {'F': [], 'M': []}
    for p in pages:
        if p['doc'] != 'MODULE 02':
            continue
        current = None
        for e in p['elems']:
            if e['type'] == 'h3':
                txt = ' '.join(e['lines'])
                if txt.startswith('Prompt 1F'):
                    current = 'F'
                elif txt.startswith('Prompt 1M'):
                    current = 'M'
                else:
                    current = None
            elif e['type'] == 'code' and current:
                blocks[current].append(e)
    return blocks


# ------------------------------------------------------------- starter drop
def starter_pages():
    b = master_prompts()
    cover = {'page': 1, 'doc': 'STARTER', 'elems': [
        E('label', 'FREE STARTER DROP'),
        E('h1', 'YOUR FIRST AI CHARACTER'),
        E('sub', 'Make a face people remember, post your first hook and pin '
                 'your first comment — in about an hour.'),
        E('label', 'CREATE THE CHARACTER. DIRECT THE SCENE. BUILD THE WORLD.'),
    ]}
    p2 = {'page': 2, 'doc': 'STARTER', 'elems': [
        E('h2', 'How this works'),
        E('body', 'This is a free taste of THE SCENE AI Creator OS. '
                  'Three steps. Copy, paste, post.'),
        E('flow', steps=[['1', 'MAKE THE FACE'], ['2', 'POST THE HOOK'],
                         ['3', 'PIN THE COMMENT']],
          caption='About an hour, start to first post.'),
        E('bullet', 'Pick him or her — both prompts are below.'),
        E('bullet', 'Fill in every [BRACKET] with your own words.'),
        E('bullet', 'Run the prompt until you love ONE face. Save that photo. '
                    'That photo is your MASTER — your character’s ID card.'),
        E('bullet', 'From now on, never generate this character without '
                    'uploading the MASTER first.'),
        E('h2', 'Step 1 — Make her face'),
    ] + b['F'] + [
        E('h2', 'Or make his face'),
    ] + b['M']}
    p3 = {'page': 3, 'doc': 'STARTER', 'elems': [
        E('h2', 'Step 2 — Post your first hook'),
        E('body', 'A hook is one normal moment with one thing wrong. '
                  'Generate a short clip or photo of your character in this '
                  'moment, and do not explain it:'),
        E('code', 'Use the uploaded image as the exact identity reference. '
                  'Same person, same face, same skin tone. No identity '
                  'drift. Scene: a server delivers a drink to '
                  '[HIM / HER] from an unknown guest at a nice restaurant. '
                  'Your character reacts with a small, real expression — '
                  'curious, not shocked. Vertical 9:16, natural light, '
                  'shot like phone footage. ' + REAL),
        E('body', 'Caption it with this and nothing else:'),
        E('code', 'Now who sent this over...'),
        E('h2', 'Step 3 — Pin this comment'),
        E('body', 'The comment section is where views turn into followers. '
                  'Post this from your own account and pin it:'),
        E('ccard', note='PIN THIS  —  EVERYONE HAS AN OPINION',
          text='Be honest — would you take the drink or send it back?'),
        E('h2', 'What happens next'),
        E('body', 'Here is the problem you will hit tomorrow: you will '
                  'generate your character again, and the face will drift. '
                  'Different nose, different skin, different person. That is '
                  'the moment most people quit.'),
        E('body', 'THE SCENE AI Creator OS is the fix — 19 modules that lock '
                  'the identity, style the look (him AND her), direct the '
                  'camera, keep Part 2 matching Part 1, and turn one '
                  'character into a world people follow like a show.'),
    ]}
    return [cover, p2, p3]


# ---------------------------------------------------------------- mini pack
SCENES_HER = [
    ('Golden Hour Rooftop', 'standing at a rooftop railing at golden hour, '
     'city skyline behind, wind moving her hair slightly, soft warm light on '
     'her face'),
    ('Coffee Run Candid', 'walking out of a small coffee shop holding an '
     'iced coffee, mid-step, caught-off-guard smile, morning light'),
    ('Car Selfie', 'sitting in the driver’s seat taking a phone selfie, '
     'seatbelt on, daylight through the window, natural makeup'),
    ('Mirror Fit Check', 'taking a full-body mirror photo in a clean bedroom, '
     'phone visible, outfit [OUTFIT], confident relaxed posture'),
    ('Boutique Fitting', 'stepping out of a boutique fitting room in '
     '[OUTFIT], one hand on the curtain, boutique lighting'),
    ('Night Out Arrival', 'stepping out of a car at night in [OUTFIT], city '
     'lights bokeh behind her, flash-photo look'),
    ('Beach Walk', 'walking along the shoreline at late afternoon, sandals '
     'in hand, hair moving in the wind, sun low behind her'),
    ('Kitchen Candid', 'laughing in a bright kitchen while making breakfast, '
     'comfortable at-home outfit, morning window light'),
    ('Gym Session', 'resting between sets on a bench, water bottle in hand, '
     'athletic set, honest post-workout glow, gym lighting'),
    ('Rainy Window', 'sitting by a cafe window on a rainy day, warm drink in '
     'both hands, soft grey daylight, quiet mood'),
]
SCENES_HIM = [
    ('Golden Hour Rooftop', 'leaning on a rooftop railing at golden hour, '
     'city skyline behind him, warm light across his face'),
    ('Coffee Run Candid', 'walking out of a coffee shop with a hot cup, '
     'mid-step, easy confident expression, morning light'),
    ('Car Seat Portrait', 'sitting in the driver’s seat, one hand on the '
     'wheel, daylight through the window, relaxed expression'),
    ('Mirror Fit Check', 'taking a full-body mirror photo in a clean bedroom, '
     'phone visible, outfit [OUTFIT], calm confident stance'),
    ('Barbershop Fresh', 'sitting in a barber chair right after a fresh cut, '
     'cape just removed, checking the line-up in the mirror'),
    ('Night Out Arrival', 'stepping out of a car at night in [OUTFIT], city '
     'lights behind him, flash-photo look'),
    ('Beach Walk', 'walking along the shoreline at late afternoon, relaxed '
     'linen fit, sun low behind him'),
    ('Kitchen Candid', 'cooking in a bright kitchen, sleeves pushed up, '
     'small focused smile, morning window light'),
    ('Gym Session', 'resting between sets, towel over one shoulder, athletic '
     'fit, honest post-workout look, gym lighting'),
    ('Office Hours', 'at a desk by a big window, laptop open, business-casual '
     'fit, golden afternoon light, candid working moment'),
]


def scene_prompt(who, desc):
    return (f'{ID_LOCK} The uploaded {who} is {desc}. Keep the outfit, hair '
            f'and accessories consistent if they appear in the reference. '
            f'Shot like real phone photography, vertical 9:16. {REAL}')


def minipack_pages():
    cover = {'page': 1, 'doc': 'MINIPACK', 'elems': [
        E('label', 'THE IDENTITY LOCK'),
        E('h1', 'MINI-PACK'),
        E('sub', '20 photo prompts that keep the same face in every single '
                 'shot. Ten for her, ten for him.'),
        E('label', 'CREATE THE CHARACTER. DIRECT THE SCENE. BUILD THE WORLD.'),
    ]}
    intro = {'page': 2, 'doc': 'MINIPACK', 'elems': [
        E('h2', 'How to use this pack'),
        E('bullet', 'Upload your MASTER photo first. Every time. No exceptions.'),
        E('bullet', 'Fill in every [BRACKET] with your own words.'),
        E('bullet', 'Every prompt already carries the identity lock — the '
                    'sentence that stops the face from changing.'),
        E('bullet', 'If the face drifts anyway, reply: "Same person as the '
                    'uploaded image. Do not change the face." and run it again.'),
        E('label', 'THE IDENTITY LOCK — THIS SENTENCE IS THE PRODUCT'),
        E('code', ID_LOCK),
        E('body', 'You will see it at the start of all 20 prompts below. '
                  'That repetition is not lazy — it is the technique.'),
    ]}
    her = {'page': 3, 'doc': 'MINIPACK', 'elems': [E('h2', 'For her — 10 scenes')]}
    for i, (name, desc) in enumerate(SCENES_HER, 1):
        her['elems'].append(E('h3', f'{i:02d}. {name}'))
        her['elems'].append(E('code', scene_prompt('woman', desc)))
    him = {'page': 4, 'doc': 'MINIPACK', 'elems': [E('h2', 'For him — 10 scenes')]}
    for i, (name, desc) in enumerate(SCENES_HIM, 11):
        him['elems'].append(E('h3', f'{i:02d}. {name}'))
        him['elems'].append(E('code', scene_prompt('man', desc)))
    outro = {'page': 5, 'doc': 'MINIPACK', 'elems': [
        E('h2', 'Photos are step one'),
        E('body', 'These 20 prompts keep the face locked in photos. The full '
                  'Creator OS goes further: video, story episodes, outfits '
                  'and hair for him and her, camera direction, and the '
                  'continuity system that makes Part 2 match Part 1.'),
    ]}
    return [cover, intro, her, him, outro]


def main():
    render.register_fonts()
    os.makedirs(OUT, exist_ok=True)

    STORE = 'https://stan.store/thesceneai'
    jobs = [
        ('STARTER', starter_pages(), LIME,
         {'kicker': 'FREE STARTER DROP', 'title': 'YOUR FIRST AI CHARACTER',
          'sub': 'Make a face people remember, post your first hook and pin '
                 'your first comment — in about an hour.',
          'tagline': 'CREATE THE CHARACTER. DIRECT THE SCENE. BUILD THE WORLD.'},
         'The-SCENE-AI_FREE_Starter-Drop_Your-First-AI-Character.pdf'),
        ('MINIPACK', minipack_pages(), CYAN,
         {'kicker': 'IDENTITY LOCK', 'title': 'MINI-PACK',
          'sub': '20 photo prompts that keep the same face in every single '
                 'shot. Ten for her, ten for him.',
          'tagline': 'CREATE THE CHARACTER. DIRECT THE SCENE. BUILD THE WORLD.'},
         'The-SCENE-AI_Identity-Lock-Mini-Pack.pdf'),
    ]
    for docid, pages, accent, meta_extra, fname in jobs:
        S = make_styles(HexColor(accent))
        meta = {'accent': HexColor(accent), 'accent_hex': accent,
                'part': 0, 'total': 0, 'next': None,
                'banner': ('NEXT STEP — TAP THIS BANNER',
                           'Get THE SCENE AI — the full Creator OS'),
                'banner_url': STORE,
                'cover_page': pages[0]}
        meta.update(meta_extra)
        build_doc(docid, pages, meta, os.path.join(OUT, fname), S)
        print('wrote', fname)


if __name__ == '__main__':
    main()
