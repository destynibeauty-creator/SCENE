# -*- coding: utf-8 -*-
"""Map outfit pieces -> Fluent Emoji (MIT) icons and expose data URIs."""
import json, os, base64

HERE = os.path.dirname(os.path.abspath(__file__))
# Prefer the vendored subset (repo is self-contained); fall back to the full
# npm package if it's installed (e.g. when adding new icons).
_VENDOR = os.path.join(HERE, "icons_used.json")
_FULL = os.path.join(HERE, "iconpkg", "node_modules",
                     "@iconify-json", "fluent-emoji-flat", "icons.json")
_data = json.load(open(_VENDOR if os.path.exists(_VENDOR) else _FULL))
_icons = _data["icons"]
_W = _data.get("width", 32); _H = _data.get("height", 32)

# ordered rules: (keywords, icon).  First match wins.
# garment / functional nouns are checked BEFORE beauty so color words
# like "cream"/"blush" on a blazer never mis-route to makeup.
RULES = [
    # tech / lifestyle accents
    (["airpod", "headphone", "earbud"], "headphone"),
    (["phone case", "phone crossbody", "iphone", "phone"], "mobile-phone"),
    (["tumbler", "bottle", "quencher", "stanley", "owala", "hydro",
      "iceflow", "flask", "electrolyte", "lmnt"], "tumbler-glass"),
    # eyewear / watch
    (["sunglass", "sunnies", "shield sunglasses"], "sunglasses"),
    (["eyewear", "glasses"], "glasses"),
    (["watch"], "watch"),
    (["anklet"], "gem-stone"),
    (["therabody", "theraface", "theragun", "device"], "gem-stone"),
    (["towel", "pillowcase", "blanket"], "scarf"),
    # jewelry (strong nouns)
    (["earring", "hoop", "stud", "ear cuff", "ear stack", "huggie"], "gem-stone"),
    (["necklace", "pendant", "choker", "beads", "station necklace",
      "coin necklace", "chain"], "prayer-beads"),
    (["ring", "bangle", "bracelet", "cuff", "tennis", "clou", "juste un",
      "love bangle", "serpenti", "signet"], "ring"),
    (["gem", "crystal", "diamond"], "gem-stone"),
    # accessories
    (["scarf", "shawl", "headscarf", "pashmina", "silk wrap"], "scarf"),
    (["glove"], "gloves"),
    (["crown", "tiara"], "crown"),
    (["sock", "tights"], "socks"),
    (["clip", "claw", "scrunchie", "bonnet", "headband", "barrette",
      "hair bow", "hair ties", "curl", "hair wrap", "spiral"], "gem-stone"),
    (["sleep mask", "eye mask"], "scarf"),
    # hats
    (["fedora", "panama", "wide-brim", "straw hat", "bucket hat",
      "raffia hat", "sun hat"], "womans-hat"),
    (["visor", "trucker", "beanie", "skullcap", "watch cap",
      " cap", "cap,"], "billed-cap"),
    (["hat"], "womans-hat"),
    # bags
    (["clutch", "minaudiere", "minaudi", "pouch", "pochette"], "clutch-bag"),
    (["backpack"], "backpack"),
    (["tote", "shopping bag", "onthego", "neverfull", "le pliage", "shopper",
      "saint louis", "system tote", "weekender", "carry-on", "carry on",
      "suitcase", "luggage"], "shopping-bags"),
    (["wallet", "purse"], "purse"),
    (["bag", "birkin", "kelly", "handbag", "jodie", "cagole", "hourglass",
      "flap", "bucket", "crossbody", "shoulder", "sac ", "loulou", "lady dior",
      "numero", "nano", "margaux", "andiamo", "baguette", "belt bag",
      "kate clutch", "panier", "beri", "polene"], "handbag"),
    # shoes
    (["pump", "heel", "stiletto", "slingback", "so kate", "begum", "gilda",
      "nudist", "opyum", "pointed pump", "rosie mule", "bing"], "high-heeled-shoe"),
    (["boot"], "womans-boot"),
    (["flip-flop", "flip flop", "thong sandal", "tkees"], "thong-sandal"),
    (["sandal", "slide", "espadrille", "wedge", "gladiator", "oran",
      "nu pieds", "little star", "chypre", "adilette", "oofos"], "womans-sandal"),
    (["sneaker", "trainer", "samba", "gazelle", "dunk", "air force", "af1",
      "air max", "new balance", "9060", "530", "550", "cloud", "running shoe",
      "asics", "hoka", "vomero", "metcon", "nobull", "veja", "campo",
      "common projects", "achilles", "b23", "superstar", "forum", "530",
      "fuelcell", "cloudmonster", "cloudtilt", "clifton", "gel-", "barricade",
      "530", "9060"], "running-shoe"),
    (["loafer", "ballet flat", "ballet", "mule", "clog", "birkenstock", "ugg",
      "tasman", "slipper", "moccasin", "boston", "arizona", "madrid",
      "scuffette", "coquette", "fluff", "flat"], "flat-shoe"),
    # swimwear
    (["bikini"], "bikini"),
    (["swimsuit", "one-piece", "one piece", "maillot", "swim"], "one-piece-swimsuit"),
    # outerwear
    (["robe"], "coat"),
    (["kimono"], "kimono"),
    (["coat", "blazer", "jacket", "trench", "puffer", "parka", "bomber",
      "moto", "faux fur", "fur ", "teddy", "overcoat", "windbreaker",
      "track jacket", "wrap coat", "super puff", "nuptse", "duster", "shacket",
      "flannel", "trucker jacket", "firebird", "track top", "quilted vest",
      "down vest", "cardigan"], "coat"),
    # one-piece garments
    (["gown", "dress", "jumpsuit", "romper", "nap dress", "kaftan",
      "cover-up", "coverup"], "dress"),
    # beauty / skincare / fragrance (after garments so color words never leak here)
    (["lipstick", "lip ", "lip,", "lip glow", "lip oil", "lip butter",
      "lip sleeping", "lip treatment", "lip glowy", "gloss", "balm dotcom",
      "glowy balm", "hand balm", "lip balm", " balm", "blush", "highlighter",
      "bronzer", "cheek", "beach stick", "contour stick", "serum", "sheet mask",
      "jet lag mask", "sleeping mask", "hydrating mask", "overnight", "moistur",
      "facial", "repair", "recovery", "ceramid", "toner", "peptide", "spf",
      "sunscreen", "glowscreen", "fragrance", "parfum", "perfume", "eau de",
      "cologne", "candle", "lotion", "body oil", "glow oil", "browning",
      "tanning", "spray", "buffet", "soin", " sos", "tint", "concealer",
      "foundation", "mascara", "eyeshadow", "primer", "glaze", "glazing"], "lipstick"),
    # bottoms
    (["bike short", "short set", "shorts", "cut-off", "biker short",
      "lounge short", "sleep short", "boxer"], "shorts"),
    (["legging", "trouser", "pant", "jean", "denim", "cargo", "parachute",
      "jogger", "sweatpant", "flare", "ribcage", "wide-leg", "wide leg",
      "cigarette", "chino", "culotte", "sweatpant"], "jeans"),
    (["skirt", "skort"], "dress"),
    (["maxi", "midi", "slip "], "dress"),
    # tops (generic, last before fallback)
    (["bra", "sports bra"], "running-shirt"),
    (["tee", "t-shirt", "tshirt", "hoodie", "sweatshirt", "crewneck", "crew ",
      "pullover", "quarter-zip", "half-zip", "zip-up", "zip hoodie", "henley",
      "jersey", "windbreaker"], "t-shirt"),
    (["tank", "cami", "blouse", "bodysuit", "turtleneck", "sweater", "knit",
      "corset", "bustier", "halter", "shell", "vest", "longline", "long-sleeve",
      "longsleeve", "long sleeve", "mock", "set", "top", "shirt", "milkmaid",
      "romper"], "womans-clothes"),
]
FALLBACK = "womans-clothes"

