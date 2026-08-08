#!/usr/bin/env python3
"""THE SCENE AI — Drop 001 (August 2026): The Vacation Heat Drop."""
import os

from reportlab.lib.colors import HexColor

import render
from render import make_styles, build_doc

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, '..', 'products'))
MAG = '#F600A2'

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


VACATION = [
    'The room key does not open a room. It opens a rooftop.',
    'The resort staff greets the character by a nickname nobody uses anymore.',
    'A cabana has a reserved sign with today’s date — booked a year ago.',
    'The vacation photos show someone in the background at every location.',
    'The character orders one drink. Two arrive. The server just smiles.',
    'A jet-ski pulls up to the beach with an empty seat.',
    'The hotel upgrade comes with one condition: dinner at eight.',
    'A message in the sand is half-washed away before the reveal.',
    'The infinity pool is closed for a private event. The character is the event.',
    'The luggage arrives at the villa before the character even lands.',
]
NIGHTLIFE = [
    'The table in the back has been paid for all summer. Nobody sits there.',
    'The DJ takes one request all night. It is the character’s song.',
    'A stranger sends over dessert with the check already inside the box.',
    'The rooftop bar rains at midnight. Nobody leaves.',
    'The valet brings a car that is not the one they dropped off.',
    'The maître d’ says, “Your usual?” It is the character’s first time.',
    'A birthday sparkler arrives. It is not the character’s birthday. Yet.',
    'The elevator to the lounge needs a code. The character has it. Why?',
    'Last call comes and one table gets fresh menus.',
    'Someone leaves the club early. Their seat stays guarded all night.',
]
GLOWUP = [
    'The “before” photo falls out of the mirror frame mid-routine.',
    'A client books the last appointment and asks for a total transformation — no photos allowed.',
    'The character does the whole routine in silence. The results speak.',
    'The stylist stops mid-cut, walks away, and comes back with the owner.',
    'One product on the shelf is turned backwards. It is the one that works.',
    'A voice note plays during the glow-up: “You won’t recognize her.”',
    'The appointment book has a name in it from five years ago. Today.',
    'The mirror reveal is filmed — but the reaction is the only thing shown.',
    'The character teaches ONE technique. The comments beg for the rest.',
    'The final look is covered by a coat until the last second. The door opens.',
]

OUTFITS_HER = [
    ('White-Hot Resort Set', 'an all-white linen shirt-and-shorts resort set, '
     'gold jewelry, flat leather sandals, oversized sunglasses on top of the head'),
    ('Sunset Slip Dress', 'a silk slip dress in sunset orange, small gold hoops, '
     'strappy heels carried in one hand on the sand'),
    ('Pool Day Crochet', 'a crochet cover-up over a matching swimsuit, raffia '
     'tote, platform sandals, small gold anklet'),
    ('Night Out Satin', 'a satin corset top with tailored shorts, a mini '
     'shoulder bag, heeled mules, sleek jewelry'),
    ('Airport Comfort Luxe', 'a matching knit set with white sneakers, a '
     'structured carry-on, minimal jewelry, silk headscarf'),
]
OUTFITS_HIM = [
    ('Linen Set Clean', 'an open linen shirt over a fitted tank with matching '
     'linen pants, leather slides, one chain'),
    ('Marina Nights', 'a knitted polo with tailored trousers and loafers, '
     'no socks, a leather-strap watch'),
    ('Pool Deck Fresh', 'swim trunks with an open terry-cloth shirt, sport '
     'sunglasses, one ring, clean slides'),
    ('Rooftop Blazer', 'an unstructured blazer over a plain tee with cropped '
     'trousers and minimal sneakers'),
    ('Airport Layover', 'a heavyweight tee with cargo pants, running sneakers, '
     'a duffel over one shoulder, simple chain'),
]


def outfit_prompt(who, desc):
    return (f'{ID_LOCK} Style the uploaded {who} in {desc}. Keep the face, '
            f'hair and body exactly as the reference. Shot like real phone '
            f'photography, vertical 9:16. {REAL}')


