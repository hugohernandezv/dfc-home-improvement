# DFC Home Improvement — Website

A professional static website for DFC Home Improvement. Design language is inspired by the
**Minnaro** interior-design/architecture theme (Urbanist + DM Sans typography, near-black on
warm-white with a subtle sage-green accent, generous whitespace, photo-led layouts). Content and
structure follow the current dfchomeimprovement.com site.

## Pages
| File | Purpose |
|------|---------|
| `index.html` | Homepage — full-bleed hero, Google-review strip, "who we are", New Construction / Renovations pillars, featured work, process, stats, client reviews, service areas + map, CTA |
| `new-construction.html` | Custom homes, dormers, foundations & roofing — with an FAQ section |
| `renovations.html` | Kitchens, bathrooms, whole-home remodels & the design-build process |
| `portfolio.html` | Filterable gallery (Kitchens / Bathrooms / Interiors) + click-to-zoom lightbox |
| `contact.html` | Photo hero, clear request form, company info |

Every page ends with the green "Have something in mind?" call-to-action.

## Tech
- Plain HTML / CSS / JS — **no build step required to run**. Open the files or host them.
- Fonts: Urbanist + DM Sans (Google Fonts).
- `assets/css/styles.css` — the full design system (sage-green + warm-neutral palette).
- `assets/js/script.js` — sticky/transparent header, mobile menu, scroll-reveal, portfolio filter + lightbox.
- `assets/img/` — web-optimized photos (full `*.jpg` ≈250 KB + `*-thumb.jpg`).
- `assets/logo/` — full logo (white/black), compact "DFC" mark (white/black) for the menu bar, favicons.

## Preview locally
```bash
cd dfc-site
python3 -m http.server 8000
# then open http://localhost:8000
```

## Two things to fill in before going live
1. **Business email** — placeholder `office@dfchomeimprovement.com` (footer, contact, menu). Replace with the real address.
2. **Contact form delivery** — the form posts to a placeholder Formspree URL (`https://formspree.io/f/your-form-id`).
   Until connected it shows a "please call" message. Create a free form at [formspree.io](https://formspree.io)
   (or use your own backend / Jobber web form) and replace the `action` URL in `contact.html`.

## Regenerating
Two scripts produce the optimized images and the HTML (re-run only if content or photos change):
```bash
python3 build_assets.py   # optimizes photos from ../photos/Photos, builds the logos, writes manifest.json
python3 build_html.py     # regenerates all .html pages from the manifest + content
```
- Source photos: `../photos/Photos/`  ·  Logo source: `~/Desktop/DFC Logo/concept-3.png`
- Photo categories (Kitchens / Bathrooms / Interiors / Exteriors) are set in the `PHOTOS` list in `build_assets.py`.
- `montage.py` builds a labeled contact sheet of all photos (handy when re-checking categories).

## Service area
Northern Virginia · Fairfax · Arlington · Alexandria · Falls Church · Vienna · McLean · Richmond · Washington DC

## Deploy (any static host)
Upload the `dfc-site` folder to Netlify, Vercel, Cloudflare Pages, or GitHub Pages, then point
`dfchomeimprovement.com` at it. No server needed.

---
Phone: (301) 237-9555 · Class A Licensed & Insured · "Your home should feel like a vacation."
