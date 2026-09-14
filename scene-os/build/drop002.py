#!/usr/bin/env python3
"""THE SCENE AI — Drop 002 (September 2026): The WWE Fan Day Drop."""
import os

from reportlab.lib.colors import HexColor

import render
from render import make_styles, build_doc

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, '..', 'products'))
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


RINGSIDE = [
    'The seat upgrade lands two rows from the ring, no explanation given.',
    'Security waves the character past the line like they already know the face.',
    'A wrestler points straight into the crowd mid-entrance. Right at the character.',
    'The jumbotron holds on the character’s reaction one second too long.',
    'A staff member hands over a signed item nobody remembers ordering.',
    'The lights cut mid-match and a phone flashlight is the only light in the row.',
    'A championship belt gets passed down the row and stops at the character.',
    'The character’s chant gets picked up by the entire section.',
    'Confetti falls and the character is standing exactly under it.',
    'The post-match walkout route passes one row. It’s the character’s.',
]
PHOTO_BOOTH = [
    'The photo booth print comes out doubled, like there were two of them in frame.',
    'The merch stand is sold out of everything except the one item they wanted.',
    'A staff member swaps the backdrop right as the flash goes off.',
    'The receipt prints a message instead of a total.',
    'The line for the photo booth clears the second the character steps up.',
    'A stranger asks to be in the photo, then is gone before it prints.',
    'The merch bag is heavier than what was actually bought.',
    'The photo strip shows a fourth frame nobody posed for.',
    'A vendor gives the “employee” discount without being asked.',
    'The souvenir cup changes color and nobody explains why.',
]
BACKSTAGE = [
    'The wristband grants access to a hallway that isn’t on the map.',
    'A crew member says “you’re already on the list” before a name is given.',
    'The greenroom door is left open, just for one row of seats.',
    'A signed photo is already personalized with the character’s name.',
    'The meet and greet line moves fast until it’s the character’s turn, then it stops.',
    'Someone backstage uses a nickname nobody has ever called the character.',
    'A production assistant hands over an earpiece “just in case.”',
    'The autograph table has one seat left. Reserved.',
    'The tour guide skips the group and takes the character down one hallway alone.',
    'A locker room door has the character’s name taped on it. Temporarily.',
]

OUTFITS_HER = [
    ('Ringside Glam', 'a fitted graphic tee tied at the waist over bike '
     'shorts, chunky sneakers, an oversized event bomber jacket'),
    ('Photo Booth Ready', 'a fitted long-sleeve top with a small heart '
     'print, matching leggings, fuzzy slides, a soft bucket hat'),
    ('VIP Meet and Greet', 'a fitted bodysuit with high-waisted jeans, a '
     'statement belt buckle, ankle boots'),
    ('Merch Table Casual', 'an oversized event hoodie worn as a dress, '
     'thigh-high socks, chunky sneakers'),
    ('Arena Night', 'a leather moto jacket over a graphic crop top, cargo '
     'pants, combat boots'),
]
OUTFITS_HIM = [
    ('Ringside Fit', 'a fitted graphic tee, joggers, retro sneakers, a '
     'snapback'),
    ('Champion Energy', 'an open track jacket over a tank, athletic shorts, '
     'high socks, slides'),
    ('VIP Meet and Greet', 'a fitted button-up worn open over a plain tee, '
     'tapered jeans, clean sneakers'),
    ('Merch Stand Casual', 'an oversized hoodie, cargo shorts, crew socks, '
     'sneakers'),
    ('Arena Night', 'a leather jacket over a fitted tee, dark denim, boots'),
]


def outfit_prompt(who, desc):
    return (f'{ID_LOCK} Style the uploaded {who} in {desc}. Keep the face, '
            f'hair and body exactly as the reference. Shot like real phone '
            f'photography, vertical 9:16. {REAL}')