PENTHOUSE = """REFERENCE IMAGES (USE ALL REFERENCES TOGETHER)

Reference 1 — Identity Reference (Highest Priority)
Use this image as the exact identity source. Preserve the exact face, skin tone, ethnicity, facial structure, eyes, nose, lips, eyebrows, hairline, hairstyle, eyelashes, body proportions, and overall appearance. Do not beautify, face swap, or alter the identity in any way. Maintain the exact same identity from the first frame to the last frame.

Reference 2 — Hair Reference
Use this image to preserve the exact hairstyle, color, texture, density, edges, parting, and overall hair appearance. Hair must remain consistent throughout the video.

Reference 3 — Outfit Reference
Use this image as the exact wardrobe reference.
Preserve:
- [SWIM OR RESORT SET]
- [COVER-UP OR SHIRT]
- [BAG]
- [SUNGLASSES — resting on top of the head only]
- [SHOES]
- [JEWELRY]

Reference 4 — Suite Interior Reference
Use this image as the exact interior location. The video begins inside this [SUITE / VILLA / PENTHOUSE].
Preserve:
- [FLOORS]
- [WINDOWS]
- [FURNITURE]
- [LIGHT]
- [VIEW]

Reference 5 — Rooftop / Pool Reference
Use this image as the exact second location. The transition from the interior to this space must feel completely seamless and realistic.

IDENTITY LOCK (HIGHEST PRIORITY)
Use the uploaded identity reference as the exact person. Preserve the same face, skin tone, ethnicity, facial structure, eyes, nose, lips, eyebrows, hairline, hairstyle, eyelashes, body proportions, and overall appearance. Do not beautify, face swap, or alter the identity. No face drift. No identity drift. Maintain the exact same identity throughout the entire video.

CAMERA
Filmed on [YOUR PHONE MODEL] front-facing camera. Vertical 9:16. Generate in native 4K. 60 FPS. Natural HDR. Default phone color science. Authentic handheld selfie. Very slight handheld movement. Tiny autofocus breathing. Natural exposure adjustments. Slight rolling shutter. Natural motion blur while walking. Looks exactly like genuine phone footage uploaded directly to Instagram. No cinematic filters. No beauty filters. No skin smoothing. No over-sharpening.

HANDS
The phone is naturally held in [HER / HIS] right hand. The left hand naturally carries [THE BAG] while walking. Do not generate a second phone. Do not generate another camera. Do not generate a selfie stick. Do not generate any additional recording devices.

SCENE
The video begins inside the [SUITE].
[SHE / HE] stands in front of the sliding glass doors, sunlight pouring in from behind.
[SHE / HE] smiles, reaches for the handle, and quietly says, "[LINE 1 — e.g. Hold on...]"
[SHE / HE] slides the door open and walks out.
[SHE / HE] turns the phone away to reveal the [ROOFTOP / POOL / VIEW].
Hold the reveal naturally for about two seconds.
[SHE / HE] turns the phone back, smiles in disbelief, and says, "[LINE 2 — e.g. Nah...]"
[SHE / HE] walks over, sets the bag down, sits at the edge and dips both feet in.
Then quietly says, "[LINE 3 — the line people will comment about]"
The clip ends naturally.

MOVEMENT
[SHE / HE] moves at a relaxed vacation pace. Natural posture. Natural shoulder, arm and hip movement. Natural breathing. Natural blinking. Natural facial expressions. The outfit flows naturally. The hair moves naturally with the breeze. Nothing appears robotic or overly animated.

REALISM (HIGHEST PRIORITY)
The final result must be visually indistinguishable from authentic phone footage. Ultra-photorealistic 4K quality. Natural skin texture. Visible pores. Subtle baby hairs. Natural facial texture. Natural lip texture. Realistic eye reflections. Natural teeth. Correct hand anatomy. Correct finger anatomy. Natural fingernails. Realistic muscle movement. Natural body proportions. Physically accurate lighting. Authentic sunlight. Realistic shadows. Natural reflections. Consistent identity throughout every frame. No face morphing. No identity drift. No flickering. No ghosting. No warping. No floating objects. No duplicated limbs. No extra fingers. No plastic skin. No waxy skin. No AI artifacts.

ATMOSPHERE
[SETTING — e.g. bright summer afternoon in your dream city]. [AIR — e.g. warm ocean breeze]. [BACKGROUND MOTION — e.g. palm trees moving gently]. [SOUNDS — e.g. soft waves, occasional seagulls]. Natural environmental audio only. No background music. No sound effects. Natural speaking voice.

LENGTH
15 seconds.

STYLE
The first three seconds must create immediate curiosity through a natural reveal. The pacing should feel effortless, as if [SHE / HE] instinctively grabbed the phone to show someone something incredible. The video should look so authentic that viewers genuinely question whether it is AI or a real luxury vacation vlog."""


