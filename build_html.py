#!/usr/bin/env python3
"""Generate the DFC Home Improvement static site (v2)."""
import json, os, html

ROOT = "/Users/hugohernandez/Documentos/DFC/website/dfc-site"
M = {x["slug"]: x for x in json.load(open(os.path.join(ROOT, "manifest.json")))}

PHONE_DISP = "(703) 596-8375"
PHONE_TEL  = "+17035968375"
EMAIL      = "admin@dfchomeimprovement.com"
AREAS = ["Northern Virginia", "Fairfax", "Arlington", "Alexandria", "Falls Church",
         "Vienna", "McLean", "Richmond", "Washington DC"]
MAP_SRC = ("https://www.openstreetmap.org/export/embed.html?"
           "bbox=-77.62%2C38.62%2C-76.86%2C39.08&amp;layer=mapnik&amp;marker=38.8462%2C-77.3064")

ARROW = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" '
         'stroke-linecap="round" stroke-linejoin="round"><path d="M4 12h15M13 6l6 6-6 6"/></svg>')
ZOOM = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" '
        'stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="7"/>'
        '<path d="M21 21l-4.3-4.3M11 8v6M8 11h6"/></svg>')

# Social profiles
IG_URL = "https://www.instagram.com/dfchomeimprovement/"
FB_URL = "https://www.facebook.com/DFCHome"
IG_ICON = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" '
           'stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="2" width="20" height="20" rx="5.5"/>'
           '<circle cx="12" cy="12" r="4.3"/><circle cx="17.5" cy="6.5" r="1.2" fill="currentColor" stroke="none"/></svg>')
FB_ICON = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" '
           'stroke-linecap="round" stroke-linejoin="round"><path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/></svg>')

def img(s): return M[s]["src"]
def thumb(s): return M[s]["thumb"]

# ---------------------------------------------------------------- HEAD
def head(title, desc, page):
    jsonld = {
        "@context": "https://schema.org", "@type": "HomeAndConstructionBusiness",
        "name": "DFC Home Improvement",
        "image": "https://dfchomeimprovement.com/assets/img/218-15th-st-ne.jpg",
        "url": "https://dfchomeimprovement.com/", "telephone": PHONE_TEL, "priceRange": "$$$",
        "slogan": "Your home should feel like a vacation.",
        "description": ("Class A licensed design-build general contractor for custom homes, new "
                        "construction, additions and whole-home renovations across Northern Virginia, "
                        "Richmond and Washington DC."),
        "areaServed": AREAS,
        "aggregateRating": {"@type": "AggregateRating", "ratingValue": "4.8", "reviewCount": "30"},
    }
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script>document.documentElement.classList.add('js');</script>
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:type" content="website">
<meta property="og:image" content="assets/img/218-15th-st-ne.jpg">
<meta name="theme-color" content="#313d2c">
<link rel="icon" type="image/png" sizes="32x32" href="assets/logo/favicon-32.png">
<link rel="icon" type="image/png" sizes="64x64" href="assets/logo/favicon-64.png">
<link rel="apple-touch-icon" href="assets/logo/favicon-180.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Urbanist:wght@400;500;600;700&family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/styles.css">
<script type="application/ld+json">{json.dumps(jsonld)}</script>
</head>
<body data-page="{page}">"""

# ---------------------------------------------------------------- HEADER
def header(current):
    def link(href, label, key):
        cls = ' class="current"' if key == current else ''
        return f'<a href="{href}"{cls}>{label}</a>'
    nav = "\n      ".join([
        link("new-construction.html", "New Construction", "new"),
        link("renovations.html", "Renovations", "ren"),
        link("portfolio.html", "Portfolio", "portfolio"),
        link("index.html#areas", "Service Areas", "areas"),
        link("contact.html", "Contact", "contact"),
    ])
    m_nav = "\n        ".join([
        '<a href="index.html">Home</a>',
        '<a href="new-construction.html">New Construction</a>',
        '<a href="renovations.html">Renovations</a>',
        '<a href="portfolio.html">Portfolio</a>',
        '<a href="index.html#areas">Service Areas</a>',
        '<a href="contact.html">Contact</a>',
    ])
    return f"""
<header class="site-header" id="siteHeader">
  <a class="brand" href="index.html" aria-label="DFC Home Improvement — home">
    <img class="mark-white" src="assets/logo/dfc-mark-white.png" alt="DFC Home Improvement">
    <img class="mark-black" src="assets/logo/dfc-mark-black.png" alt="" aria-hidden="true">
  </a>
  <nav class="nav" aria-label="Primary">
      {nav}
  </nav>
  <div class="header-right">
    <a class="header-phone" href="tel:{PHONE_TEL}">{PHONE_DISP}</a>
    <a class="btn header-cta" href="contact.html">Request Evaluation</a>
    <button class="nav-toggle" id="navToggle" aria-label="Open menu" aria-expanded="false" aria-controls="mobileMenu">
      <span></span><span></span><span></span>
    </button>
  </div>
