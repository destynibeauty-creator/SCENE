#!/usr/bin/env python3
"""THE SCENE AI — Drop 003 (October 2026): The Halloween Drop."""
import os

from reportlab.lib.colors import HexColor

import render
from render import make_styles, build_doc

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, '..', 'products'))
LIME = '#C6FF00'

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


COSTUME_REVEAL = [
    'The last piece of the costume won’t sit right until the mirror catches it just once.',
    'The lighting changes the second the wig goes on, like the room knew first.',
    'A friend knocks mid-transformation and refuses to look until it’s finished.',
    'The costume box has one extra piece nobody remembers ordering.',
    'The mirror fogs at the edges right as the look comes together.',
    'A single photo gets taken before the reveal. It never gets shown to anyone.',
    'The door reveal gets delayed three times before it finally happens.',
    'Someone films the countdown and the character makes them wait anyway.',
    'The final accessory doesn’t match anything else, and that’s exactly the point.',
    'The reveal happens in one continuous turn, no cuts, no retakes.',
]
HAUNTED_NIGHT = [
    'The haunted house line moves fast until it reaches the character’s group.',
    'A actor in character breaks for one second, just for the character.',
    'The party’s fog machine times perfectly with the character’s entrance.',
    'Someone in an identical costume stands across the room, unmoving.',
    'The DJ drops the one song the whole group has been waiting for.',
    'A prize for “best costume” gets announced before the judging even starts.',
    'The haunted maze has one hallway that isn’t on the map they handed out.',
    'A stranger in costume says “finally” like they were expected.',
    'The group photo has one extra shadow nobody can explain.',
    'The last room of the haunted house is simply empty. And that’s worse.',
]
FALL_DATE_NIGHT = [
    'The pumpkin patch has one pumpkin set aside with the character’s name chalked on it.',
    'The apple orchard worker waves the character through without a ticket.',
    'A hayride stops for exactly one photo and starts again.',
    'The cider stand runs out of everything except the character’s order.',
    'Fall leaves fall in frame on cue, like the season timed it.',
    'A corn maze dead-ends at a bench that wasn’t there on the map.',
    'The bonfire gets lit the second the character sits down.',
    'A caramel apple gets handed over already wrapped with a name on it.',
    'The golden hour light holds two minutes longer than it should.',
    'The drive home takes the long way, on purpose, past every lit-up porch.',
]

OUTFITS_HER = [
    ('Classic Glam Witch', 'an elevated witch costume, fitted black corset '
     'dress, statement pointed hat, sheer cape, dramatic jewelry'),
    ('Vintage Pin-Up Vampire', 'a fitted red-and-black vampire dress, '
     'opera gloves, dramatic choker, deep red lip'),
    ('Cozy Cat', 'a chic cat-ear headband, fitted black bodysuit, sheer '
     'tights, ankle boots, minimal gold jewelry'),
    ('Fallen Angel', 'a white corset gown, feathered wings, soft silver '
     'jewelry, loose waved hair'),
    ('Orchard Casual', 'an oversized flannel over a fitted top, denim '
     'shorts and tights, ankle boots, a knit beanie'),
]
OUTFITS_HIM = [
    ('Classic Vampire', 'a fitted black suit with a dramatic collar cape, '
     'statement rings, slicked-back hair'),
    ('Greek God', 'a draped toga-style wrap, gold cuff bracelet, laurel '
     'leaf crown, sandals'),
    ('Cozy Werewolf', 'a textured fur-accent jacket over a fitted tee, '
     'dark denim, boots'),
    ('Dark Knight', 'a fitted black armor-style jacket, leather gloves, '
     'dark trousers, boots'),
    ('Orchard Casual', 'a flannel over a plain tee, dark denim, work '
     'boots, a knit beanie'),
]


def outfit_prompt(who, desc):
    return (f'{ID_LOCK} Style the uploaded {who} in {desc}. Keep the face, '
            f'hair and body exactly as the reference. Shot like real phone '
            f'photography, vertical 9:16. {REAL}')