def pages():
    cover = {'page': 1, 'doc': 'DROP 001', 'elems': [
        E('label', 'THE SCENE AI · DROP 001 · AUGUST'),
        E('h1', 'THE VACATION HEAT DROP'),
        E('sub', '30 new scenes, 10 new looks, and this month’s master '
                 'scene — members only.'),
        E('label', 'CREATE THE CHARACTER. DIRECT THE SCENE. BUILD THE WORLD.'),
    ]}
    p2 = {'page': 2, 'doc': 'DROP 001', 'elems': [
        E('h2', 'What’s in this drop'),
        E('flow', steps=[['1', '30 NEW SCENES'], ['2', '10 NEW LOOKS'],
                         ['3', 'MASTER SCENE'], ['4', 'TOOL NOTES']],
          caption='Run one scene a day and this drop is a full month of content.'),
        E('body', 'Everything works exactly like the Creator OS: upload your '
                  'MASTER, fill in the [BRACKETS], copy, paste, post.'),
        E('h2', 'Summer vacation — 10 scenes'),
    ] + [E('body', f'{i:02d}. {s}') for i, s in enumerate(VACATION, 1)] + [
        E('h2', 'Nightlife + dinner — 10 scenes'),
    ] + [E('body', f'{i:02d}. {s}') for i, s in enumerate(NIGHTLIFE, 1)] + [
        E('h2', 'Glow-up + beauty — 10 scenes'),
    ] + [E('body', f'{i:02d}. {s}') for i, s in enumerate(GLOWUP, 1)]}
    p3 = {'page': 3, 'doc': 'DROP 001', 'elems': [
        E('h2', 'The August looks — 5 for her'),
    ]}
    for i, (name, desc) in enumerate(OUTFITS_HER, 1):
        p3['elems'].append(E('h3', f'{i:02d}. {name}'))
        p3['elems'].append(E('code', outfit_prompt('woman', desc)))
    p4 = {'page': 4, 'doc': 'DROP 001', 'elems': [
        E('h2', 'The August looks — 5 for him'),
    ]}
    for i, (name, desc) in enumerate(OUTFITS_HIM, 6):
        p4['elems'].append(E('h3', f'{i:02d}. {name}'))
        p4['elems'].append(E('code', outfit_prompt('man', desc)))
    p5 = {'page': 5, 'doc': 'DROP 001', 'elems': [
        E('h2', 'Master scene of the month: The Big Reveal'),
        E('body', 'A complete, filled-out Director’s Master Template. Swap '
                  'the brackets for your character and your dream location, '
                  'attach your references, and paste the whole thing into '
                  'your video tool.'),
        E('code', PENTHOUSE),
    ]}
    p6 = {'page': 6, 'doc': 'DROP 001', 'elems': [
        E('h2', 'Tool notes — August'),
        E('bullet', 'Video: Seedance 2.0 syncs lips best on clips of 10 '
                    'seconds or less. Keep spoken lines 5–10 words.'),
        E('bullet', 'Photos: batch your poses in Nano Banana Pro right after '
                    'you lock a new outfit — 6 to 10 angles per look.'),
        E('bullet', 'Dialogue budget: about 2 spoken words per second of '
                    'clip. A 15-second scene holds 25–30 words TOTAL.'),
        E('h2', 'Member mission'),
        E('body', 'Post ONE scene from this drop with #THESCENEAI. The best '
                  'episode gets reposted and broken down in next month’s '
                  'drop.'),
    ]}
    return [cover, p2, p3, p4, p5, p6]


def main():
    render.register_fonts()
    os.makedirs(OUT, exist_ok=True)
    S = make_styles(HexColor(MAG))
    meta = {'kicker': 'THE SCENE AI · DROP 001', 'title': 'THE VACATION HEAT DROP',
            'sub': '30 new scenes, 10 new looks, and this month’s master '
                   'scene — members only.',
            'tagline': 'CREATE THE CHARACTER. DIRECT THE SCENE. BUILD THE WORLD.',
            'accent': HexColor(MAG), 'accent_hex': MAG,
            'part': 0, 'total': 0, 'next': None,
            'banner': ('NEXT DROP', 'Drop 002 lands next month. Post with #THESCENEAI.'),
            'banner_url': 'https://www.skool.com/the-scene-ai-2627/about',
            'cover_page': None, 'closing': True}
    ps = pages()
    meta['cover_page'] = ps[0]
    build_doc('DROP 001', ps, meta,
              os.path.join(OUT, 'THE-SCENE-AI_Drop-001_The-Vacation-Heat-Drop.pdf'), S)
    print('wrote THE-SCENE-AI_Drop-001_The-Vacation-Heat-Drop.pdf')


if __name__ == '__main__':
    main()