PHOTO_BOOTH_SCENE = """REFERENCE IMAGES (USE ALL REFERENCES TOGETHER)

Reference 1 — Identity Reference (Highest Priority)
Use this image as the exact identity source. Preserve the exact face, skin tone, ethnicity, facial structure, eyes, nose, lips, eyebrows, hairline, hairstyle, eyelashes, body proportions, and overall appearance. Do not beautify, face swap, or alter the identity in any way. Maintain the exact same identity from the first frame to the last frame.

Reference 2 — Outfit Reference
Use this image as the exact wardrobe reference.
Preserve:
- [TOP OR SET]
- [BAG OR ACCESSORY]
- [HAT — worn or in hand]
- [SHOES]
- [JEWELRY]

Reference 3 — Location Reference (real event photo)
Use this image as the exact location. This is a real photo booth setup from a live event. Match the backdrop, lighting rig, flooring, and booth structure exactly.

IDENTITY LOCK (HIGHEST PRIORITY)
Use the uploaded identity reference as the exact person. Preserve the same face, skin tone, ethnicity, facial structure, eyes, nose, lips, eyebrows, hairline, hairstyle, eyelashes, body proportions, and overall appearance. Do not beautify, face swap, or alter the identity. No face drift. No identity drift. Maintain the exact same identity throughout the entire video.

CAMERA
Filmed on [YOUR PHONE MODEL] front-facing camera. Vertical 9:16. Generate in native 4K. 60 FPS. Natural HDR. Default phone color science. Authentic handheld selfie. Very slight handheld movement. Tiny autofocus breathing. Natural exposure adjustments. Slight rolling shutter. Looks exactly like genuine phone footage uploaded directly to Instagram. No cinematic filters. No beauty filters. No skin smoothing.

HANDS
The phone is naturally held in [HER / HIS] right hand. The left hand naturally rests on [THE BAG / HIP]. Do not generate a second phone. Do not generate another camera. Do not generate any additional recording devices.

SCENE
The video begins with the character stepping up to the photo booth line.
[SHE / HE] glances at the backdrop and says, "[LINE 1 — e.g. Wait, this is actually so cute...]"
The booth attendant waves them forward.
[SHE / HE] steps in, poses once, and the flash goes off.
[SHE / HE] turns the phone to show the printed strip and says, "[LINE 2 — the line people will comment about]"
The clip ends naturally on the printed photo strip in hand.

MOVEMENT
Natural posture. Natural shoulder, arm and hip movement. Natural breathing. Natural blinking. Natural facial expressions. The outfit flows naturally. Nothing appears robotic or overly animated.

REALISM (HIGHEST PRIORITY)
The final result must be visually indistinguishable from authentic phone footage. Ultra-photorealistic 4K quality. Natural skin texture. Visible pores. Subtle baby hairs. Natural facial texture. Realistic eye reflections. Natural teeth. Correct hand anatomy. Correct finger anatomy. Natural fingernails. Physically accurate lighting. Realistic shadows. Consistent identity throughout every frame. No face morphing. No identity drift. No flickering. No warping. No duplicated limbs. No extra fingers. No plastic skin. No AI artifacts.

ATMOSPHERE
[SETTING — e.g. a packed live event, string lights and event signage in the background]. Natural environmental audio only. No background music. No sound effects. Natural speaking voice.

LENGTH
15 seconds.

STYLE
The first three seconds must create immediate curiosity through a natural, unstaged feel. The pacing should feel effortless, like the character instinctively grabbed the phone to show someone the photo strip. The video should look so authentic that viewers question whether it is AI or a real event vlog."""


