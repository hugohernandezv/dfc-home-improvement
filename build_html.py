#!/usr/bin/env python3
"""Generate the DFC Home Improvement static site (v2)."""
import json, os, html

ROOT = "/Users/hugohernandez/Documentos/DFC/website/dfc-site"
M = {x["slug"]: x for x in json.load(open(os.path.join(ROOT, "manifest.json")))}

PHONE_DISP = "(703) 596-8375"
PHONE_TEL  = "+17035968375"
EMAIL      = "admin@dfchomeimprovement.com"
# Jobber public work-request form ("Request Evaluation" CTA)
JOBBER_FORM = "https://clienthub.getjobber.com/client_hubs/2fd5e64e-6cab-4257-bd4e-f0e85b523082/public/work_request/new"
# Jobber work-request form embedded inline on the contact page
JOBBER_EMBED = """<div id="2fd5e64e-6cab-4257-bd4e-f0e85b523082-2323534"></div>
<link rel="stylesheet" href="https://d3ey4dbjkt2f6s.cloudfront.net/assets/external/work_request_embed.css" media="screen" />
<script src="https://d3ey4dbjkt2f6s.cloudfront.net/assets/static_link/work_request_embed_snippet.js" clienthub_id="2fd5e64e-6cab-4257-bd4e-f0e85b523082-2323534" form_url="https://clienthub.getjobber.com/client_hubs/2fd5e64e-6cab-4257-bd4e-f0e85b523082/public/work_request/embedded_work_request_form?form_id=2323534"></script>"""
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
        "image": "https://dfchomeimprovement.com/assets/img/kitchen-thomas-jefferson.jpg",
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
<meta property="og:image" content="assets/img/kitchen-thomas-jefferson.jpg">
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
    <a class="btn header-cta" href="{JOBBER_FORM}" target="_blank" rel="noopener">Request Evaluation</a>
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

