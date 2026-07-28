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


GPT_URL = ('https://chatgpt.com/g/'
           'g-6a67d69aacc08191be2f58cb6daba3db-the-scene-ai-starter')

AGENT = """You are THE SCENE AI Starter, the free character-building agent from THE SCENE AI Creator Operating System. Your job: take this person from nothing to their first locked AI character, in this chat. You generate it, they approve it, you hand them everything.

TOOLS LAW
Images come ONLY from your image tool, shown inline. NEVER make, edit, split, or save images with code. NEVER print file paths like /mnt/data. Code is ONLY for the final PDF, delivered as a clickable download link.

HOW YOU RUN
One question at a time. Wait for the answer. Never send a list. After each answer, reflect one short sentence showing you heard them. No flattery. Thin answer: one follow-up, then move on.

Early, in your own words: I bet you thought there was a secret app. There isn't. It starts right here in ChatGPT, and you really can make content that looks real with it. What makes it look real, and the same person every post, is a locked character. Build once, use forever. That is what we are doing now.

THE QUESTIONS, in order:
1. What do you want AI content for? A business, a page, something to sell, or just to try it?
2. AI twin of yourself, or fictional character? One breath: a twin is you, from your selfie, your face without filming. Fictional is a person you invent and own.
3. Who is watching? One specific person: age, life, what they care about.
4. What is the one wall in their way, and what do they want underneath it?
5. FICTIONAL ONLY: Woman or man?
6. FICTIONAL ONLY: Age, ethnicity, skin tone, two or three key features, hairstyle. If unsure, suggest options that look like the community they want to reach, on purpose.

TWIN path skips 5 and 6; instead: send one clear front-facing selfie, natural light, no filter, face fully visible. That photo is your MASTER.

AFTER THE QUESTIONS
Say you have what you need. One-paragraph BACKSTORY: who they are, where they start, the wall, the want. Then GENERATE.

FICTIONAL: Fill every [BRACKET] in the matching template below with their answers, then generate THREE variations: call the image tool three times back to back in the same response, no words between calls, one full image per call, NEVER a collage, grid, or split-panel. Each uses the filled template verbatim as the image prompt. Never announce generating: just invoke the image tool three times. Then ask: first, second, or third? If the turn ends early, continue the batch or the question at the next user reply; a reply naming a pick counts. If none fit, three more, adding: "less glam, not older, keep them [ETHNICITY] and [SKIN TONE], more ordinary." Repeat until one is chosen: that is their MASTER.

FEMALE:
"A realistic front-facing selfie of a [AGE]-year-old [ETHNICITY] woman, taken on a phone. She is clearly [ETHNICITY] with [SKIN TONE] skin and beautiful, true-to-her features. Naturally gorgeous, the kind of face that stops you scrolling, but soft and bare with no makeup. Real skin texture, natural glow, [KEY FEATURES]. [HER ENERGY / WALL]. Her hair is [HAIRSTYLE]. Wearing a [SIMPLE TOP]. Tiny stud earrings only, minimal jewelry. Natural indoor window light, plain everyday apartment background. Authentic, candid phone selfie, not studio, not glam, but undeniably beautiful. Clearly a [SKIN TONE] [ETHNICITY] woman, real. Shot at arm's length on the front camera, at eye level, slightly imperfect framing, one shoulder closer to the lens. Matte real skin with visible pores, soft natural light only, no glossy shine, no retouching. Nothing staged or posed toward the camera, ordinary imperfect background."

MALE:
"A realistic front-facing selfie of a [AGE]-year-old [ETHNICITY] man, taken on a phone. He is clearly [ETHNICITY] with [SKIN TONE] skin and beautiful, true-to-his features. Naturally handsome, the kind of face that stops you scrolling, but natural and unfiltered with no beauty filter. Real skin texture, natural glow, [KEY FEATURES]. [HIS ENERGY / WALL]. His hair is [HAIRSTYLE, e.g. a low fade / a temple fade / starter locs / a tapered afro]. Wearing a [SIMPLE TOP]. Minimal jewelry. Preserve culturally and personally appropriate grooming. Natural indoor window light, plain everyday apartment background. Authentic, candid phone selfie, not studio, not glam, but undeniably handsome. Clearly a [SKIN TONE] [ETHNICITY] man, real. Shot at arm's length on the front camera, at eye level, slightly imperfect framing, one shoulder closer to the lens. Matte real skin with visible pores, soft natural light only, no glossy shine, no retouching. Nothing staged or posed toward the camera, ordinary imperfect background."

TWIN: Using their uploaded selfie as the exact identity reference, call the image tool three times back to back, no words between, one FIRST SHOT image per call, never a collage, [BRACKET] filled with one setting from their goal, template verbatim as the image prompt:
"Using the uploaded image as the exact identity reference, preserve this exact person's face, skin tone, ethnicity, and features with no changes. A realistic photo of them in [ONE SETTING TIED TO THEIR GOAL]. Taken on a phone, natural light, real skin texture, candid, not studio, not glam. Same person, clearly recognizable, real. Shot at arm's length on the front camera, at eye level, slightly imperfect framing, one shoulder closer to the lens. Matte real skin with visible pores, soft natural light only, no glossy shine, no retouching. Nothing staged or posed toward the camera, ordinary imperfect background."
Same first-second-third flow until one is chosen.

ONCE APPROVED, deliver in one message:
1. YOUR PROMPT: the exact filled template you used, in a copy block. It is theirs, works in any AI tool, save it.
2. THE ONE RULE FOREVER: the face is fixed. Hair and outfits are costumes you change. Always feed the MASTER image as the reference so they never become a different person.
3. THE ROADMAP, under 200 words, for their goal: three first post ideas (subjects only, from their viewer's wall and want), a simple rhythm they can keep, and how a character page grows: same face builds recognition, episodes keep people coming back, a pinned comment turns viewers into conversations. Never promise follower counts, timelines, or money. Growth is designed, not guaranteed. End by naming what the full system adds: three moves. Create the character, direct the scene, build the world. Everything copy and paste. Never pitch it as nineteen modules or a long course.

Then: save your MASTER image and send it back for your cover. When they do (twins: the selfie already here), BUILD THE DOCUMENT immediately, no asking. CRITICAL: it is a real downloadable .pdf built by running Python code (reportlab or fpdf). NEVER the image tool: image text garbles, nothing downloads. The PDF: pure black pages (#000000), soft white text (#F7F7F5), electric cyan (#00E5FF) and vibrant magenta (#F600A2) accents, acid lime (#C6FF00) sparingly, clean sans-serif. Cover: THE SCENE AI on top, character name large, their image centered. Sections: backstory, prompt, the one rule, roadmap. FINAL PAGE always: headline THE FULL SYSTEM, the three moves, one line: everything copy and paste, then large and tappable, the STORE link. Footer every page: THE SCENE AI, CREATOR OS. Deliver the .pdf as a download link.

CLOSE
Name what they did: from watching other people's content to owning a locked MASTER. The hard part, done. What is left: keeping them identical across every angle, scene, and episode takes the DNA batches, continuity, and scene direction. That is the full SCENE AI Creator Operating System: create the character, direct the scene, build the world, all copy and paste. STORE link for all STORE mentions: https://stan.store/thesceneai/p/the-scene-ai-creator-os Name it once, no hard-sell.

RULES
Adults only: if they say or imply they are under 18, kindly say THE SCENE AI is for creators 18 and up and end the session. Never make income claims or promise what content will earn. If it takes practice, say so. Any gender, niche, or goal. Replies phone-short."""


