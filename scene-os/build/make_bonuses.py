#!/usr/bin/env python3
"""
Rebuild the four bonus documents so every tool belongs to the BUYER:
their own keyword, their own captions, their own pinned comments, plus a
competitor-study system and niche-diverse examples. Writes content_final.json
(content_simple.json with the bonus docs replaced).
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'content_simple.json')
OUT = os.path.join(HERE, 'content_final.json')


def E(t, *lines, **kw):
    d = {'type': t, 'y': 0}
    if lines:
        d['lines'] = list(lines)
    d.update(kw)
    return d


def cover(kicker, title, sub):
    return [
        E('label', kicker),
        E('h1', title),
        E('sub', sub),
        E('label', 'CREATE THE CHARACTER. DIRECT THE SCENE. BUILD THE WORLD.'),
    ]


# ------------------------------------------------------------- START HERE
def start_here_tools():
    return {'page': 3.5, 'doc': 'START HERE', 'elems': [
        E('h2', 'Your tool kit — the apps you need'),
        E('body', 'You only need three tools: one that makes photos, one that '
                  'turns photos into video, and one that edits. The system '
                  'works in ANY app that can use your MASTER photo as a '
                  'reference. These are the popular picks right now:'),
        E('table', rows=[
            ['THE JOB', 'POPULAR TOOLS', 'TIP'],
            ['Make the face and photos',
             'Midjourney, Higgsfield, OpenArt, Gemini',
             'Pick one with a character or reference feature.'],
            ['Turn photos into video',
             'Kling, Veo, Higgsfield, Runway',
             'It must accept your MASTER image.'],
            ['Edit, captions and sound',
             'CapCut, InShot',
             'CapCut is free and enough to start.'],
        ]),
        E('flow', steps=[['1', 'PICK ONE PER JOB'], ['2', 'LEARN IT ONCE'],
                         ['3', 'STAY THERE']],
          caption='Switching apps every week is how characters drift. Pick your three and commit.'),
        E('bullet', 'Free versions are fine to start. Upgrade when episodes are working.'),
        E('bullet', 'Upload your MASTER photo into every tool, every time.'),
        E('bullet', 'Keep the SAME three tools for a whole series.'),
        E('body', 'Tools change fast. If a new app comes out, the system still '
                  'works — the prompts and the method do not change.'),
        E('wcard', title='MY TOOL KIT', fields=[
            'My photo tool:', 'My video tool:', 'My editing app:',
            'My keyword (one word):']),
    ]}


# ---------------------------------------------------------------- BONUS 01
def bonus01_intro():
    return {'page': 72.5, 'doc': 'BONUS 01', 'elems': [
        E('h2', 'Make your own hook first'),
        E('body', 'A hook is the first three seconds of your video. '
                  'It is one normal moment with one thing wrong. Use this recipe:'),
        E('flow', steps=[['1', 'NORMAL MOMENT'], ['2', 'ONE THING IS OFF'],
                         ['3', 'DO NOT EXPLAIN IT']],
          caption='Start normal. Break one thing. Let the comments ask why.'),
        E('h3', 'The same recipe works in any niche'),
        E('bullet', 'Beauty: A client sits down and says, "Fix what she did."'),
        E('bullet', 'Real estate: The buyers walk in. Someone is already home.'),
        E('bullet', 'Fitness: The gym is empty except one machine. It is still running.'),
        E('bullet', 'Food: The order is ready. Nobody ordered it.'),
        E('bullet', 'Music: The beat stops. The crowd does not.'),
        E('body', 'Now use the vault below. Pick a hook, then rewrite it with '
                  'the recipe so it fits YOUR world. Do not copy it word for word.'),
        E('h2', 'The Hook Vault — 150 starters'),
    ]}


# ---------------------------------------------------------------- BONUS 02
def bonus02():
    return [
        {'page': 77, 'doc': 'BONUS 02', 'elems': cover(
            'BONUS 02', 'CAPTION VAULT',
            'Caption recipes and fill-in templates. Make every caption yours.')},
        {'page': 78, 'doc': 'BONUS 02', 'elems': [
            E('h2', 'The caption recipe'),
            E('flow', steps=[['1', 'PULL THEM IN'], ['2', 'ASK OR TEASE'],
                             ['3', 'YOUR KEYWORD']],
              caption='Line 1 hooks. Line 2 starts talk. Line 3 tells them what to comment.'),
            E('body', 'Fill in every [BRACKET] with your own words. '
                      'Never post a caption with someone else’s keyword in it.'),
            E('h2', 'Mystery'),
            E('bullet', 'Now who sent this over...'),
            E('bullet', 'At this point, whoever sent it needs to come out of hiding.'),
            E('bullet', 'How are you this bold but scared to say something?'),
            E('bullet', 'I came for lunch. Apparently somebody else had plans.'),
            E('bullet', 'The plot was never random. Y’all just got here late.'),
            E('h2', 'Story series'),
            E('bullet', 'Part [#], because y’all were not letting this go.'),
            E('bullet', 'Still no reveal, but now I’m invested.'),
            E('bullet', 'This was supposed to be the calm part of the trip.'),
            E('bullet', 'The next five minutes changed the whole storyline.'),
            E('bullet', 'Some people do not need an introduction.'),
            E('h2', 'Creator / AI'),
            E('bullet', 'I almost did not post the first one. Now y’all are asking who the characters are.'),
            E('bullet', 'The moment people stopped asking if it was AI and started asking what happened next.'),
            E('bullet', 'We do not just prompt. We direct.'),
            E('bullet', 'I built the character, the camera and the entire situation from my phone.'),
            E('bullet', 'Episode one of a world I’m building. Stay if you’re nosy.'),
            E('h2', 'Education (fill in your craft)'),
            E('bullet', 'I’mma be real, we are not skipping [THE BASICS OF YOUR CRAFT].'),
            E('bullet', 'The part everybody calls boring is the part protecting [YOUR CLIENT / CUSTOMER].'),
            E('bullet', 'Before we talk about [THE RESULT], we need to talk about [THE PROCESS].'),
            E('bullet', 'A pretty [RESULT] does not excuse a bad [PROCESS].'),
            E('bullet', 'What is one thing your first [TRAINING / JOB] never taught you?'),
            E('h2', 'Brand-friendly'),
            E('bullet', 'A concept built around the product, not pasted on top of it.'),
            E('bullet', 'This is what branded storytelling can look like.'),
            E('bullet', 'The product belongs inside the plot.'),
            E('bullet', 'A campaign people watch before they realize it is a campaign.'),
            E('bullet', '[YOUR CITY] brands, picture your business inside the next scene.'),
            E('h2', 'Conversion endings (use YOUR keyword)'),
            E('bullet', 'Comment [YOUR KEYWORD] and I’ll send you [WHAT THEY GET].'),
            E('bullet', 'DM me [YOUR KEYWORD] for the details.'),
            E('bullet', 'Click the link in my bio to get [WHAT THEY GET].'),
            E('bullet', 'Book [YOUR SERVICE] through the link in my bio.'),
            E('bullet', 'Join the waitlist for [YOUR OFFER] before it opens.'),
        ]},
    ]


# ---------------------------------------------------------------- BONUS 03
def bonus03():
    return [
        {'page': 79, 'doc': 'BONUS 03', 'elems': cover(
            'BONUS 03', 'COMMENT BLUEPRINT',
            'Turn your comment section into your best salesperson — '
            'with your own keyword, not anyone else’s.')},
        {'page': 80, 'doc': 'BONUS 03', 'elems': [
            E('h2', 'Step 1 — Pick YOUR keyword'),
            E('body', 'Your keyword is one word people comment to get something '
                      'from you. It must be YOUR word, tied to YOUR offer.'),
            E('flow', steps=[['1', 'PICK ONE WORD'], ['2', 'NAME THE PRIZE'],
                             ['3', 'USE IT EVERY TIME']],
              caption='One word. Easy to spell. Always points at your offer.'),
            E('table', rows=[
                ['YOUR NICHE', 'KEYWORD IDEA', 'WHAT YOU SEND THEM'],
                ['Beauty', 'GLOW', 'Your booking link or prep guide'],
                ['Real estate', 'KEYS', 'Your buyer checklist or tour booking'],
                ['Fitness', 'LIFT', 'Your free workout or coaching link'],
                ['Food', 'PLATE', 'Your recipe or order link'],
                ['Music', 'TRACK', 'Your unreleased snippet or presave link'],
                ['Fashion', 'FIT', 'Your lookbook or shop link'],
            ]),
            E('body', 'Pick one now. Write it down. You will use it in every '
                      'caption, pinned comment and reply below.'),
            E('h2', 'Step 2 — Pin these three comments'),
            E('body', 'Pin these on every episode, in this order. '
                      'Copy the pattern, not the words.'),
            E('ccard', note='PIN 1  —  EASY OPINION (everyone can answer)',
              text='Be honest — would you take the drink or send it back?'),
            E('ccard', note='PIN 2  —  START A DEBATE (they defend a side)',
              text='Smooth or doing too much?'),
            E('ccard', note='PIN 3  —  CAPTURE LEADS (your keyword works here)',
              text='Want [WHAT YOU OFFER]? Comment [YOUR KEYWORD] and I’ll send it to you.'),
            E('h2', 'Step 3 — Reply like this'),
            E('table', rows=[
                ['WHEN THEY SAY', 'YOU REPLY'],
                ['“Make me one”', 'I got you \U0001F602 Comment [YOUR KEYWORD] and watch what I send you.'],
                ['“Is this AI?”', 'Yes \U0001F62D but you still need to know what happens next.'],
                ['“Who is he?”', 'Y’all really want the reveal that bad? \U0001F440'],
                ['Something negative', 'And yet you stopped to comment \U0001F62D'],
                ['Brand praise', 'Now imagine YOUR product inside a whole storyline.'],
                ['Beginner question', 'Start with one character and one scene. That’s it.'],
            ]),
            E('h2', 'Step 4 — Build your own comment set'),
            E('wcard', title='MY COMMENT SET', fields=[
                'My easy opinion question:',
                'My debate question:',
                'My keyword (one word):',
                'What I send when they comment it:',
                'My Part 2 teaser:',
            ]),
        ]},
    ]


# ---------------------------------------------------------------- BONUS 04
def bonus04():
    case = lambda title, hook, refs, engine, nxt: [
        E('h2', title),
        E('bullet', f'Hook: {hook}'),
        E('bullet', f'References: {refs}'),
        E('bullet', f'Why people watch: {engine}'),
        E('bullet', f'Next episode: {nxt}'),
    ]
    elems82 = [
        E('h2', 'Study your top 3 competitors first'),
        E('body', 'Before you film anything, find the top three creators in '
                  'YOUR niche who are doing this right now. Watch their three '
                  'best videos each. Fill in one card per creator. '
                  'Your job is not to copy them. Your job is to beat them.'),
        E('flow', steps=[['1', 'FIND TOP 3'], ['2', 'STUDY THEIR BEST'],
                         ['3', 'DO IT BETTER']],
          caption='Same niche. Same format. Better character, better story, better world.'),
        E('wcard', title='COMPETITOR #1', fields=[
            'Name / handle:', 'Their best video (link):',
            'The hook in the first 3 seconds:', 'Their caption:',
            'Their pinned comment / keyword:', 'Why it worked:',
            'What I will do better:']),
        E('wcard', title='COMPETITOR #2', fields=[
            'Name / handle:', 'Their best video (link):',
            'The hook in the first 3 seconds:', 'Their caption:',
            'Their pinned comment / keyword:', 'Why it worked:',
            'What I will do better:']),
        E('wcard', title='COMPETITOR #3', fields=[
            'Name / handle:', 'Their best video (link):',
            'The hook in the first 3 seconds:', 'Their caption:',
            'Their pinned comment / keyword:', 'Why it worked:',
            'What I will do better:']),
    ]
    elems83 = (
        [E('h2', 'Five viral patterns you can run in any niche')] +
        case('1. The Mystery Gift',
             'something arrives for your character from an unknown sender.',
             'identity, outfit, location, continuity, the item itself.',
             'viewers need to know who sent it and demand the reveal.',
             'the sender stays hidden one more time, then gets revealed.') +
        case('2. The Dream Location',
             'phone-style footage that feels real inside a dream spot.',
             'identity, outfit, location exterior and interior, one product.',
             'continuity makes made-up events feel like a real series.',
             'one new event, same world, same character.') +
        case('3. The Shopping Spree',
             'your character came to browse and leaves with everything.',
             'identity, exact outfit, store environment, bags and product.',
             'locals recognize the place, and brands may repost it.',
             'fitting room, checkout moment or outfit reveal.') +
        case('4. The Night Out',
             'nightlife chaos your audience understands at a glance.',
             'characters, outfits, venue, signage, table service.',
             'a bold location, matching sound and comment-section debate.',
             'the morning after, or the behind-the-scenes reaction.') +
        case('5. The Nervous First Client',
             'a first-timer walks into your world of work.',
             'your identity, work outfit, real workspace, your tools.',
             'emotion plus expert authority builds trust in your skill.',
             'the transformation, a lesson or the client’s reaction.')
    )
    elems84 = [
        E('h2', 'Blank case-study file (fill one per episode)'),
        E('wcard', title='EPISODE FILE — BEFORE YOU POST', fields=[
            'Concept / inspiration:', 'Who it is for (audience):',
            'Character:', 'Story in one line:', 'Cast:', 'Environment:',
            'Reference order:', 'Camera:', 'Opening frame:']),
        E('wcard', title='EPISODE FILE — AFTER YOU POST', fields=[
            'Caption I used:', 'My three pinned comments:',
            'Views / saves / comments:', 'What worked:', 'What failed:',
            'Next episode:']),
    ]
    return [
        {'page': 81, 'doc': 'BONUS 04', 'elems': cover(
            'BONUS 04', 'THE SCENE FILES',
            'Study the winners in your niche, run proven viral patterns, '
            'and keep a file on every episode you post.')},
        {'page': 82, 'doc': 'BONUS 04', 'elems': elems82},
        {'page': 83, 'doc': 'BONUS 04', 'elems': elems83},
        {'page': 84, 'doc': 'BONUS 04', 'elems': elems84},
    ]


def main():
    pages = json.load(open(SRC))
    out = []
    b1_done = sh_done = False
    for p in pages:
        if p['doc'] in ('BONUS 02', 'BONUS 03', 'BONUS 04'):
            continue  # fully replaced below
        if p['doc'] != 'START HERE' and not sh_done:
            out.append(start_here_tools())  # after the last Start Here page
            sh_done = True
        out.append(p)
        if p['doc'] == 'BONUS 01' and not b1_done:
            out.append(bonus01_intro())  # after the Bonus 01 cover
            b1_done = True
    out.extend(bonus02())
    out.extend(bonus03())
    out.extend(bonus04())
    json.dump(out, open(OUT, 'w'), indent=1)
    print(f'wrote {OUT}: {len(out)} pages')


if __name__ == '__main__':
    main()