</header>
<div class="mobile-menu" id="mobileMenu" aria-hidden="true">
  <nav class="m-links" aria-label="Mobile">
        {m_nav}
  </nav>
  <div class="m-foot">
    <a href="tel:{PHONE_TEL}">{PHONE_DISP}</a>
    <a href="mailto:{EMAIL}">{EMAIL}</a>
  </div>
</div>"""

# ---------------------------------------------------------------- CTA (every page)
def cta():
    return f"""
  <section class="section cta-band">
    <div class="wrap reveal">
      <p class="eyebrow">Have something in mind?</p>
      <h2>Let's build something worth coming home to.</h2>
      <div class="cta-actions">
        <a class="btn btn--light" href="contact.html">Request a free consultation</a>
        <a class="link-arrow light" href="tel:{PHONE_TEL}">Call {PHONE_DISP} {ARROW}</a>
      </div>
    </div>
  </section>"""

# ---------------------------------------------------------------- FOOTER
def footer():
    areas = " · ".join(AREAS)
    return f"""
<footer class="site-footer">
  <div class="wrap">
    <div class="footer-top">
      <div class="footer-brand">
        <img src="assets/logo/dfc-logo-white.png" alt="DFC Home Improvement">
        <p>Class A licensed design-build general contractor. One accountable team from first concept to final walkthrough.</p>
        <div class="footer-social">
          <a href="{IG_URL}" target="_blank" rel="noopener" aria-label="DFC Home Improvement on Instagram">{IG_ICON}</a>
          <a href="{FB_URL}" target="_blank" rel="noopener" aria-label="DFC Home Improvement on Facebook">{FB_ICON}</a>
        </div>
      </div>
      <div class="footer-col">
        <h4>Explore</h4>
        <a href="index.html">Home</a>
        <a href="new-construction.html">New Construction</a>
        <a href="renovations.html">Renovations</a>
        <a href="portfolio.html">Portfolio</a>
        <a href="contact.html">Contact</a>
      </div>
      <div class="footer-col">
        <h4>Services</h4>
        <a href="new-construction.html#new-homes">Custom Homes</a>
        <a href="renovations.html#kitchen">Kitchen Remodeling</a>
        <a href="renovations.html#bathroom">Bathroom Renovation</a>
        <a href="renovations.html#full-home">Whole-Home Renovation</a>
        <a href="renovations.html#rendering">3D Design &amp; Rendering</a>
        <a href="renovations.html#design-build">Design-Build</a>
      </div>
      <div class="footer-col footer-contact">
        <h4>Get in touch</h4>
        <a class="big" href="tel:{PHONE_TEL}">{PHONE_DISP}</a>
        <a href="mailto:{EMAIL}">{EMAIL}</a>
        <p>Serving Northern Virginia, Richmond<br>&amp; Washington DC.</p>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© 2026 DFC Home Improvement. Class A Licensed &amp; Insured.</span>
      <span class="fb-right"><a href="index.html#areas">{areas}</a></span>
    </div>
  </div>