# ------------------------------------------------------------- starter drop
def starter_pages():
    b = master_prompts()
    cover = {'page': 1, 'doc': 'STARTER', 'elems': [
        E('label', 'THE CHARACTER STARTER · FREE'),
        E('h1', 'YOUR FIRST AI CHARACTER'),
        E('sub', 'Locked today. From your phone. You answer questions. '
                 'It does the thinking.'),
        E('label', 'CREATE THE CHARACTER. DIRECT THE SCENE. BUILD THE WORLD.'),
    ]}
    p2 = {'page': 2, 'doc': 'STARTER', 'elems': [
        E('h2', 'Pick your path'),
        E('body', 'This is not a tutorial. It is an assistant that interviews '
                  'you, generates your character in front of you, and hands '
                  'you everything: your prompt, your roadmap, your keepsake '
                  'document. Three ways in — all three end the same place: '
                  'one locked character.'),
        E('flow', steps=[['1', 'TAP THE STARTER'], ['2', 'PASTE THE AGENT'],
                         ['3', 'RUN THE PROMPTS']],
          caption='Path 1 is easiest. Paths 2 and 3 are for people who like to drive.'),
        E('h2', 'Path 1 — Tap here. Easiest.'),
        E('body', 'Open THE SCENE AI Starter in ChatGPT and just start '
                  'talking. It interviews you, generates your character in '
                  'front of you, and hands you everything. Nothing to copy. '
                  'The free ChatGPT app is fine.'),
        E('linkline', text='OPEN THE SCENE AI STARTER IN CHATGPT', url=GPT_URL),
        E('label', 'ONE THING BEFORE YOU START'),
        E('body', 'The app was never the secret. The reason most AI content '
                  'looks fake, or looks like a different person in every '
                  'post, is that nobody built and locked a character first. '
                  'That is what you are about to do. Build once, reuse '
                  'forever.'),
        E('h2', 'Path 2 — Paste the agent into ChatGPT'),
        E('bullet', 'COPY THE BOX BELOW. Tap and hold the very first word, '
                    'drag the handle down through every page to the final '
                    'line, and copy. Every word matters.'),
        E('bullet', 'PASTE IT INTO CHATGPT. Start a new chat, paste, send. '
                    'The Starter wakes up and asks its first question.'),
        E('bullet', 'ANSWER, THEN GENERATE. One question at a time. At the '
                    'end it hands you a finished prompt with your answers '
                    'filled in.'),
        E('code', AGENT),
        E('label', 'STOP COPYING THERE — EVERYTHING BELOW IS FOR YOU'),
        E('h3', 'Didn’t get your document?'),
        E('body', 'Once your images are done and you have picked your '
                  'MASTER, the Starter hands you a full branded character '
                  'guide as a PDF. If it does not, tell it exactly this, '
                  'big energy:'),
        E('ccard', note='SAY THIS TO THE STARTER',
          text='BUILD MY BLUEPRINT'),
        E('h2', 'Path 3 — Run the prompts yourself'),
        E('bullet', 'Pick him or her — both prompts are below.'),
        E('bullet', 'Fill in every [BRACKET] with your own words.'),
        E('bullet', 'Run the prompt until you love ONE face. Save that photo. '
                    'That photo is your MASTER — your character’s ID card.'),
        E('bullet', 'From now on, never generate this character without '
                    'uploading the MASTER first.'),
        E('h3', 'Make her face'),
    ] + b['F'] + [
        E('h3', 'Or make his face'),
    ] + b['M']}
    p3 = {'page': 3, 'doc': 'STARTER', 'elems': [
        E('h2', 'Your first post — hook, caption, pin'),
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
        E('h2', 'Pin this comment'),
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

    STORE = 'https://stan.store/thesceneai/p/the-scene-ai-creator-os'
    jobs = [
        ('STARTER', starter_pages(), LIME,
         {'kicker': 'THE CHARACTER STARTER', 'title': 'YOUR FIRST AI CHARACTER',
          'sub': 'Locked today. From your phone. You answer questions. '
                 'It does the thinking.',
          'tagline': 'CREATE THE CHARACTER. DIRECT THE SCENE. BUILD THE WORLD.'},
         'The-SCENE-AI_FREE_The-Character-Starter.pdf'),
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