def pages():
    cover = {'page': 1, 'doc': 'DROP 002', 'elems': [
        E('label', 'THE SCENE AI · DROP 002 · SEPTEMBER'),
        E('h1', 'THE WWE FAN DAY DROP'),
        E('sub', '30 new scenes, 10 new looks, and this month’s master '
                 'scene — members only.'),
        E('label', 'CREATE THE CHARACTER. DIRECT THE SCENE. BUILD THE WORLD.'),
    ]}
    p2 = {'page': 2, 'doc': 'DROP 002', 'elems': [
        E('h2', 'What’s in this drop'),
        E('flow', steps=[['1', '30 NEW SCENES'], ['2', '10 NEW LOOKS'],
                         ['3', 'MASTER SCENE'], ['4', 'TOOL NOTES']],
          caption='Run one scene a day and this drop is a full month of content.'),
        E('body', 'Everything works exactly like the Creator OS: upload your '
                  'MASTER, fill in the [BRACKETS], copy, paste, post.'),
        E('h2', 'Ringside + arena — 10 scenes'),
    ] + [E('body', f'{i:02d}. {s}') for i, s in enumerate(RINGSIDE, 1)] + [
        E('h2', 'Photo booth + merch — 10 scenes'),
    ] + [E('body', f'{i:02d}. {s}') for i, s in enumerate(PHOTO_BOOTH, 1)] + [
        E('h2', 'Meet and greet + backstage — 10 scenes'),
    ] + [E('body', f'{i:02d}. {s}') for i, s in enumerate(BACKSTAGE, 1)]}
    p3 = {'page': 3, 'doc': 'DROP 002', 'elems': [
        E('h2', 'The September looks — 5 for her'),
    ]}
    for i, (name, desc) in enumerate(OUTFITS_HER, 1):
        p3['elems'].append(E('h3', f'{i:02d}. {name}'))
        p3['elems'].append(E('code', outfit_prompt('woman', desc)))
    p4 = {'page': 4, 'doc': 'DROP 002', 'elems': [
        E('h2', 'The September looks — 5 for him'),
    ]}
    for i, (name, desc) in enumerate(OUTFITS_HIM, 6):
        p4['elems'].append(E('h3', f'{i:02d}. {name}'))
        p4['elems'].append(E('code', outfit_prompt('man', desc)))
    p5 = {'page': 5, 'doc': 'DROP 002', 'elems': [
        E('h2', 'Master scene of the month: The Photo Booth Reveal'),
        E('body', 'A complete, filled-out Director’s Master Template. Swap '
                  'the brackets for your character and a real event photo, '
                  'attach your references, and paste the whole thing into '
                  'your video tool.'),
        E('code', PHOTO_BOOTH_SCENE),
    ]}
    p6 = {'page': 6, 'doc': 'DROP 002', 'elems': [
        E('h2', 'Tool notes — September'),
        E('bullet', 'The 3-step method behind this drop: an idea chat first '
                    '(no character, just ask for scene ideas), then real '
                    'reference photos from an actual event, then your '
                    'locked character chat to combine them.'),
        E('bullet', 'Batch mode: ask for 10 variations at once instead of '
                    'one at a time, then refine with short follow-ups like '
                    '"batch mode 10 more, make the jacket black instead."'),
        E('bullet', 'Video: Seedance 2.5 syncs lips best on clips of 10 '
                    'seconds or less. Keep spoken lines 5–10 words.'),
        E('bullet', 'Photos: batch your poses in Nano Banana Pro or '
                    'Seedream 4.5 right after you lock a new outfit — 6 to '
                    '10 angles per look.'),
        E('h2', 'Member mission'),
        E('body', 'Post ONE scene from this drop with #THESCENEAI. The best '
                  'episode gets reposted and broken down in next month’s '
                  'drop.'),
    ]}
    return [cover, p2, p3, p4, p5, p6]


def main():
    render.register_fonts()
    os.makedirs(OUT, exist_ok=True)
    S = make_styles(HexColor(CYAN))
    meta = {'kicker': 'THE SCENE AI · DROP 002', 'title': 'THE WWE FAN DAY DROP',
            'sub': '30 new scenes, 10 new looks, and this month’s master '
                   'scene — members only.',
            'tagline': 'CREATE THE CHARACTER. DIRECT THE SCENE. BUILD THE WORLD.',
            'accent': HexColor(CYAN), 'accent_hex': CYAN,
            'part': 0, 'total': 0, 'next': None,
            'banner': ('NEXT DROP', 'Drop 003 lands next month. Post with #THESCENEAI.'),
            'banner_url': 'https://www.skool.com/thesceneai/about',
            'cover_page': None, 'closing': True}
    ps = pages()
    meta['cover_page'] = ps[0]
    build_doc('DROP 002', ps, meta,
              os.path.join(OUT, 'THE-SCENE-AI_Drop-002_The-WWE-Fan-Day-Drop.pdf'), S)
    print('wrote THE-SCENE-AI_Drop-002_The-WWE-Fan-Day-Drop.pdf')


if __name__ == '__main__':
    main()