</footer>
<script src="assets/js/script.js" defer></script>
</body>
</html>"""

def page(fname, head_html, body_html, current):
    doc = head_html + header(current) + body_html + footer()
    with open(os.path.join(ROOT, fname), "w") as f:
        f.write(doc)
    print("wrote", fname, f"({len(doc)//1024} kb)")

# review helper
def review_card(quote, name, cls="review", stars="★★★★★"):
    sc = "r-stars" if cls == "review" else "gc-stars"
    return f"""        <figure class="{cls}">
          <div class="{sc}">{stars}</div>
          <blockquote><p>{quote}</p></blockquote>
          <cite>{name}</cite>
        </figure>"""

# ================================================================ HOMEPAGE
def build_index():
    notes = [
        ("Have used DFC Home Improvement for three projects so far, and will certainly continue. Each time they have been on time and professional, and they instruct me on the options I have.", "Heather Savel"),
        ("This is the second project DFC has successfully completed on my property. We have been very pleased with their work product and timely completion.", "R. Scott"),
        ("DFC handled the situation professionally and made sure the work was done correctly. Their craftsmanship was strong, and they communicated well throughout the job.", "Ash Lei"),
    ]
    notes_html = "\n".join(review_card(q, n) for q, n in notes)

    trades = ["New Homes &amp; Additions", "Dormers &amp; Roofing", "Foundations", "Kitchen Remodels",
              "Bathroom Remodels", "Decks &amp; Patios", "Electrical &amp; Plumbing", "Design-Build &amp; Rendering"]
    trades_html = "\n".join(f"          <li>{t}</li>" for t in trades)

    work = [
        ("tall", "springvale-lane", "Springvale Lane", "Custom Home"),
        ("wide", "1063-thomas-jefferson-st-4", "Thomas Jefferson St", "Interiors"),
        ("box",  "29", "Kitchen Remodel", "Kitchens"),
        ("box",  "2210-monteiro-ave", "Monteiro Avenue", "Bathrooms"),
        ("half", "2903-east-marshall-st", "East Marshall St", "Interiors"),
        ("half", "1611-polecat-lane-4", "Polecat Lane", "Interiors"),
    ]
    work_html = "\n".join(
        f"""        <a class="work-item {cls} reveal" href="portfolio.html">
          <img src="{img(s)}" alt="{html.escape(proj)} — {cat} project by DFC Home Improvement" loading="lazy">
          <div class="w-cap"><h3>{proj}</h3><span>{cat}</span></div>
        </a>""" for cls, s, proj, cat in work)

    process = [
        ("01","Evaluate","We discuss goals, site conditions, scope and budget direction, then agree on the right next step — with no pressure."),
        ("02","Plan","Design coordination, 3D renderings when useful, material selections, schedule and trade strategy are aligned before work begins."),
        ("03","Build","Licensed, insured crews manage construction with direct communication, daily accountability and a clean job site."),
        ("04","Finish","Punch list, final walkthrough and cleanup are handled with the same care as the structural work — plus warranty support."),
    ]
    process_html = "\n".join(
        f"""        <div class="p-row reveal"><div class="p-no">{n}</div><h3>{t}</h3><p>{b}</p></div>"""
        for n, t, b in process)

    stats = [("A","Class A licensed contractor"),("1","Accountable team, concept to finish"),
             ("9","Cities &amp; counties served"),("5.0","Average client rating")]
    stats_html = "\n".join(
        f"""        <div class="stat reveal d{i}"><div class="s-num">{n}</div><div class="s-lab">{l}</div></div>"""
        for i, (n, l) in enumerate(stats, 1))

    areas_html = "\n".join(f'            <span>{a}</span>' for a in AREAS)

    body = f"""
