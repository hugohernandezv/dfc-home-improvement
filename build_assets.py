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
    ("10602 Springvale Lane.png",                      "Springvale Lane",     "Exteriors",  True),
    ("1611 Polecat Lane.png",                          "Polecat Lane",        "Exteriors",  True),
    ("1611 Polecat Lane (2).png",                      "Polecat Lane",        "Kitchens",   False),
    ("1611 Polecat Lane (3).png",                      "Polecat Lane",        "Bathrooms",  False),
    ("1611 Polecat Lane (4).png",                      "Polecat Lane",        "Interiors",  True),
    ("1063 Thomas Jefferson St.png",                   "Thomas Jefferson St", "Interiors",  True),
    ("1063 Thomas Jefferson St (2).png",               "Thomas Jefferson St", "Interiors",  False),
    ("1063 Thomas Jefferson St (3).png",               "Thomas Jefferson St", "Bathrooms",  False),
    ("1063 Thomas Jefferson St (4).png",               "Thomas Jefferson St", "Interiors",  True),
    ("218 15th St NE, Washington, DC 20002.png",       "15th Street NE",      "Interiors",  True),
    ("218 15th St NE, Washington, DC 20002 (2).png",   "15th Street NE",      "Kitchens",   True),
    ("329 15th St NE, Washington, DC 20002.png",       "15th Street NE",      "Kitchens",   False),
    ("329 15th St NE, Washington, DC 20002 (2).png",   "15th Street NE",      "Bathrooms",  False),
    ("329 15th St NE, Washington, DC 20002 (3).png",   "15th Street NE",      "Interiors",  False),
    ("2210 Monteiro Ave, Richmond, VA 23222.png",      "Monteiro Avenue",     "Bathrooms",  True),
    ("2210 Monteiro Ave, Richmond, VA 23222 (2).png",  "Monteiro Avenue",     "Interiors",  False),
    ("2210 Monteiro Ave, Richmond, VA 23222 (3).png",  "Monteiro Avenue",     "Interiors",  False),
    ("2210 Monteiro Ave, Richmond, VA 23222 (4).png",  "Monteiro Avenue",     "Interiors",  False),
    ("2903 East Marshall St.png",                      "East Marshall St",    "Interiors",  True),
    ("2903 East Marshall St (2).png",                  "East Marshall St",    "Bathrooms",  False),
    ("2903 East Marshall St (3).png",                  "East Marshall St",    "Interiors",  False),
    ("617 Elliot St. NE.png",                          "Elliot Street NE",    "Interiors",  True),
    ("25.png",                                         "Kitchen Remodel",     "Kitchens",   True),
    ("26.png",                                         "Interior Finishes",   "Interiors",  False),
    ("29.png",                                         "Kitchen Remodel",     "Kitchens",   True),
    ("31.png",                                         "Kitchen Remodel",     "Kitchens",   False),
    ("30.png",                                         "Bathroom Remodel",    "Bathrooms",  False),
    ("27.png",                                         "Bathroom Remodel",    "Bathrooms",  True),
    ("23.png",                                         "Interior Finishes",   "Interiors",  False),
    ("24.png",                                         "Interior Finishes",   "Interiors",  False),
    ("28.png",                                         "Kitchen Remodel",     "Kitchens",   False),
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
