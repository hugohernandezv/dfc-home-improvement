#!/usr/bin/env python3
"""Prepare web assets for the DFC Home Improvement site:
   - trim/recolor the logo (white + black + favicon)
   - optimize the heavy source photos into web JPEGs (large + thumb)
   - emit a manifest.json describing the gallery."""
import json, re, os
from PIL import Image, ImageFilter, ImageDraw

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
    # white house mark on a sage-green rounded square — visible on light OR dark browser tabs
    ma = mark.split()[-1]
    white = Image.merge("RGBA", (Image.new("L",mark.size,255), Image.new("L",mark.size,255), Image.new("L",mark.size,255), ma))
    side = int(max(mark.size) * 1.5)
    canvas = Image.new("RGBA", (side, side), (0x31,0x3d,0x2c,255))
    rmask = Image.new("L", (side, side), 0)
    ImageDraw.Draw(rmask).rounded_rectangle([0,0,side-1,side-1], radius=int(side*0.22), fill=255)
    canvas.putalpha(rmask)
    mw = int(side*0.62); sc = mw/white.width; mh = int(white.height*sc)
    canvas.alpha_composite(white.resize((mw,mh), Image.LANCZOS), ((side-mw)//2, (side-mh)//2))
    for sz in (180, 64, 32):
        canvas.resize((sz,sz), Image.LANCZOS).save(os.path.join(LOGO, f"favicon-{sz}.png"))
    print("logo:", im.size, "-> white/black/favicon done")

# ---------- PHOTOS ----------
# (filename, project, category, featured-on-home)
PHOTOS = [
    # Kitchens (hi-res project photos)
    ("Kitchen Springvale Lane.png",  "Springvale Lane",     "Homepage",  False),
    ("Kitchen Thomas Jefferson.png", "Thomas Jefferson St", "Homepage",  True),
    ("Kitchen Polecat Lane.png",     "Polecat Lane",        "Homepage",  False),
    ("Kitchen Reymet Road.png",      "Reymet Road",         "Homepage",  False),
    ("Kitchen 15th Street NE.png",   "15th Street NE",      "Homepage",  True),
    ("Kitchen Monteiro Ave.png",     "Monteiro Avenue",     "Homepage",  True),
    ("Kitchen North Ave.png",        "North Avenue",        "Homepage",  False),
    ("Kitchen East Marshall.png",    "East Marshall St",    "Homepage",  True),
    ("Kitchen Channing Street.png",  "Channing Street",     "Homepage",  False),
    ("Kitchen Elliott Street.png",   "Elliott Street NE",   "Homepage",  False),
    # Bathrooms (hi-res project photos)
    ("Bath Springvale Lane.png",     "Springvale Lane",     "Homepage", False),
    ("Bath Thomas Jefferson.png",    "Thomas Jefferson St", "Homepage", False),
    ("Bath Polecat Lane.png",        "Polecat Lane",        "Homepage", True),
    ("Bath Reymet Road.png",         "Reymet Road",         "Homepage", False),
    ("Bath 15th Street NE.png",      "15th Street NE",      "Homepage", True),
    ("Bath Monteiro Ave.png",        "Monteiro Avenue",     "Homepage", True),
    ("Bath North Ave.png",           "North Avenue",        "Homepage", False),
    ("Bath Channing Street.png",     "Channing Street",     "Homepage", False),
    ("Bath Elliott Street.png",      "Elliott Street NE",   "Homepage", False),
    ("Bath Marble Suite.png",        "Marble Suite",        "Homepage", True),
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
# Portfolio galleries (from Canva, 2x export, watermark cropped)
PHOTOS += [(f"Kitchen Gallery {i:02d}.png",   "Kitchen",                "Kitchens",                 False) for i in range(1, 26)]
PHOTOS += [(f"Bath Gallery {i:02d}.png",      "Bathroom",               "Bathrooms",                False) for i in range(1, 16)]
PHOTOS += [(f"WholeHome Gallery {i:02d}.png", "Whole-Home Renovation",  "Whole-Home Renovations",   False) for i in range(1, 10)]
# Added designs: 3D renders (project Perspectives PDFs) + Sample Works photos
PHOTOS += [
    ("3D Ginger 1.png",   "3D Rendering", "3D Designs", False),
    ("3D Ginger 2.png",   "3D Rendering", "3D Designs", False),
    ("3D Emily 1.png",    "3D Rendering", "3D Designs", False),
    ("3D Emily 2.png",    "3D Rendering", "3D Designs", False),
    ("3D Emily 3.png",    "3D Rendering", "3D Designs", False),
    ("3D Emily 4.png",    "3D Rendering", "3D Designs", False),
    ("3D Emily 5.png",    "3D Rendering", "3D Designs", False),
    ("3D Bradley 1.png",  "3D Rendering", "3D Designs", False),
    ("3D Bradley 2.png",  "3D Rendering", "3D Designs", False),
    ("3D Cook 1.png",     "3D Rendering", "3D Designs", False),
    ("3D Cook 2.png",     "3D Rendering", "3D Designs", False),
    ("3D Cook 3.png",     "3D Rendering", "3D Designs", False),
    ("3D Brendan 1.png",  "3D Rendering", "3D Designs", False),
    ("3D Brendan 2.png",  "3D Rendering", "3D Designs", False),
    ("3D Brendan 3.png",  "3D Rendering", "3D Designs", False),
    ("3D Bridetta 1.png", "3D Rendering", "3D Designs", False),
    ("3D Bridetta 2.png", "3D Rendering", "3D Designs", False),
    ("3D Bridetta 3.png", "3D Rendering", "3D Designs", False),
    ("3D Harry 1.png",    "3D Rendering", "3D Designs", False),
    ("3D Harry 2.png",    "3D Rendering", "3D Designs", False),
    ("3D Harry 3.png",    "3D Rendering", "3D Designs", False),
    ("Sample Kitchen 01.png", "Featured Kitchen",    "Kitchens",               False),
    ("Sample Bath 01.png",    "Featured Bathroom",   "Bathrooms",              False),
    ("Sample Bath 02.png",    "Featured Bathroom",   "Bathrooms",              False),
    ("Sample Living 01.png",  "Featured Renovation", "Whole-Home Renovations", False),
    ("Sample Living 02.png",  "Featured Renovation", "Whole-Home Renovations", False),
]
# Redfin listing kitchen photos (MLS logo cropped off)
PHOTOS += [(f"Redfin Kitchen {i:02d}.png", "Featured Kitchen", "Kitchens", False) for i in range(1, 7)]

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
        lg = lg.filter(ImageFilter.UnsharpMask(radius=1.4, percent=85, threshold=2))
        lg.save(os.path.join(IMG, slug+".jpg"), "JPEG", quality=86, optimize=True, progressive=True)
        # thumb (long side 900)
        ts = min(1.0, 900/max(w,h))
        th = im.resize((round(w*ts), round(h*ts)), Image.LANCZOS) if ts<1 else im
        th = th.filter(ImageFilter.UnsharpMask(radius=1.0, percent=80, threshold=2))
        th.save(os.path.join(IMG, slug+"-thumb.jpg"), "JPEG", quality=82, optimize=True, progressive=True)
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