<main id="top">

  <!-- HERO -->
  <section class="hero">
    <div class="hero-bg"><img src="{img('218-15th-st-ne')}" alt="Refined living room renovated by DFC Home Improvement" fetchpriority="high"></div>
    <div class="hero-inner">
      <img class="hero-logo" src="assets/logo/dfc-logo-white.png" alt="DFC Home Improvement">
      <h1>Your home should feel like a vacation.</h1>
      <p class="hero-kicker">Class A Design–Build · Northern Virginia · Richmond · DC</p>
      <div class="hero-actions">
        <a class="btn btn--light" href="contact.html">Request a free consultation</a>
        <a class="btn btn--light" href="portfolio.html" style="background:rgba(255,255,255,.08)">View our work</a>
      </div>
    </div>
  </section>

  <!-- RATING STRIP -->
  <section class="rating-strip">
    <div class="wrap rs-inner">
      <div class="rs-stars" aria-hidden="true">★★★★★</div>
      <div class="rs-score"><strong>4.8</strong> / 5 on Google Reviews</div>
      <div class="rs-note">Rated by homeowners across Northern Virginia, DC &amp; Richmond</div>
    </div>
  </section>

  <!-- WHO WE ARE (sage) -->
  <section class="section bg-sage who">
    <div class="wrap">
      <div class="split split--center">
        <div class="reveal">
          <p class="eyebrow">Who we are</p>
          <h2>A more deliberate way to build, remodel and invest in your home.</h2>
        </div>
        <div class="body reveal d1">
          <p>DFC Home Improvement is a Class A licensed general contractor and design-build specialist serving Northern Virginia — Fairfax, Arlington, Alexandria, Falls Church, Vienna and McLean — as well as Richmond and Washington DC.</p>
          <p>We help homeowners move from concept to construction with one team handling planning, design coordination, budgeting, trade management and finish work — so your project stays organized and on schedule from first walkthrough to the last detail.</p>
          <p style="margin-top:1.6em"><a class="link-arrow" href="renovations.html">Explore what we do {ARROW}</a></p>
        </div>
      </div>
    </div>
  </section>

  <!-- SERVICE PILLARS -->
  <section class="section wrap">
    <div class="head-row">
      <div class="reveal"><p class="eyebrow">What we build</p><h2>Two ways we bring homes to life.</h2></div>
      <p class="h-right reveal d1">Whether you're building from the ground up or reimagining the home you're in, every trade is coordinated in-house under one accountable team.</p>
    </div>
    <div class="pillars">
      <a class="pillar reveal" href="new-construction.html">
        <img src="{img('1611-polecat-lane')}" alt="New custom home construction by DFC Home Improvement" loading="lazy">
        <div class="p-body">
          <div class="p-num">01 — Build new</div>
          <h3>New Construction</h3>
          <p>Custom homes, additions, dormers, roofing and foundations — full-service construction from land to move-in.</p>
          <span class="link-arrow light">Explore new construction {ARROW}</span>
        </div>
      </a>
      <a class="pillar reveal d1" href="renovations.html">
        <img src="{img('1063-thomas-jefferson-st')}" alt="Whole-home renovation by DFC Home Improvement" loading="lazy">
        <div class="p-body">
          <div class="p-num">02 — Reimagine</div>
          <h3>Renovations</h3>
          <p>Kitchens, bathrooms, whole-home remodels and design-build — refined spaces tailored to the way you live.</p>
          <span class="link-arrow light">Explore renovations {ARROW}</span>
        </div>
      </a>
    </div>
    <ul class="trades reveal">
{trades_html}
    </ul>
  </section>

  <!-- FEATURE BAND -->
  <section class="feature bg-night">
    <div class="f-copy reveal">
      <p class="eyebrow on-dark">Craft &amp; finishes</p>
      <h2>Rooms finished with architectural restraint and lasting detail.</h2>
      <p style="margin-top:1.4em;color:rgba(255,255,255,.74)">Custom millwork, stone, tile and lighting brought together with clean communication and a job site held to a higher standard.</p>
      <p style="margin-top:2rem"><a class="link-arrow light" href="portfolio.html">See the portfolio {ARROW}</a></p>
    </div>
    <div class="f-img"><img src="{img('617-elliot-st-ne')}" alt="Renovated living room with custom fireplace and hardwood floors" loading="lazy"></div>
  </section>

  <!-- SELECTED WORK -->
  <section class="section wrap">
    <div class="head-row">
      <div class="reveal"><p class="eyebrow">Selected work</p><h2>Recent homes &amp; renovations.</h2></div>
      <p class="h-right reveal d1">Custom homes, full renovations, kitchens and baths completed across the region.</p>
    </div>
    <div class="work-grid">
{work_html}
    </div>
    <div style="margin-top:clamp(34px,4vw,54px)" class="reveal"><a class="btn" href="portfolio.html">View full portfolio</a></div>
  </section>

  <!-- PROCESS -->
  <section class="section bg-paper" id="process">
    <div class="wrap">
      <div class="head-row">
        <div class="reveal"><p class="eyebrow">Our process</p><h2>One accountable team, from consultation to final walkthrough.</h2></div>
        <p class="h-right reveal d1">No subcontracting confusion, no finger-pointing — just a clear path and a single point of responsibility.</p>
      </div>
      <div class="process">
{process_html}
      </div>
    </div>
  </section>

  <!-- STATS -->
  <section class="section--tight bg-night">
    <div class="wrap"><div class="stats">
{stats_html}
    </div></div>
  </section>

  <!-- CLIENT NOTES -->
  <section class="section wrap">
    <div class="head-row">
      <div class="reveal"><p class="eyebrow">Client notes</p><h2>Trusted for communication, craft and complicated work.</h2></div>
      <p class="h-right reveal d1">A few words from homeowners across Northern Virginia, DC and Richmond.</p>
    </div>
    <div class="reviews-grid">
{notes_html}
    </div>
  </section>

  <!-- SERVICE AREAS + MAP -->
  <section class="section bg-sage" id="areas">
    <div class="wrap">
      <div class="areas-grid">
        <div class="reveal">
          <p class="eyebrow">Service areas</p>
          <h2>Building across Northern Virginia, Richmond &amp; DC.</h2>
          <p style="margin-top:1.2em">We work throughout the region's most established residential communities. Don't see your town? Reach out — we likely cover it.</p>
          <div class="areas-list">
{areas_html}
          </div>
        </div>
        <iframe class="area-map reveal d1" title="DFC Home Improvement service area map" loading="lazy" src="{MAP_SRC}"></iframe>
      </div>
    </div>
  </section>
{cta()}
</main>"""
    page("index.html",
         head("DFC Home Improvement | Custom Homes & Renovations in Northern Virginia",
              "Class A licensed design-build contractor for custom homes, new construction, additions and whole-home renovations across Northern Virginia, Richmond and Washington DC.",
              "home"),
         body, "home")

# ================================================================ NEW CONSTRUCTION
def build_new_construction():
    bullets_newhomes = ["Land evaluation, site prep &amp; grading", "Work from your plans or design from scratch",
                        "Foundation through interior finishes", "Transparent, detailed budgeting",
                        "Daily project management &amp; communication", "Warranty &amp; post-build support"]
    cards = [
        ("Dormers", "Add curb appeal, natural light and usable headroom. Planned early in the build for correct framing, weatherproofing and a roofline that looks custom.",
         ["Shed, gable &amp; hip dormers", "Framing &amp; load coordination", "Flashing &amp; weatherproofing", "Matched siding &amp; trim"]),
        ("Foundations", "Slab, crawl space or basement — engineered to your site's soil and elevation, and built to meet or exceed local code from groundbreaking through framing.",
         ["Excavation, grading &amp; drainage", "Footings &amp; stem-wall pours", "Slab, crawl space or basement", "Waterproofing &amp; rebar systems"]),
        ("Roofing", "Code-compliant roofing for new builds, coordinated to your construction schedule using trusted material systems and backed by labor and manufacturer warranties.",
         ["Architectural &amp; asphalt shingles", "Metal &amp; designer systems", "Underlayment &amp; flashing", "Ventilation, gutters &amp; downspouts"]),
    ]
    cards_html = "\n".join(
        f"""        <article class="reveal d{i}">
          <h3>{t}</h3>
          <p style="margin:14px 0 18px;color:var(--ink-soft)">{d}</p>
          <ul style="list-style:none;padding:0;margin:0;border-top:1px solid var(--line)">
            {''.join(f'<li style="padding:12px 0;border-bottom:1px solid var(--line);color:var(--ink)">{b}</li>' for b in bl)}
          </ul>
        </article>""" for i, (t, d, bl) in enumerate(cards, 1))

    faqs = [
        ("How long does it take to build a custom home?", "Most builds take 6–12 months from groundbreaking to move-in, depending on size, complexity and permitting."),
        ("Do I need architectural plans before starting?", "Not necessarily. We can work from your existing plans or help connect you with architects and designers to develop a plan from scratch."),
        ("What does building a custom home cost?", "Costs depend on square footage, finishes and land conditions. We provide detailed, transparent estimates and help you stay within your budget."),
        ("Can I make changes during the build?", "Yes, within reason. We allow flexibility where possible and keep you informed on how changes affect cost and timeline."),
        ("What type of foundation is best for my home?", "It depends on your site's soil, elevation and home design — we'll recommend the right option: slab, crawl space or basement."),
        ("Do dormers add value and usable space?", "Yes. Dormers increase curb appeal, natural light and functional space — and shed dormers in particular add real headroom on second floors and attics."),
        ("What roofing materials do you offer for new homes?", "Asphalt and architectural shingles, metal and designer roofing systems from trusted brands — we'll help you choose the best fit for your design and budget."),
        ("Is the work backed by a warranty?", "Absolutely. Our homes and systems come with labor and manufacturer warranties, plus continued support after completion."),
    ]
    faq_html = "\n".join(
        f"""        <details{' open' if i==0 else ''}>
          <summary>{q}</summary>
          <div class="faq-a"><p>{a}</p></div>
        </details>""" for i, (q, a) in enumerate(faqs))

    body = f"""
