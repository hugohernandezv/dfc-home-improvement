#!/usr/bin/env python3
"""Build a labeled contact sheet of all project photos so categories can be verified."""
import os, math
from PIL import Image, ImageDraw, ImageFont
IMG = "/Users/hugohernandez/Documentos/DFC/website/dfc-site/assets/img"
thumbs = sorted([f for f in os.listdir(IMG) if f.endswith("-thumb.jpg")])
cols, cw, ch, lab = 4, 360, 230, 26
rows = math.ceil(len(thumbs)/cols)
W, H = cols*cw, rows*(ch+lab)
sheet = Image.new("RGB", (W, H), (20,18,16))
try: font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 16)
except: font = ImageFont.load_default()
d = ImageDraw.Draw(sheet)
for i, t in enumerate(thumbs):
    r, c = divmod(i, cols)
    x, y = c*cw, r*(ch+lab)
    im = Image.open(os.path.join(IMG, t)).convert("RGB")
    im.thumbnail((cw-8, ch-8))
    sheet.paste(im, (x+4, y+4))
    d.text((x+6, y+ch-2), t.replace("-thumb.jpg",""), fill=(255,255,255), font=font)
sheet.save("/tmp/dfc_montage.jpg", quality=85)
print("wrote /tmp/dfc_montage.jpg", sheet.size, "tiles:", len(thumbs))