# ---------------------------------------------------------------- PAGE HEAD (text, no photo)
def page_head(crumb, title, desc):
    return f"""
<section class="page-head">
  <div class="wrap reveal">
    <p class="breadcrumb"><a href="index.html">Home</a> / {crumb}</p>
    <h1>{title}</h1>
    <p class="ph-desc">{desc}</p>
  </div>
</section>"""

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
      <span>© 2026 DFC Home Improvement. Class A Licensed &amp; Insured. · <a href="privacy.html">Privacy Policy</a> · <a href="terms.html">Terms of Service</a></span>
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
    <div class="hero-bg"><img src="{img('kitchen-thomas-jefferson')}" alt="Custom kitchen remodel by DFC Home Improvement" fetchpriority="high"></div>
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
        <img src="{img('outdoor-15th-street-deck')}" alt="New custom home construction by DFC Home Improvement" loading="lazy">
        <div class="p-body">
          <div class="p-num">01 — Build new</div>
          <h3>New Construction</h3>
          <p>Custom homes, additions, dormers, roofing and foundations — full-service construction from land to move-in.</p>
          <span class="link-arrow light">Explore new construction {ARROW}</span>
        </div>
      </a>
      <a class="pillar reveal d1" href="renovations.html">
        <img src="{img('kitchen-monteiro-ave')}" alt="Whole-home renovation by DFC Home Improvement" loading="lazy">
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
    <div class="f-img"><img src="{img('bath-marble-suite')}" alt="Spa-style marble bathroom by DFC Home Improvement" loading="lazy"></div>
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
{page_head("New Construction", "New construction, built right from the ground up.", "Custom homes, additions, dormers, foundations and roofing — full-service construction managed by one accountable, Class A licensed team.")}

  <!-- New Homes feature row -->
  <section class="section wrap" id="new-homes">
    <div class="svc-row">
      <div class="stmt reveal">
        <p class="eyebrow">Custom Homes</p>
        <h2>New homes designed around your life.</h2>
        <p style="margin-top:1.1em">From land evaluation through final move-in, we guide you through architecture, permitting, foundation, framing and finishes — treating each build as a personal reflection of how you want to live.</p>
        <ul>{''.join(f'<li>{b}</li>' for b in bullets_newhomes)}</ul>
      </div>
      <div class="media reveal d1"><img src="{img('kitchen-polecat-lane')}" alt="Custom kitchen by DFC Home Improvement" loading="lazy"></div>
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
        ("kitchen", "Kitchen Remodeling", "01", "kitchen-north-ave", False,
         "A unified team handles layout, cabinetry, countertops, tile and electrical — improving how your kitchen works as much as how it looks.",
         ["Full renovations &amp; reconfigurations", "Custom cabinetry &amp; islands", "Countertops, backsplash &amp; tile", "Flooring, trim, paint &amp; appliances"]),
        ("bathroom", "Bathroom Renovations", "02", "bath-monteiro-ave", True,
         "Demolition, waterproofing, tile, plumbing and finish carpentry coordinated as one accountable job — built for durability and a spa-grade feel.",
         ["Primary, guest &amp; powder baths", "Custom tile showers &amp; waterproofing", "Vanities, lighting &amp; fixtures", "Glass, flooring &amp; finish detail"]),
        ("full-home", "Whole-Home Renovations", "03", "kitchen-springvale-lane", False,
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
{page_head("Renovations", "Renovations that reimagine the home you're in.", "Kitchens, bathrooms and whole-home remodels — designed and built by one team, from first sketch to final walkthrough.")}
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
        <div class="media reveal"><img src="{img('3d-cook-1')}" alt="Photoreal 3D kitchen rendering by DFC Home Improvement" loading="lazy"></div>
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
    # landing: one tile per category -> opens that category's gallery page
    tiles = [
        ("Kitchens",               "portfolio-kitchens.html",  "kitchen-p1-01"),
        ("Bathrooms",              "portfolio-bathrooms.html", "bath-p10-01"),
        ("Whole-Home Renovations", "portfolio-wholehome.html", "wholehome-gallery-01"),
        ("3D Designs",             "portfolio-3d.html",        "3d-cook-1"),
    ]
    tile_html = "\n".join(
        f"""      <a class="cat-tile reveal" href="{href}">
        <img src="{img(slug)}" alt="{label} portfolio by DFC Home Improvement" loading="lazy">
        <div class="ct-cap"><h2>{label}</h2><span class="link-arrow light">View gallery {ARROW}</span></div>
      </a>""" for label, href, slug in tiles)
    body = f"""
<main id="top">
{page_head("Portfolio", "Our work, by space.", "Explore completed DFC projects across Northern Virginia, Washington DC and Richmond. Choose a category to see the full gallery.")}
  <section class="section--tight wrap">
    <div class="cat-tiles">
{tile_html}
    </div>
  </section>
{cta()}
</main>"""
    page("portfolio.html",
         head("Portfolio | DFC Home Improvement — Kitchens, Bathrooms & 3D Designs",
              "Browse completed DFC Home Improvement projects — kitchens, bathrooms and 3D design renderings across Northern Virginia, DC and Richmond.",
              "portfolio"),
         body, "portfolio")

def build_category(cat, fname, title, desc):
    items = [x for x in M.values() if x["category"] == cat]
    items.sort(key=lambda x: (not x["featured"], x["slug"]))
    figs = "\n".join(
        f"""        <figure data-full="{x['src']}" data-proj="{html.escape(x['project'])}" data-cat="{x['category']}">
          <img src="{x['thumb']}" alt="{html.escape(x['project'])} — {x['category']} by DFC Home Improvement" loading="lazy">
          <span class="g-zoom" aria-hidden="true">{ZOOM}</span>
        </figure>""" for x in items)
    crumb = f'<a href="portfolio.html">Portfolio</a> / {title}'
    body = f"""
<main id="top">
{page_head(crumb, title, desc)}
  <section class="section--tight wrap">
    <div class="gallery gallery--2col" id="gallery">
{figs}
    </div>
    <div class="cat-nav reveal"><a class="btn" href="portfolio.html">← Back to all categories</a></div>
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
    page(fname,
         head(f"{title} | DFC Home Improvement Portfolio", desc, "portfolio"),
         body, "portfolio")

# ====================================== PROJECT-GROUPED CATEGORY (editorial)
THREED_GROUPS = [
    {"title":"Sage Shaker Kitchen","slugs":["3d-cook-1","3d-cook-2","3d-cook-3"],
     "desc":"Sage-green shaker cabinetry paired with a warm wood island, quartz counters, brass pendants and a marble-look backsplash. The soft green and natural wood give the room a calm, grounded warmth — fresh yet timeless, it's a kitchen that invites you to slow down and gather."},
    {"title":"White Kitchen & Spa Baths","slugs":["3d-emily-1","3d-emily-2","3d-emily-3","3d-emily-4","3d-emily-5"],
     "desc":"A crisp all-white kitchen with a generous island and designer lighting, carried through to spa-style bathrooms with floating vanities and full-height tile. Light and uncluttered, the spaces feel airy and quietly luxurious — a sense of calm at the start and end of every day."},
    {"title":"Two-Tone Island Kitchen","slugs":["3d-bradley-1","3d-bradley-2"],
     "desc":"White perimeter cabinetry grounded by a deep, contrasting island, waterfall quartz and statement pendants. The contrast reads confident and modern — bold but balanced, a kitchen with real presence that still feels welcoming."},
    {"title":"Custom Tile Bath Suite","slugs":["3d-brendan-1","3d-brendan-2","3d-brendan-3"],
     "desc":"Floor-to-ceiling tile, a frameless glass shower and a clean floating vanity. The effect is serene and spa-like — a calm, hotel-grade retreat that feels like a daily reset."},
    {"title":"Spa Bath Retreat","slugs":["3d-harry-1","3d-harry-2","3d-harry-3"],
     "desc":"A spa-inspired bath with a barn-door entry, large-format tile and a sculptural vanity wall. Moody and intimate, it feels grounded and restorative — quiet luxury you can truly unwind in."},
    {"title":"Kitchen & Bath Refresh","slugs":["3d-bridetta-1","3d-bridetta-2","3d-bridetta-3"],
     "desc":"A coordinated kitchen and bath in a light, transitional palette — white cabinetry, quartz surfaces and brushed fixtures. Bright and welcoming, the spaces feel fresh, easy and effortlessly put-together."},
    {"title":"Covered Patio & Pergola","slugs":["3d-covered-patio-1","3d-covered-patio-2","3d-covered-patio-3"],
     "desc":"A cedar-tone pergola, lounge seating and clean railings that extend the home into the backyard. It transmits ease and escape — a relaxed outdoor room made for slow mornings and evening gatherings."},
    {"title":"Wraparound Porch & Great Room","slugs":["3d-ginger-1","3d-ginger-2"],
     "desc":"An addition that opens the home up — a covered porch for outdoor living and a bright, connected great room inside. It transmits warmth and openness: a home that breathes and brings people together."},
]

KITCHEN_GROUPS = [
    {"title":"Geometric Backsplash Kitchen","slugs":["kitchen-p1-01","kitchen-p1-02","kitchen-p1-03","kitchen-p1-04"],
     "desc":"Crisp white shaker cabinetry meets a deep gray island and a bold black-and-white geometric backsplash, tied together with brass pendants and a sunny breakfast nook. It feels lively and current — a confident, social kitchen with just enough pattern to give it personality."},
    {"title":"Bright Galley Kitchen","slugs":["kitchen-p2-01","kitchen-p2-02","kitchen-p2-03"],
     "desc":"A compact, efficient layout in white and soft gray with subway tile and a full stainless suite. Bright and uncomplicated, it transmits a clean, easy calm — proof that a smaller footprint can still feel open and refined."},
    {"title":"Warm Wood Accent Kitchen","slugs":["kitchen-p3-01","kitchen-p3-02","kitchen-p3-03"],
     "desc":"White cabinetry warmed by a natural wood island and counter, with under-cabinet lighting and an open connection to the stair hall. The mix of crisp white and warm timber feels inviting and grounded — modern, but never cold."},
    {"title":"Coastal Navy Island","slugs":["kitchen-p4-01","kitchen-p4-02","kitchen-p4-03"],
     "desc":"White perimeter cabinetry anchored by a navy island, pale wood floors and airy pendants that open to the dining space. The palette feels fresh and coastal — relaxed, breezy and made for gathering."},
    {"title":"Classic White & Gray","slugs":["kitchen-p5-01","kitchen-p5-02","kitchen-p5-03"],
     "desc":"Our signature pairing — white shaker uppers, a gray island and quartz counters under elegant pendant lighting. Timeless and balanced, it feels bright and welcoming, the kind of kitchen that never goes out of style."},
    {"title":"Marble & Brass Kitchen","slugs":["kitchen-p6-01","kitchen-p6-02","kitchen-p6-03"],
     "desc":"White cabinetry elevated by marble counters and backsplash, a sculptural brass bridge faucet and warm hardwood floors. Polished and a touch glamorous, it transmits quiet luxury — refined without ever feeling fussy."},
    {"title":"White & Wood Island","slugs":["kitchen-p7-01","kitchen-p7-02","kitchen-p7-03"],
     "desc":"Bright white cabinetry paired with a warm wood island and waterfall quartz, finished with statement lighting. The contrast of cool white and natural wood feels modern and organic — clean lines with a soft, livable warmth."},
    {"title":"Transitional Family Kitchen","slugs":["kitchen-p8-01","kitchen-p8-02","kitchen-p8-03"],
     "desc":"White and gray cabinetry, quartz counters and a full stainless suite with double ovens. Practical and put-together, it feels like a true family kitchen — hardworking, bright and effortlessly classic."},
    {"title":"Open-Concept White Kitchen","slugs":["redfin-kitchen-01","redfin-kitchen-02","redfin-kitchen-03"],
     "desc":"A bright, open-plan white kitchen with a marble backsplash, central island and pendant lighting that flows into the living space. It feels expansive and welcoming — a true heart-of-the-home layout."},
    {"title":"Row-Home Chef's Kitchen","slugs":["redfin-kitchen-04","redfin-kitchen-05","redfin-kitchen-06"],
     "desc":"A crisp white kitchen built for cooking — a generous island, full stainless suite and clean lines that make the most of a city row-home footprint. Functional and refined, it feels calm and uncluttered."},
]

BATH_GROUPS = [
    {"title":"Bright Marble Spa Bath","slugs":["bath-p10-01","bath-p10-02","bath-p10-03"],
     "desc":"A light-filled primary bath wrapped in marble, with a glass walk-in shower, a freestanding soaking tub and a crisp white double vanity beneath big windows. Warm brass and matte black mix for contrast — it feels open, fresh and restorative, a personal spa flooded with daylight."},
    {"title":"Moody Black & Marble Bath","slugs":["bath-p11-01","bath-p11-02"],
     "desc":"A dramatic bath that plays a charcoal accent wall against bright marble and matte-black fixtures. The contrast feels bold and intimate — confident and a little luxe, a space with real depth and character."},
    {"title":"Sculptural Soaking Tub","slugs":["bath-p12-01"],
     "desc":"Floor-to-ceiling marble frames a sculptural freestanding tub, finished with matte-black fixtures and a clean built-in niche. Minimal and serene, it transmits pure calm — a quiet retreat built around the simple ritual of a long soak."},
    {"title":"Warm Marble & Brass Bath","slugs":["bath-p13-01","bath-p13-02"],
     "desc":"Marble and warm wood tones meet brushed brass, a round backlit mirror and a glass shower. The mix of cool stone and warm metal feels welcoming and grounded — polished, but easy to relax in."},
    {"title":"Arched-Mirror Glam Bath","slugs":["bath-p14-01","bath-p14-02","bath-p14-03","bath-p14-04","bath-p14-05","bath-p14-06"],
     "desc":"An elegant bath with arched mirrors, gold sconces, blush-veined marble and a frameless glass shower over a white double vanity. Refined and a touch glamorous, it feels bright, romantic and special — a true showpiece."},
]

def build_grouped(fname, title, desc, groups):
    secs = []
    for g in groups:
        figs = "\n".join(
            f"""          <figure data-full="{M[s]['src']}" data-proj="{html.escape(g['title'])}" data-cat="{html.escape(title)}">
            <img src="{M[s]['thumb']}" alt="{html.escape(g['title'])} — {html.escape(title)} by DFC Home Improvement" loading="lazy">
            <span class="g-zoom" aria-hidden="true">{ZOOM}</span>
          </figure>""" for s in g['slugs'])
        secs.append(f"""
  <section class="proj reveal">
    <div class="wrap">
      <div class="proj-head">
        <p class="eyebrow">{html.escape(title)}</p>
        <h2>{html.escape(g['title'])}</h2>
        <p class="proj-desc">{g['desc']}</p>
      </div>
      <div class="proj-grid">
{figs}
      </div>
    </div>
  </section>""")
    crumb = f'<a href="portfolio.html">Portfolio</a> / {title}'
    body = f"""
<main id="top">
{page_head(crumb, title, desc)}
  <div id="gallery">
{''.join(secs)}
  </div>
  <div class="section--tight wrap"><div class="cat-nav reveal"><a class="btn" href="portfolio.html">← Back to all categories</a></div></div>
{cta()}
</main>
<div class="lightbox" id="lightbox" aria-hidden="true" role="dialog" aria-label="Project image">
  <button class="lb-close" id="lbClose" aria-label="Close">✕</button>
  <button class="lb-nav lb-prev" id="lbPrev" aria-label="Previous">‹</button>
  <img id="lbImg" src="" alt="">
  <button class="lb-nav lb-next" id="lbNext" aria-label="Next">›</button>
  <div class="lb-cap" id="lbCap"></div>
</div>"""
    page(fname, head(f"{title} | DFC Home Improvement Portfolio", desc, "portfolio"), body, "portfolio")

# ================================================================ CONTACT
def build_contact():
    areas = " · ".join(AREAS)
    body = f"""
<main id="top">
{page_head("Contact", "Let's talk about your project.", "Tell us a little about what you have in mind. We'll follow up to schedule your free evaluation — no obligation, honest pricing, expert guidance.")}
  <section class="section--tight wrap">
    <div class="contact-grid">
      <div class="contact-info reveal">
        <div class="ci-block"><div class="ci-lab">Call or text</div><div class="ci-val"><a href="tel:{PHONE_TEL}">{PHONE_DISP}</a></div></div>
        <div class="ci-block"><div class="ci-lab">Email</div><div class="ci-val"><a href="mailto:{EMAIL}">{EMAIL}</a></div></div>
        <div class="ci-block"><div class="ci-lab">Service area</div><div class="ci-val small">{areas}</div></div>
        <div class="ci-block"><div class="ci-lab">Credentials</div><div class="ci-val small">Class A Licensed General Contractor · Licensed &amp; Insured · Design-Build</div></div>
        <div class="ci-block"><div class="ci-lab">Response time</div><div class="ci-val small">We follow up on new requests within 24 hours.</div></div>
      </div>
      <div class="form-card">
        <div class="fc-title">Request a free consultation</div>
        <p class="fc-sub">Book your on-site assessment online — pick a date, add photos, and it goes straight into our scheduling system.</p>
        <div class="jobber-embed">
          {JOBBER_EMBED}
        </div>
        <div class="or-divider"><span>or just send us a message</span></div>
        <p class="fc-sub">Fields marked <span style="color:var(--accent)">*</span> are required.</p>
        <form class="lead-form" id="leadForm" action="https://formsubmit.co/{EMAIL}" method="POST">
          <input type="hidden" name="_subject" value="New website lead — DFC Home Improvement">
          <input type="hidden" name="_template" value="table">
          <input type="hidden" name="_captcha" value="false">
          <input type="hidden" name="_autoresponse" value="Thanks for reaching out to DFC Home Improvement! We've received your request and someone from our team will personally follow up within 24 hours to schedule your free, no-obligation evaluation. In the meantime, here's a quick look at what we do: https://www.dfchomeimprovement.com/assets/dfc-brochure.pdf — If it's urgent, call or text us at {PHONE_DISP}. — The DFC Home Improvement Team">
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

# ================================================================ PRIVACY POLICY
def build_privacy():
    updated = "June 1, 2026"
    body = f"""
<main id="top">
{page_head("Privacy Policy", "Privacy Policy", "How DFC Home Improvement collects, uses and protects the information you share with us.")}
  <section class="section--tight wrap">
    <div class="legal reveal">
      <p class="legal-updated">Last updated: {updated}</p>

      <p>DFC Home Improvement ("DFC," "we," "us" or "our") is a Class A licensed design-build general contractor serving Northern Virginia, Washington DC and Richmond. This Privacy Policy explains what information we collect, how we use it, and the choices you have when you visit <a href="https://www.dfchomeimprovement.com">dfchomeimprovement.com</a>, contact us, or respond to our advertisements on platforms such as Facebook and Instagram.</p>

      <h2>Information we collect</h2>
      <p><strong>Information you provide.</strong> When you submit our consultation request form, respond to a Facebook or Instagram lead ad, call or text us, or email us, we collect the details you share — typically your name, phone number, email address, project address or service area, and a description of the work you're considering.</p>
      <p><strong>Information collected automatically.</strong> Like most websites, our site and its providers may automatically receive standard technical data such as your IP address, browser and device type, and the pages you view. Our pages load Google Fonts and an embedded map, which may receive your IP address as part of delivering those features.</p>
      <p><strong>Advertising data.</strong> If you engage with our ads on Meta platforms (Facebook, Instagram) or Google, those platforms and any advertising tools we use (such as the Meta Pixel or conversion tracking) may collect information about your interaction with the ad and our site, and share lead or aggregated information with us.</p>

      <h2>How we use your information</h2>
      <ul>
        <li>Respond to your inquiry and schedule a consultation or estimate</li>
        <li>Prepare quotes and provide the construction, renovation and design services you request</li>
        <li>Communicate with you about your project, including follow-up by phone, text or email</li>
        <li>Operate, maintain and improve our website and services</li>
        <li>Measure and improve the performance of our advertising</li>
        <li>Comply with legal obligations and protect our rights</li>
      </ul>

      <h2>How we share information</h2>
      <p>We do <strong>not</strong> sell your personal information. We share it only as needed to run our business:</p>
      <ul>
        <li><strong>Service providers</strong> that help us operate — for example our CRM and quoting system (Jobber), our web-form and email delivery provider (FormSubmit), our website host (Railway), and our email provider (Google Workspace).</li>
        <li><strong>Advertising platforms</strong> (Meta, Google) when you reach us through their lead or advertising tools.</li>
        <li><strong>Legal and safety reasons</strong> — when required by law or to protect our rights, our customers or the public.</li>
      </ul>

      <h2>Third-party services</h2>
      <p>Some tools and features we use are operated by third parties with their own privacy policies:</p>
      <ul>
        <li>Meta (Facebook / Instagram) — <a href="https://www.facebook.com/privacy/policy/" target="_blank" rel="noopener">facebook.com/privacy/policy</a></li>
        <li>Google — <a href="https://policies.google.com/privacy" target="_blank" rel="noopener">policies.google.com/privacy</a></li>
        <li>Jobber — <a href="https://getjobber.com/privacy-policy/" target="_blank" rel="noopener">getjobber.com/privacy-policy</a></li>
        <li>FormSubmit — <a href="https://formsubmit.co/" target="_blank" rel="noopener">formsubmit.co</a></li>
      </ul>

      <h2>Cookies &amp; tracking technologies</h2>
      <p>We and our advertising partners may use cookies, pixels and similar technologies to operate the site and to understand and improve ad performance. You can control cookies through your browser settings, and manage ad personalization through <a href="https://www.facebook.com/adpreferences" target="_blank" rel="noopener">Meta's ad preferences</a>, <a href="https://adssettings.google.com" target="_blank" rel="noopener">Google's ad settings</a>, and the industry opt-out tools at <a href="https://optout.aboutads.info" target="_blank" rel="noopener">optout.aboutads.info</a>.</p>

      <h2>Data retention</h2>
      <p>We keep your information for as long as needed to respond to your request, provide our services, and meet legal, tax and recordkeeping requirements. You may ask us to delete information we are not required to retain.</p>

      <h2>Your choices &amp; rights</h2>
      <p>You can opt out of marketing messages at any time by asking us to stop contacting you or replying "STOP" to a text. Depending on where you live — including Virginia residents under the Virginia Consumer Data Protection Act — you may have the right to access, correct or delete your personal information, or to opt out of certain processing. To make a request, contact us using the details below and we will respond as required by applicable law.</p>

      <h2>Data security</h2>
      <p>We take reasonable measures to protect your information. However, no method of transmission over the internet or electronic storage is completely secure, and we cannot guarantee absolute security.</p>

      <h2>Children's privacy</h2>
      <p>Our website and services are intended for adults. We do not knowingly collect personal information from children under 13.</p>

      <h2>Links to other sites</h2>
      <p>Our site may link to third-party websites. We are not responsible for the privacy practices of those sites and encourage you to review their policies.</p>

      <h2>Changes to this policy</h2>
      <p>We may update this Privacy Policy from time to time. When we do, we'll revise the "Last updated" date above, and material changes will be posted on this page.</p>

      <h2>Contact us</h2>
      <p>If you have questions about this Privacy Policy or your information, contact:</p>
      <p><strong>DFC Home Improvement</strong><br>
      Phone / Text: <a href="tel:+17035968375">(703) 596-8375</a><br>
      Email: <a href="mailto:admin@dfchomeimprovement.com">admin@dfchomeimprovement.com</a><br>
      Service area: Northern Virginia · Washington DC · Richmond</p>
    </div>
  </section>
{cta()}
</main>"""
    page("privacy.html",
         head("Privacy Policy | DFC Home Improvement",
              "How DFC Home Improvement collects, uses and protects your information across our website and our Facebook and Instagram advertising.",
              "privacy"),
         body, "privacy")

# ================================================================ TERMS OF SERVICE
def build_terms():
    updated = "June 1, 2026"
    body = f"""
<main id="top">
{page_head("Terms of Service", "Terms of Service", "The terms that govern your use of our website and our estimates, quotes and communications.")}
  <section class="section--tight wrap">
    <div class="legal reveal">
      <p class="legal-updated">Last updated: {updated}</p>

      <p>These Terms of Service ("Terms") govern your access to and use of the website at <a href="https://www.dfchomeimprovement.com">dfchomeimprovement.com</a> (the "Site") and your interactions with DFC Home Improvement ("DFC," "we," "us" or "our"), a Class A licensed design-build general contractor serving Northern Virginia, Washington DC and Richmond. By using the Site, requesting an estimate, or communicating with us, you agree to these Terms. If you do not agree, please do not use the Site.</p>

      <h2>Use of our website</h2>
      <p>You may use the Site for lawful, personal and non-commercial purposes — to learn about our services, view our work, and request a consultation. You agree not to misuse the Site, attempt to gain unauthorized access to it, disrupt its operation, or use it to violate any applicable law. The Site, its content, layout, logos and photography are owned by DFC or our licensors and are protected by intellectual-property laws; you may not copy, reproduce or republish them without our written permission.</p>

      <h2>Estimates, proposals and quotes</h2>
      <p>Information on the Site — including service descriptions, project galleries and any pricing references — is provided for general information only and does not constitute an offer, a quote, or a binding contract. Any budget figure or "starting at" range we mention is an estimate, not a fixed price.</p>
      <p>A binding agreement is created only when DFC issues a written quote or proposal for your specific project and that document is accepted and signed by you. Quotes are valid for the period stated on them (and otherwise for 30 days) and may be revised if the scope, site conditions, selections, or material costs change. The signed quote or contract, together with any written change orders, governs the work — and in the event of any conflict with these Terms, that signed document controls.</p>

      <h2>Scheduling and site access</h2>
      <p>Consultations, evaluations and project schedules are arranged by appointment and may be affected by weather, permitting, inspections, material availability, and circumstances beyond our control. You agree to provide safe and reasonable access to the project site so we can perform the agreed work.</p>

      <h2>Communications and text-message consent</h2>
      <p>When you give us your phone number — for example by submitting our consultation form, responding to one of our ads, or contacting us — you agree that we may contact you by phone call, text message (SMS) and email about your inquiry, your project, scheduling, and quotes. Message and data rates may apply, and message frequency varies. You can opt out of text messages at any time by replying <strong>STOP</strong>, or ask us to stop contacting you, and we will honor your request. How we handle the information you share is described in our <a href="privacy.html">Privacy Policy</a>.</p>

      <h2>Third-party links and platforms</h2>
      <p>The Site and our advertising may link to or operate through third-party platforms — such as Jobber, Google, Facebook and Instagram — each with its own terms and privacy policies. We are not responsible for the content, products or practices of those third parties, and your use of their services is governed by their terms.</p>

      <h2>Disclaimers</h2>
      <p>The Site and its content are provided "as is" and "as available" without warranties of any kind, whether express or implied, including any implied warranties of merchantability, fitness for a particular purpose, or non-infringement. We do not warrant that the Site will be uninterrupted, error-free, or free of harmful components. This section concerns your use of the Site; the warranties for any construction work we perform are set out in your signed contract.</p>

      <h2>Limitation of liability</h2>
      <p>To the fullest extent permitted by law, DFC and its owners, employees and contractors will not be liable for any indirect, incidental, special, consequential or punitive damages, or any loss of data, arising out of or relating to your use of the Site. Nothing in these Terms limits any liability that cannot be limited under applicable law.</p>

      <h2>Indemnification</h2>
      <p>You agree to indemnify and hold harmless DFC from any claims, damages or expenses arising out of your misuse of the Site or your violation of these Terms or any applicable law.</p>

      <h2>Governing law</h2>
      <p>These Terms are governed by the laws of the Commonwealth of Virginia, without regard to its conflict-of-laws rules. Any dispute relating to the Site or these Terms will be subject to the exclusive jurisdiction of the state and federal courts located in Virginia.</p>

      <h2>Changes to these Terms</h2>
      <p>We may update these Terms from time to time. When we do, we'll revise the "Last updated" date above, and the updated Terms take effect when posted on this page. Your continued use of the Site after changes are posted means you accept the revised Terms.</p>

      <h2>Contact us</h2>
      <p>If you have questions about these Terms, contact:</p>
      <p><strong>DFC Home Improvement</strong><br>
      Phone / Text: <a href="tel:{PHONE_TEL}">{PHONE_DISP}</a><br>
      Email: <a href="mailto:{EMAIL}">{EMAIL}</a><br>
      Service area: Northern Virginia · Washington DC · Richmond</p>
    </div>
  </section>
{cta()}
</main>"""
    page("terms.html",
         head("Terms of Service | DFC Home Improvement",
              "The terms that govern your use of the DFC Home Improvement website, our estimates and quotes, and how we communicate with you.",
              "terms"),
         body, "terms")

if __name__ == "__main__":
    build_index()
    build_new_construction()
    build_renovations()
    build_portfolio()
    build_grouped("portfolio-kitchens.html", "Kitchens",
                  "Custom kitchen remodels and new builds across Northern Virginia, Washington DC and Richmond — grouped by style.",
                  KITCHEN_GROUPS)
    build_grouped("portfolio-bathrooms.html", "Bathrooms",
                  "Spa-style baths, custom tile showers and finish work — explored project by project.",
                  BATH_GROUPS)
    build_grouped("portfolio-3d.html", "3D Designs",
                  "Photoreal 3D renderings we create so you can see your project before we build it — explored project by project.",
                  THREED_GROUPS)
    build_category("Whole-Home Renovations", "portfolio-wholehome.html", "Whole-Home Renovations",
                   "Full-home transformations — living spaces, additions and finishes carried out end to end.")
    build_contact()
    build_privacy()
    build_terms()
    # remove the old services page if present
    old = os.path.join(ROOT, "services.html")
    if os.path.exists(old): os.remove(old); print("removed services.html")
    print("done.")