<main id="top">
  <section class="page-hero">
    <div class="ph-bg"><img src="{img('1611-polecat-lane')}" alt="New custom home built by DFC Home Improvement"></div>
    <div class="ph-inner">
      <p class="breadcrumb reveal"><a href="index.html">Home</a> / New Construction</p>
      <h1 class="reveal">New construction, built right from the ground up.</h1>
      <p class="reveal d1">Custom homes, additions, dormers, foundations and roofing — full-service construction managed by one accountable, Class A licensed team.</p>
    </div>
  </section>

  <!-- New Homes feature row -->
  <section class="section wrap" id="new-homes">
    <div class="svc-row">
      <div class="stmt reveal">
        <p class="eyebrow">Custom Homes</p>
        <h2>New homes designed around your life.</h2>
        <p style="margin-top:1.1em">From land evaluation through final move-in, we guide you through architecture, permitting, foundation, framing and finishes — treating each build as a personal reflection of how you want to live.</p>
        <ul>{''.join(f'<li>{b}</li>' for b in bullets_newhomes)}</ul>
      </div>
      <div class="media reveal d1"><img src="{img('1611-polecat-lane-4')}" alt="Interior of a new home built by DFC Home Improvement" loading="lazy"></div>
    </div>
  </section>

  <!-- Dormers / Foundations / Roofing cards -->
  <section class="section bg-sage">
    <div class="wrap">
      <div class="head-row">
        <div class="reveal"><p class="eyebrow">Structural &amp; exterior</p><h2>The build, handled end to end.</h2></div>
        <p class="h-right reveal d1">Planned early and executed in-house so the framing, roofline and weatherproofing are right the first time.</p>
      </div>
      <div class="svc-grid" style="display:grid;grid-template-columns:repeat(3,1fr);gap:clamp(20px,2.6vw,40px)">
{cards_html}
      </div>
    </div>
  </section>

  <!-- FAQ -->
  <section class="section wrap">
    <div class="head-row simple reveal" style="display:block;max-width:60ch;margin-bottom:clamp(34px,4vw,56px)">
      <p class="eyebrow">Good to know</p><h2>New construction questions, answered.</h2>
    </div>
    <div class="faq reveal" style="margin-inline:0">
{faq_html}
    </div>
  </section>
{cta()}
</main>"""
    page("new-construction.html",
         head("New Construction | DFC Home Improvement — Custom Homes, Dormers, Foundations & Roofing",
              "DFC Home Improvement builds custom homes and handles new-construction dormers, foundations and roofing across Northern Virginia and Richmond — one Class A licensed team from land to move-in.",
              "new"),
         body, "new")

# ================================================================ RENOVATIONS
def build_renovations():
    rows = [
        ("kitchen", "Kitchen Remodeling", "01", "218-15th-st-ne-2", False,
         "A unified team handles layout, cabinetry, countertops, tile and electrical — improving how your kitchen works as much as how it looks.",
         ["Full renovations &amp; reconfigurations", "Custom cabinetry &amp; islands", "Countertops, backsplash &amp; tile", "Flooring, trim, paint &amp; appliances"]),
        ("bathroom", "Bathroom Renovations", "02", "2210-monteiro-ave", True,
         "Demolition, waterproofing, tile, plumbing and finish carpentry coordinated as one accountable job — built for durability and a spa-grade feel.",
         ["Primary, guest &amp; powder baths", "Custom tile showers &amp; waterproofing", "Vanities, lighting &amp; fixtures", "Glass, flooring &amp; finish detail"]),
        ("full-home", "Whole-Home Renovations", "03", "617-elliot-st-ne", False,
         "Kitchen and bath updates, room expansions, basement finishing and exterior improvements — managed start to finish with one point of responsibility.",
         ["Layout reconfiguration &amp; additions", "Basement finishing", "Structural repairs", "Exterior &amp; full-home finish upgrades"]),
    ]
    blocks = []
    for rid, title, no, slug, rev, desc, bl in rows:
        media = f'<div class="media reveal"><img src="{img(slug)}" alt="{html.escape(title)} by DFC Home Improvement" loading="lazy"></div>'
        copy = f"""<div class="stmt reveal d1">
          <p class="eyebrow">{no} — Renovation</p>
          <h2>{title}</h2>
          <p style="margin-top:1.1em">{desc}</p>
          <ul>{''.join(f'<li>{b}</li>' for b in bl)}</ul>
        </div>"""
        order = (media, copy) if not rev else (copy, media)
        blocks.append(f"""
  <section class="section{' bg-paper' if rev else ''}" id="{rid}">
    <div class="wrap"><div class="svc-row{' rev' if rev else ''}">{order[0]}{order[1]}</div></div>
  </section>""")

    phases = [
        ("01","Discovery","Consultation, goals, lifestyle needs and early budget direction."),
        ("02","Concept planning","Layout ideas, scope definition and material direction."),
        ("03","Design development","Drawings, selections, specifications and pricing alignment."),
        ("04","Pre-construction","Permits, ordering, scheduling and final production planning."),
        ("05","Construction","Project management, quality control, communication and delivery."),
    ]
    phases_html = "\n".join(
        f"""        <div class="p-row reveal"><div class="p-no">{n}</div><h3>{t}</h3><p>{d}</p></div>"""
        for n, t, d in phases)

    body = f"""