COSTUME_REVEAL_SCENE = """REFERENCE IMAGES (USE ALL REFERENCES TOGETHER)

Reference 1 — Identity Reference (Highest Priority)
Use this image as the exact identity source. Preserve the exact face, skin tone, ethnicity, facial structure, eyes, nose, lips, eyebrows, hairline, hairstyle, eyelashes, body proportions, and overall appearance. Do not beautify, face swap, or alter the identity in any way. Maintain the exact same identity from the first frame to the last frame.

Reference 2 — Costume Reference
Use this image as the exact wardrobe reference.
Preserve:
- [COSTUME PIECE 1]
- [COSTUME PIECE 2]
- [ACCESSORY]
- [SHOES]
- [MAKEUP STYLE — if applicable]

Reference 3 — Location Reference
Use this image as the exact location. The video begins in this [ROOM / HALLWAY / DOORWAY].

IDENTITY LOCK (HIGHEST PRIORITY)
Use the uploaded identity reference as the exact person. Preserve the same face, skin tone, ethnicity, facial structure, eyes, nose, lips, eyebrows, hairline, hairstyle, eyelashes, body proportions, and overall appearance. Do not beautify, face swap, or alter the identity. No face drift. No identity drift. Maintain the exact same identity throughout the entire video.

CAMERA
Filmed on [YOUR PHONE MODEL] front-facing camera. Vertical 9:16. Generate in native 4K. 60 FPS. Natural HDR. Default phone color science. Authentic handheld selfie. Very slight handheld movement. Tiny autofocus breathing. Natural exposure adjustments. Slight rolling shutter. Looks exactly like genuine phone footage uploaded directly to Instagram. No cinematic filters. No beauty filters. No skin smoothing.

HANDS
The phone is naturally held in [HER / HIS] right hand. Do not generate a second phone. Do not generate another camera. Do not generate any additional recording devices.

SCENE
The video begins with the character standing just out of frame of a mirror or doorway, costume already on.
[SHE / HE] takes a breath and says, "[LINE 1 — e.g. Okay, here we go...]"
[SHE / HE] turns to face the mirror or steps through the doorway, revealing the full costume.
Hold the reveal naturally for about two seconds.
[SHE / HE] smiles at the reflection or camera and says, "[LINE 2 — the line people will comment about]"
The clip ends naturally on the reveal.

MOVEMENT
Natural posture. Natural shoulder, arm and hip movement. Natural breathing. Natural blinking. Natural facial expressions. The costume flows naturally. Nothing appears robotic or overly animated.

REALISM (HIGHEST PRIORITY)
The final result must be visually indistinguishable from authentic phone footage. Ultra-photorealistic 4K quality. Natural skin texture. Visible pores. Subtle baby hairs. Natural facial texture. Realistic eye reflections. Natural teeth. Correct hand anatomy. Correct finger anatomy. Natural fingernails. Physically accurate lighting. Realistic shadows. Consistent identity throughout every frame. No face morphing. No identity drift. No flickering. No warping. No duplicated limbs. No extra fingers. No plastic skin. No AI artifacts.

ATMOSPHERE
[SETTING — e.g. dim warm bedroom light, string lights in the background]. Natural environmental audio only. No background music. No sound effects. Natural speaking voice.

LENGTH
15 seconds.

STYLE
The first three seconds must create immediate curiosity through a natural, unstaged feel. The pacing should feel effortless, like the character instinctively turned to show someone the finished look. The video should look so authentic that viewers question whether it is AI or a real costume reveal."""