def classify(brand, desc):
    s = (desc + " " + brand).lower()
    for kws, icon in RULES:
        for k in kws:
            if k in s:
                return icon
    return FALLBACK

_cache = {}
def data_uri(icon):
    if icon in _cache:
        return _cache[icon]
    body = _icons[icon]["body"]
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" '
           f'viewBox="0 0 {_W} {_H}">{body}</svg>')
    uri = "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()
    _cache[icon] = uri
    return uri

_isvg = {}
def svg_inline(icon, cls="ic"):
    """Inline <svg> — renders reliably in Chromium --print-to-pdf (unlike <img>)."""
    key = (icon, cls)
    if key in _isvg:
        return _isvg[key]
    body = _icons[icon]["body"]
    out = (f'<svg class="{cls}" xmlns="http://www.w3.org/2000/svg" '
           f'viewBox="0 0 {_W} {_H}">{body}</svg>')
    _isvg[key] = out
    return out

# ---- very faint color tint, read from each piece's description ----
# base medium tones; blended toward white so the chip stays whisper-soft.
_COLOR_BASE = [
    # multiword / specific first
    ("light wash", (188, 211, 239)), ("mid-wash", (150, 178, 214)),
    ("dark wash", (120, 140, 178)), ("university blue", (150, 190, 235)),
    ("powder blue", (196, 220, 244)), ("baby blue", (196, 220, 244)),
    # pinks
    ("blush", (244, 201, 219)), ("rose", (240, 178, 198)), ("mauve", (220, 190, 202)),
    ("powder", (245, 214, 227)), ("sugar", (247, 210, 224)), ("petal", (246, 205, 220)),
    ("pink", (244, 190, 214)),
    # purples
    ("lilac", (220, 204, 236)), ("lavender", (222, 210, 238)), ("purple", (205, 180, 220)),
    # reds / warm
    ("burgundy", (196, 130, 138)), ("wine", (200, 138, 146)), ("ruby", (226, 150, 160)),
    ("cherry", (232, 150, 158)), ("red", (232, 160, 166)), ("scarlet", (232, 150, 150)),
    ("coral", (244, 196, 166)), ("apricot", (246, 208, 176)), ("terracotta", (226, 176, 150)),
    ("peach", (248, 214, 190)), ("rust", (214, 160, 128)), ("orange", (246, 196, 150)),
    # yellows / gold
    ("champagne", (232, 220, 190)), ("butter", (244, 232, 190)), ("gold", (232, 210, 158)),
    ("mustard", (226, 196, 120)), ("yellow", (246, 232, 170)),
    # greens
    ("emerald", (170, 206, 180)), ("sage", (200, 216, 198)), ("olive", (196, 200, 150)),
    ("mint", (198, 226, 206)), ("green", (188, 214, 186)),
    # blues
    ("navy", (185, 196, 222)), ("denim", (176, 200, 230)), ("cobalt", (170, 190, 232)),
    ("blue", (190, 212, 236)), ("teal", (176, 214, 214)),
    # neutrals
    ("charcoal", (196, 192, 202)), ("graphite", (198, 194, 204)),
    ("grey", (216, 214, 220)), ("gray", (216, 214, 220)), ("heather", (214, 212, 220)),
    ("silver", (222, 223, 230)), ("dove", (222, 220, 226)), ("fog", (220, 220, 226)),
    ("black", (200, 196, 206)), ("onyx", (200, 196, 206)), ("jet", (200, 196, 206)),
    ("chocolate", (196, 158, 128)), ("cocoa", (200, 164, 134)), ("mocha", (206, 176, 148)),
    ("coffee", (196, 160, 128)), ("espresso", (176, 146, 120)), ("brown", (200, 164, 132)),
    ("camel", (224, 196, 150)), ("caramel", (222, 190, 146)), ("tan", (222, 200, 162)),
    ("khaki", (210, 200, 158)), ("taupe", (216, 204, 186)), ("sand", (230, 216, 190)),
    ("stone", (222, 216, 204)), ("beige", (230, 218, 196)), ("nude", (232, 214, 194)),
    ("oatmeal", (230, 222, 204)), ("oat", (230, 222, 204)), ("ecru", (234, 226, 210)),
    ("bone", (234, 226, 212)), ("cream", (236, 228, 210)), ("ivory", (238, 230, 214)),
    ("vanilla", (238, 230, 214)), ("white", (236, 232, 226)),
]
_NEUTRAL = (243, 233, 240)   # soft blush-grey default