<main id="top">
  <section class="page-hero">
    <div class="ph-bg"><img src="{img('1063-thomas-jefferson-st')}" alt="Whole-home renovation by DFC Home Improvement"></div>
    <div class="ph-inner">
      <p class="breadcrumb reveal"><a href="index.html">Home</a> / Renovations</p>
      <h1 class="reveal">Renovations that reimagine the home you're in.</h1>
      <p class="reveal d1">Kitchens, bathrooms and whole-home remodels — designed and built by one team, from first sketch to final walkthrough.</p>
    </div>
  </section>
{''.join(blocks)}

  <!-- 3D Design & Rendering -->
  <section class="section bg-paper" id="rendering">
    <div class="wrap"><div class="svc-row rev">
        <div class="stmt reveal d1">
          <p class="eyebrow">3D Design &amp; Rendering</p>
          <h2>See your project before we build it.</h2>
          <p style="margin-top:1.1em">Before demolition starts, we turn your ideas into photoreal 3D renderings — so you can walk through the layout, finishes, lighting and materials and approve every detail with confidence. Visualizing the finished space up front means fewer surprises, fewer change orders, and a result that matches the vision.</p>
          <ul><li>Photoreal interior &amp; exterior renderings</li><li>Kitchen, bath &amp; whole-home visualizations</li><li>Material, color &amp; finish previews</li><li>Layout &amp; floor-plan studies before construction</li></ul>
          <p style="margin-top:1.6em"><a class="link-arrow" href="portfolio.html">See 3D designs in the portfolio {ARROW}</a></p>
        </div>
        <div class="media reveal"><img src="{img('3d-sage-kitchen-1')}" alt="Photoreal 3D kitchen rendering by DFC Home Improvement" loading="lazy"></div>
    </div></div>
  </section>

  <!-- Design-Build process -->
  <section class="section bg-sage" id="design-build">
    <div class="wrap">
      <div class="head-row">
        <div class="reveal"><p class="eyebrow">Design-Build</p><h2>Design and construction, under one roof.</h2></div>
        <p class="h-right reveal d1">One team guides planning, design, budgeting, selections and construction — which keeps accountability clear and reduces budget surprises and change orders.</p>
      </div>
      <div class="process" style="border-top-color:rgba(13,8,5,.16)">
{phases_html}
      </div>
    </div>
  </section>
{cta()}
</main>"""
    page("renovations.html",
         head("Renovations | DFC Home Improvement — Kitchens, Bathrooms & Whole-Home Remodels",
              "Kitchen and bathroom remodeling, whole-home renovations and design-build from DFC Home Improvement across Northern Virginia, Richmond and Washington DC.",
              "ren"),
         body, "ren")

# ================================================================ PORTFOLIO
def build_portfolio():
    cats = ["All", "Kitchens", "Bathrooms", "Interiors", "3D Designs"]
    filt = "\n".join(
        f'        <button class="{"active" if c=="All" else ""}" data-filter="{c.lower()}">{c}</button>'
        for c in cats)
    order = sorted(M.values(), key=lambda x: (not x["featured"], x["project"]))
    figs = []
    for x in order:
        figs.append(
            f"""        <figure data-category="{x['category'].lower()}" data-full="{x['src']}" data-proj="{html.escape(x['project'])}" data-cat="{x['category']}">
          <img src="{x['thumb']}" alt="{html.escape(x['project'])} — {x['category']} project by DFC Home Improvement" loading="lazy">
          <span class="g-zoom" aria-hidden="true">{ZOOM}</span>
        </figure>""")
    body = f"""
