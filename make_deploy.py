#!/usr/bin/env python3
"""Build a lean deploy copy (smaller images) so the Railway upload completes reliably."""
import os, shutil
from PIL import Image
SRC = "/Users/hugohernandez/Documentos/DFC/website/dfc-site"
DST = "/tmp/dfc-deploy"
shutil.rmtree(DST, ignore_errors=True)
shutil.copytree(SRC, DST)
# drop build-only files from the deploy context
for f in ["build_assets.py", "build_html.py", "montage.py", "make_deploy.py", "manifest.json", "README.md"]:
    p = os.path.join(DST, f)
    if os.path.exists(p):
        os.remove(p)
# re-compress JPGs smaller (still good for web, much smaller upload)
imgdir = os.path.join(DST, "assets/img")
for fn in sorted(os.listdir(imgdir)):
    if not fn.endswith(".jpg"):
        continue
    p = os.path.join(imgdir, fn)
    im = Image.open(p).convert("RGB")
    thumb = fn.endswith("-thumb.jpg")
    maxd, q = (480, 56) if thumb else (1120, 60)
    w, h = im.size
    s = min(1.0, maxd / max(w, h))
    if s < 1:
        im = im.resize((round(w*s), round(h*s)), Image.LANCZOS)
    im.save(p, "JPEG", quality=q, optimize=True, progressive=True)
tot = sum(os.path.getsize(os.path.join(dp, f)) for dp, _, fs in os.walk(DST) for f in fs)
print(f"deploy dir: {tot/1024/1024:.2f} MB")