def _blend_white(rgb, keep=0.22):
    r, g, b = rgb
    r = round(255*(1-keep) + r*keep)
    g = round(255*(1-keep) + g*keep)
    b = round(255*(1-keep) + b*keep)
    return f"#{r:02x}{g:02x}{b:02x}"

def tint_for(desc):
    """Whisper-faint chip color pulled from the color word in the description."""
    d = desc.lower()
    parts = [p.strip() for p in d.split(",")]
    cand = parts[-1] if len(parts) > 1 else d
    for kw, rgb in _COLOR_BASE:
        if kw in cand:
            return _blend_white(rgb)
    for kw, rgb in _COLOR_BASE:
        if kw in d:
            return _blend_white(rgb)
    return _blend_white(_NEUTRAL)

def icon_uri_for(brand, desc):
    return data_uri(classify(brand, desc))

def icon_svg_for(brand, desc, cls="ic"):
    return svg_inline(classify(brand, desc), cls)

if __name__ == "__main__":
    from data import PACK
    from collections import Counter
    cnt = Counter(); fb = []
    total = 0
    for cat, looks in PACK.items():
        for name, vibe, items in looks:
            for brand, desc in items:
                ic = classify(brand, desc); cnt[ic] += 1; total += 1
                if ic == FALLBACK and not any(
                    k in (desc+" "+brand).lower()
                    for k in ["top","shirt","blouse","cami","tank","bodysuit",
                              "sweater","knit","turtleneck","corset","bustier",
                              "shell","set","vest","milkmaid","mock","halter",
                              "longline"]):
                    fb.append(f"{cat} | {brand} — {desc}")
    print(f"items={total}")
    for ic, c in cnt.most_common():
        print(f"  {c:4d}  {ic}")
    print(f"\nUNMATCHED-fallbacks ({len(fb)}):")
    for x in fb[:60]:
        print("  ", x)