<main id="top">
  <section class="page-hero">
    <div class="ph-bg"><img src="{img('springvale-lane')}" alt="Custom home by DFC Home Improvement at dusk"></div>
    <div class="ph-inner">
      <p class="breadcrumb reveal"><a href="index.html">Home</a> / Portfolio</p>
      <h1 class="reveal">A portfolio of custom homes, renovations &amp; finishes.</h1>
      <p class="reveal d1">Real projects across Northern Virginia, Washington DC and Richmond. Filter by space, or click any image to view it larger.</p>
    </div>
  </section>
  <section class="section--tight wrap">
    <div class="filters reveal" id="filters">
{filt}
    </div>
    <div class="gallery" id="gallery">
{chr(10).join(figs)}
    </div>
  </section>
{cta()}
</main>
<div class="lightbox" id="lightbox" aria-hidden="true" role="dialog" aria-label="Project image">
  <button class="lb-close" id="lbClose" aria-label="Close">✕</button>
  <button class="lb-nav lb-prev" id="lbPrev" aria-label="Previous">‹</button>
  <img id="lbImg" src="" alt="">
  <button class="lb-nav lb-next" id="lbNext" aria-label="Next">›</button>
  <div class="lb-cap" id="lbCap"></div>
</div>"""
    page("portfolio.html",
         head("Portfolio | DFC Home Improvement — Custom Homes & Renovations",
              "Browse completed DFC Home Improvement projects: custom homes, kitchens, bathrooms and full interior renovations across Northern Virginia, DC and Richmond.",
              "portfolio"),
         body, "portfolio")

# ================================================================ CONTACT
def build_contact():
    areas = " · ".join(AREAS)
    body = f"""