def pages():
    cover = {'page': 1, 'doc': 'DROP 003', 'elems': [
        E('label', 'THE SCENE AI · DROP 003 · OCTOBER'),
        E('h1', 'THE HALLOWEEN DROP'),
        E('sub', '30 new scenes, 10 new looks, and this month’s master '
                 'scene — members only.'),
        E('label', 'CREATE THE CHARACTER. DIRECT THE SCENE. BUILD THE WORLD.'),
    ]}
    p2 = {'page': 2, 'doc': 'DROP 003', 'elems': [
        E('h2', 'What’s in this drop'),
        E('flow', steps=[['1', '30 NEW SCENES'], ['2', '10 NEW LOOKS'],
                         ['3', 'MASTER SCENE'], ['4', 'TOOL NOTES']],
          caption='Run one scene a day and this drop is a full month of content.'),
        E('body', 'Everything works exactly like the Creator OS: upload your '
                  'MASTER, fill in the [BRACKETS], copy, paste, post.'),
        E('h2', 'Costume reveal — 10 scenes'),
    ] + [E('body', f'{i:02d}. {s}') for i, s in enumerate(COSTUME_REVEAL, 1)] + [
        E('h2', 'Haunted night out — 10 scenes'),
    ] + [E('body', f'{i:02d}. {s}') for i, s in enumerate(HAUNTED_NIGHT, 1)] + [
        E('h2', 'Fall date night — 10 scenes'),
    ] + [E('body', f'{i:02d}. {s}') for i, s in enumerate(FALL_DATE_NIGHT, 1)]}
    p3 = {'page': 3, 'doc': 'DROP 003', 'elems': [
        E('h2', 'The October looks — 5 for her'),
    ]}
    for i, (name, desc) in enumerate(OUTFITS_HER, 1):
        p3['elems'].append(E('h3', f'{i:02d}. {name}'))
        p3['elems'].append(E('code', outfit_prompt('woman', desc)))
    p4 = {'page': 4, 'doc': 'DROP 003', 'elems': [
        E('h2', 'The October looks — 5 for him'),
    ]}
    for i, (name, desc) in enumerate(OUTFITS_HIM, 6):
        p4['elems'].append(E('h3', f'{i:02d}. {name}'))
        p4['elems'].append(E('code', outfit_prompt('man', desc)))
    p5 = {'page': 5, 'doc': 'DROP 003', 'elems': [
        E('h2', 'Master scene of the month: The Costume Reveal'),
        E('body', 'A complete, filled-out Director’s Master Template. Swap '
                  'the brackets for your character and your costume, '
                  'attach your references, and paste the whole thing into '
                  'your video tool.'),
        E('code', COSTUME_REVEAL_SCENE),
    ]}
    p6 = {'page': 6, 'doc': 'DROP 003', 'elems': [
        E('h2', 'Tool notes — October'),
        E('bullet', 'The 3-step method still applies: an idea chat first, '
                    'real reference photos (costume inspo, real haunted '
                    'house or orchard photos), then your locked character '
                    'chat to combine them.'),
        E('bullet', 'Batch mode: ask for 10 variations at once instead of '
                    'one at a time, then refine with short follow-ups like '
                    '"batch mode 10 more, make the cape longer."'),
        E('bullet', 'Video: Seedance 2.5 syncs lips best on clips of 10 '
                    'seconds or less. Keep spoken lines 5–10 words.'),
        E('bullet', 'Photos: batch your poses in Nano Banana Pro or '
                    'Seedream 4.5 right after you lock a new costume — 6 '
                    'to 10 angles per look.'),
        E('h2', 'Member mission'),
        E('body', 'Post ONE scene from this drop with #THESCENEAI. The best '
                  'episode gets reposted and broken down in next month’s '
                  'drop.'),
    ]}
    return [cover, p2, p3, p4, p5, p6]


def main():
    render.register_fonts()
    os.makedirs(OUT, exist_ok=True)
    S = make_styles(HexColor(LIME))
    meta = {'kicker': 'THE SCENE AI · DROP 003', 'title': 'THE HALLOWEEN DROP',
            'sub': '30 new scenes, 10 new looks, and this month’s master '
                   'scene — members only.',
            'tagline': 'CREATE THE CHARACTER. DIRECT THE SCENE. BUILD THE WORLD.',
            'accent': HexColor(LIME), 'accent_hex': LIME,
            'part': 0, 'total': 0, 'next': None,
            'banner': ('NEXT DROP', 'Drop 004 lands next month. Post with #THESCENEAI.'),
            'banner_url': 'https://www.skool.com/thesceneai/about',
            'cover_page': None, 'closing': True}
    ps = pages()
    meta['cover_page'] = ps[0]
    build_doc('DROP 003', ps, meta,
              os.path.join(OUT, 'THE-SCENE-AI_Drop-003_The-Halloween-Drop.pdf'), S)
    print('wrote THE-SCENE-AI_Drop-003_The-Halloween-Drop.pdf')


if __name__ == '__main__':
    main()
