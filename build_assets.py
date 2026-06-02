#!/usr/bin/env python3
"""Prepare web assets for the DFC Home Improvement site:
   - trim/recolor the logo (white + black + favicon)
   - optimize the heavy source photos into web JPEGs (large + thumb)
   - emit a manifest.json describing the gallery."""
import json, re, os
from PIL import Image

SRC_PHOTOS = "/Users/hugohernandez/Documentos/DFC/website/photos/Photos"
SRC_LOGO   = "/Users/hugohernandez/Desktop/DFC Logo/concept-3.png"
OUT        = "/Users/hugohernandez/Documentos/DFC/website/dfc-site/assets"
IMG        = os.path.join(OUT, "img")
LOGO       = os.path.join(OUT, "logo")

def slugify(s):
    s = s.lower()
    s = re.sub(r"\.(png|jpg|jpeg)$", "", s)
    s = re.sub(r",?\s*(washington|dc|va|richmond)\b", "", s)
    s = re.sub(r"\b\d{5}\b", "", s)
    s = s.replace("(", "").replace(")", "")
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    s = re.sub(r"-+", "-", s)
    return s

# ---------- LOGO ----------
def process_logo():
    im = Image.open(SRC_LOGO).convert("RGBA")
    # trim to alpha bounding box (logo art is white on transparent)
    alpha = im.split()[-1]
    bbox = alpha.getbbox()
    im = im.crop(bbox)
    pad = int(max(im.size) * 0.04)
    canvas = Image.new("RGBA", (im.width + 2*pad, im.height + 2*pad), (0,0,0,0))
    canvas.paste(im, (pad, pad), im)
    im = canvas
    # WHITE version (for dark backgrounds) = source as-is
    im.save(os.path.join(LOGO, "dfc-logo-white.png"))
    # BLACK version (for light backgrounds): keep alpha, set RGB to near-black ink
    r,g,b,a = im.split()
    ink = Image.new("L", im.size, 0x09)
    black = Image.merge("RGBA", (ink, Image.new("L",im.size,0x04), Image.new("L",im.size,0x02), a))
    black.save(os.path.join(LOGO, "dfc-logo-black.png"))
    # COMPACT MARK: house + "DFC" only, dropping the "HOME IMPROVEMENT" line.
    aa = im.split()[-1]
    H = im.height
    prof = list(aa.resize((1, H)).getdata())   # avg alpha per row
    ink = [v > 5 for v in prof]
    bands = []
    i = 0
    while i < H:
        if ink[i]:
            j = i
            while j < H and ink[j]:
                j += 1
            bands.append((i, j)); i = j
        else:
            i += 1
    if len(bands) >= 2:                          # last band = "HOME IMPROVEMENT"
        gap = bands[-1][0] - bands[-2][1]
        cut = bands[-1][0] - max(2, gap // 2)
    else:
        cut = H
    mark = im.crop((0, 0, im.width, cut))
    mark = mark.crop(mark.split()[-1].getbbox())
    mp = int(max(mark.size) * 0.05)
    mc = Image.new("RGBA", (mark.width + 2*mp, mark.height + 2*mp), (0,0,0,0))
    mc.paste(mark, (mp, mp), mark); mark = mc
    mark.save(os.path.join(LOGO, "dfc-mark-white.png"))
    ma = mark.split()[-1]
    Image.merge("RGBA", (Image.new("L",mark.size,0x09), Image.new("L",mark.size,0x04),
                         Image.new("L",mark.size,0x02), ma)).save(os.path.join(LOGO, "dfc-mark-black.png"))
    print("mark (house+DFC):", mark.size, "from", len(bands), "bands")
    # FAVICON: just the house mark — crop top ~58% of trimmed art, then square it
    mark = im.crop((0, 0, im.width, int(im.height*0.60)))
    mbb = mark.split()[-1].getbbox()
    mark = mark.crop(mbb)
    side = max(mark.size)
    sq = Image.new("RGBA", (side, side), (0,0,0,0))
    sq.paste(mark, ((side-mark.width)//2, (side-mark.height)//2), mark)
    # black-on-transparent favicon
    rr,gg,bb,aa = sq.split()
    fav = Image.merge("RGBA", (Image.new("L",sq.size,0x09), Image.new("L",sq.size,0x04), Image.new("L",sq.size,0x02), aa))
    for sz in (180, 64, 32):
        fav.resize((sz,sz), Image.LANCZOS).save(os.path.join(LOGO, f"favicon-{sz}.png"))
    print("logo:", im.size, "-> white/black/favicon done")

# ---------- PHOTOS ----------
# (filename, project, category, featured-on-home)
PHOTOS = [
    # Kitchens (hi-res project photos)
    ("Kitchen Springvale Lane.png",  "Springvale Lane",     "Kitchens",  False),
    ("Kitchen Thomas Jefferson.png", "Thomas Jefferson St", "Kitchens",  True),
    ("Kitchen Polecat Lane.png",     "Polecat Lane",        "Kitchens",  False),
    ("Kitchen Reymet Road.png",      "Reymet Road",         "Kitchens",  False),
    ("Kitchen 15th Street NE.png",   "15th Street NE",      "Kitchens",  True),
    ("Kitchen Monteiro Ave.png",     "Monteiro Avenue",     "Kitchens",  True),
    ("Kitchen North Ave.png",        "North Avenue",        "Kitchens",  False),
    ("Kitchen East Marshall.png",    "East Marshall St",    "Kitchens",  True),
    ("Kitchen Channing Street.png",  "Channing Street",     "Kitchens",  False),
    ("Kitchen Elliott Street.png",   "Elliott Street NE",   "Kitchens",  False),
    # Bathrooms (hi-res project photos)
    ("Bath Springvale Lane.png",     "Springvale Lane",     "Bathrooms", False),
    ("Bath Thomas Jefferson.png",    "Thomas Jefferson St", "Bathrooms", False),
    ("Bath Polecat Lane.png",        "Polecat Lane",        "Bathrooms", True),
    ("Bath Reymet Road.png",         "Reymet Road",         "Bathrooms", False),
    ("Bath 15th Street NE.png",      "15th Street NE",      "Bathrooms", True),
    ("Bath Monteiro Ave.png",        "Monteiro Avenue",     "Bathrooms", True),
    ("Bath North Ave.png",           "North Avenue",        "Bathrooms", False),
    ("Bath Channing Street.png",     "Channing Street",     "Bathrooms", False),
    ("Bath Elliott Street.png",      "Elliott Street NE",   "Bathrooms", False),
    ("Bath Marble Suite.png",        "Marble Suite",        "Bathrooms", True),
    # Outdoor (patios & decks, hi-res project photos)
    ("Outdoor Polecat Patio.png",       "Polecat Lane",     "Outdoor",   True),
    ("Outdoor Polecat Patio 2.png",     "Polecat Lane",     "Outdoor",   False),
    ("Outdoor East Marshall Patio.png", "East Marshall St", "Outdoor",   False),
    ("Outdoor 15th Street Deck.png",    "15th Street NE",   "Outdoor",   True),
    ("Outdoor 15th Street Patio.png",   "15th Street NE",   "Outdoor",   False),
    # 3D design renderings (SketchUp perspectives) — curated from DFC Projects
    ("3D Sage Kitchen 1.jpg",                          "Sage Kitchen Concept",   "3D Designs", True),
    ("3D Sage Kitchen 2.jpg",                          "Sage Kitchen Concept",   "3D Designs", False),
    ("3D Sage Kitchen 3.jpg",                          "Sage Kitchen Concept",   "3D Designs", False),
    ("3D Tiny Home Exterior.jpg",                      "Tiny Home Design",       "3D Designs", True),
    ("3D Tiny Home Kitchen.jpg",                       "Tiny Home Design",       "3D Designs", False),
    ("3D Tiny Home Bath.jpg",                          "Tiny Home Design",       "3D Designs", False),
    ("3D Tiny Home Living.jpg",                        "Tiny Home Design",       "3D Designs", False),
    ("3D Modern Kitchen 1.jpg",                        "Modern Kitchen Concept", "3D Designs", False),
    ("3D Modern Kitchen 2.jpg",                        "Modern Kitchen Concept", "3D Designs", False),
    ("3D Covered Patio 1.jpg",                         "Covered Patio Design",   "3D Designs", True),
    ("3D Covered Patio 2.jpg",                         "Covered Patio Design",   "3D Designs", False),
    ("3D Covered Patio 3.jpg",                         "Covered Patio Design",   "3D Designs", False),
]

def process_photos():
    manifest = []
    used = set()
    for fname, project, cat, feat in PHOTOS:
        path = os.path.join(SRC_PHOTOS, fname)
        if not os.path.exists(path):
            print("MISSING", fname); continue
        slug = slugify(fname)
        while slug in used:
            slug += "-x"
        used.add(slug)
        im = Image.open(path).convert("RGB")
        w,h = im.size
        # large (long side 1920)
        scale = min(1.0, 1920/max(w,h))
        lg = im.resize((round(w*scale), round(h*scale)), Image.LANCZOS) if scale<1 else im
        lg.save(os.path.join(IMG, slug+".jpg"), "JPEG", quality=82, optimize=True, progressive=True)
        # thumb (long side 900)
        ts = min(1.0, 900/max(w,h))
        th = im.resize((round(w*ts), round(h*ts)), Image.LANCZOS) if ts<1 else im
        th.save(os.path.join(IMG, slug+"-thumb.jpg"), "JPEG", quality=78, optimize=True, progressive=True)
        manifest.append({"slug":slug, "project":project, "category":cat,
                         "featured":feat, "w":lg.width, "h":lg.height,
                         "src":f"assets/img/{slug}.jpg", "thumb":f"assets/img/{slug}-thumb.jpg"})
    with open(os.path.join(OUT, "..", "manifest.json"), "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"photos: {len(manifest)} processed")
    return manifest

if __name__ == "__main__":
    process_logo()
    m = process_photos()
    # quick size report
    total = sum(os.path.getsize(os.path.join(IMG, x)) for x in os.listdir(IMG))
    print(f"total img dir: {total/1024/1024:.1f} MB across {len(os.listdir(IMG))} files")