<main id="top">
  <section class="page-hero">
    <div class="ph-bg"><img src="{img('218-15th-st-ne-2')}" alt="Kitchen remodeled by DFC Home Improvement"></div>
    <div class="ph-inner">
      <p class="breadcrumb reveal"><a href="index.html">Home</a> / Contact</p>
      <h1 class="reveal">Let's talk about your project.</h1>
      <p class="reveal d1">Tell us a little about what you have in mind. We'll follow up to schedule your free evaluation — no obligation, honest pricing, expert guidance.</p>
    </div>
  </section>
  <section class="section--tight wrap">
    <div class="contact-grid">
      <div class="contact-info reveal">
        <div class="ci-block"><div class="ci-lab">Call or text</div><div class="ci-val"><a href="tel:{PHONE_TEL}">{PHONE_DISP}</a></div></div>
        <div class="ci-block"><div class="ci-lab">Email</div><div class="ci-val"><a href="mailto:{EMAIL}">{EMAIL}</a></div></div>
        <div class="ci-block"><div class="ci-lab">Service area</div><div class="ci-val small">{areas}</div></div>
        <div class="ci-block"><div class="ci-lab">Credentials</div><div class="ci-val small">Class A Licensed General Contractor · Licensed &amp; Insured · Design-Build</div></div>
        <div class="ci-block"><div class="ci-lab">Response time</div><div class="ci-val small">We follow up on new requests within 24 hours.</div></div>
      </div>
      <div class="form-card reveal d1">
        <div class="fc-title">Request a free consultation</div>
        <p class="fc-sub">Fields marked <span style="color:var(--accent)">*</span> are required.</p>
        <form class="lead-form" id="leadForm" action="https://formsubmit.co/{EMAIL}" method="POST">
          <input type="hidden" name="_subject" value="New website lead — DFC Home Improvement">
          <input type="hidden" name="_template" value="table">
          <input type="hidden" name="_captcha" value="false">
          <input type="text" name="_honey" tabindex="-1" autocomplete="off" style="position:absolute;left:-9999px" aria-hidden="true">
          <div class="field"><label for="name">Full name <span class="req">*</span></label><input id="name" name="name" type="text" autocomplete="name" placeholder="Jane Smith" required></div>
          <div class="field"><label for="phone">Phone <span class="req">*</span></label><input id="phone" name="phone" type="tel" autocomplete="tel" placeholder="(703) 000-0000" required></div>
          <div class="field"><label for="email">Email <span class="req">*</span></label><input id="email" name="email" type="email" autocomplete="email" placeholder="you@email.com" required></div>
          <div class="field"><label for="address">Project address</label><input id="address" name="address" type="text" autocomplete="street-address" placeholder="City or full address"></div>
          <div class="field wide"><label for="type">Project type</label>
            <select id="type" name="project_type">
              <option>Custom home / new construction</option>
              <option>Whole-home renovation / addition</option>
              <option>Kitchen remodel</option>
              <option>Bathroom remodel</option>
              <option>Deck / patio / exterior</option>
              <option>3D design / rendering</option>
              <option>Other</option>
            </select>
          </div>
          <div class="field wide"><label for="message">Tell us about your project</label><textarea id="message" name="message" rows="5" placeholder="What are you hoping to build or change?"></textarea></div>
          <div class="form-actions">
            <button class="btn btn--sage" type="submit">Send request</button>
            <span class="form-note">Prefer to talk? Call <a href="tel:{PHONE_TEL}">{PHONE_DISP}</a>.</span>
          </div>
        </form>
      </div>
    </div>
  </section>
{cta()}
</main>"""
    page("contact.html",
         head("Contact | DFC Home Improvement — Request a Free Consultation",
              "Request a free consultation with DFC Home Improvement. Call (703) 596-8375 or send your project details. Serving Northern Virginia, Richmond and Washington DC.",
              "contact"),
         body, "contact")

if __name__ == "__main__":
    build_index()
    build_new_construction()
    build_renovations()
    build_portfolio()
    build_contact()
    # remove the old services page if present
    old = os.path.join(ROOT, "services.html")
    if os.path.exists(old): os.remove(old); print("removed services.html")
    print("done.")
