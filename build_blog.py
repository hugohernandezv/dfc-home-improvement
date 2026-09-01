#!/usr/bin/env python3
"""Generate the DFC blog (/blog/) — Home Notes articles.

Standalone article pages in the same style as the cost guide, plus a blog
index. Content mirrors the Home Notes email series so email + blog stay one
source of truth. Root-absolute asset/link paths (works with and without
trailing slashes under Caddy's try_files).
"""
import html, json, os

ROOT = "/Users/hugohernandez/Documentos/DFC/website/dfc-site"
SITE = "https://www.dfchomeimprovement.com"
PHONE_DISP = "(703) 596-8375"
PHONE_TEL = "+17035968375"
EMAIL = "admin@dfchomeimprovement.com"

GTAG = """<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-QRMHK61G1N"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-QRMHK61G1N');
</script>"""

META_PIXEL = """<!-- Meta Pixel Code -->
<script>
!function(f,b,e,v,n,t,s)
{if(f.fbq)return;n=f.fbq=function(){n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)};
if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];
s.parentNode.insertBefore(t,s)}(window, document,'script',
'https://connect.facebook.net/en_US/fbevents.js');
fbq('init', '1029300153267702');
fbq('track', 'PageView');
</script>
<noscript><img height="1" width="1" style="display:none"
src="https://www.facebook.com/tr?id=1029300153267702&ev=PageView&noscript=1"/></noscript>
<!-- End Meta Pixel Code -->"""

ARTICLE_CSS = """<style>
.article-body { max-width: 780px; margin: 0 auto; padding: 0 1.5rem; }
.article-body h2 { font-size: 1.45rem; margin: 2.4rem 0 .9rem; }
.article-body h3 { font-size: 1.1rem; margin: 1.8rem 0 .6rem; }
.article-body p { line-height: 1.75; margin-bottom: 1.1rem; }
.article-body ul, .article-body ol { margin: .8rem 0 1.2rem 1.4rem; }
.article-body ul li, .article-body ol li { margin-bottom: .5rem; line-height: 1.65; }
.article-hero { width: 100%; max-width: 780px; margin: 0 auto 2rem; padding: 0 1.5rem; }
.article-hero img { width: 100%; height: auto; border-radius: 10px; display: block; }
.article-meta { font-size: .88rem; color: rgba(13,8,5,.55); margin-bottom: 2rem; }
.callout { background: #f4f0ea; border-left: 3px solid #313d2c; padding: 1.2rem 1.4rem; margin: 1.5rem 0; border-radius: 0 4px 4px 0; }
.callout p { margin: 0; }
.stat-row { display: flex; gap: 1rem; margin: 1.5rem 0 2rem; flex-wrap: wrap; }
.stat-box { flex: 1 1 160px; background: #313d2c; border-radius: 10px; padding: 1.2rem 1rem; text-align: center; }
.stat-box .n { font-family: 'Urbanist', sans-serif; font-size: 1.7rem; font-weight: 700; color: #c08a2d; }
.stat-box .l { font-size: .8rem; color: rgba(255,255,255,.75); margin-top: .3rem; line-height: 1.4; }
.author-box { display: flex; flex-direction: column; align-items: center; text-align: center; gap: .35rem; border-top: 1px solid rgba(13,8,5,.12); margin-top: 2.6rem; padding-top: 2rem; }
.author-box img { width: 96px; height: 96px; border-radius: 50%; object-fit: cover; margin-bottom: .4rem; }
.author-box .a-name { font-family: 'Urbanist', sans-serif; font-weight: 700; color: #0d0805; }
.author-box .a-role { font-size: .88rem; color: #7c573a; }
.article-sources { font-size: .85rem; color: rgba(13,8,5,.55); margin-top: 1.6rem; }
.article-sources a { color: #7c573a; }
.blog-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 1.6rem; margin-top: 2.2rem; }
.blog-card { background: #fff; border-radius: 12px; overflow: hidden; text-decoration: none; color: inherit; box-shadow: 0 1px 3px rgba(13,8,5,.08); display: flex; flex-direction: column; transition: transform .18s ease, box-shadow .18s ease; }
.blog-card:hover { transform: translateY(-3px); box-shadow: 0 8px 22px rgba(13,8,5,.12); }
.blog-card img { width: 100%; aspect-ratio: 16/10; object-fit: cover; display: block; }
.blog-card .bc-body { padding: 1.2rem 1.3rem 1.4rem; display: flex; flex-direction: column; gap: .45rem; flex: 1; }
.blog-card .bc-tag { font-size: .72rem; letter-spacing: .12em; text-transform: uppercase; color: #c08a2d; font-weight: 700; }
.blog-card h3 { font-size: 1.08rem; line-height: 1.35; margin: 0; }
.blog-card p { font-size: .9rem; line-height: 1.55; color: rgba(13,8,5,.65); margin: 0; }
.blog-card .bc-date { font-size: .8rem; color: rgba(13,8,5,.45); margin-top: auto; padding-top: .5rem; }
</style>"""


def head_block(title, desc, canonical_path, og_image, jsonld=None):
    ld = ""
    if jsonld:
        ld = '<script type="application/ld+json">\n%s\n</script>\n' % json.dumps(jsonld, indent=2)
    return f"""<!doctype html>
<html lang="en">
<head>
{GTAG}
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script>document.documentElement.classList.add('js');</script>
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:type" content="article">
<meta property="og:image" content="{SITE}{og_image}">
<meta name="theme-color" content="#313d2c">
<link rel="canonical" href="{SITE}{canonical_path}">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/logo/favicon-32.png">
<link rel="icon" type="image/png" sizes="64x64" href="/assets/logo/favicon-64.png">
<link rel="apple-touch-icon" href="/assets/logo/favicon-180.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Urbanist:wght@400;500;600;700&family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/styles.css">
{ld}{ARTICLE_CSS}
{META_PIXEL}
</head>
<body data-page="article">"""


HEADER = f"""<header class="site-header" id="siteHeader">
  <a class="brand" href="/index.html" aria-label="DFC Home Improvement — home">
    <img class="mark-white" src="/assets/logo/dfc-mark-white.png" alt="DFC Home Improvement">
    <img class="mark-black" src="/assets/logo/dfc-mark-black.png" alt="" aria-hidden="true">
  </a>
  <nav class="nav" aria-label="Primary">
    <a href="/new-construction.html">New Construction</a>
    <a href="/renovations.html">Renovations</a>
    <a href="/portfolio.html">Portfolio</a>
    <a href="/blog/" class="current">Blog</a>
    <a href="/contact.html">Contact</a>
  </nav>
  <div class="header-right">
    <a class="header-phone" href="tel:{PHONE_TEL}">{PHONE_DISP}</a>
    <a class="btn header-cta" href="/contact.html">Request Evaluation</a>
    <a class="header-portal" href="/employee/" rel="nofollow" title="Employee portal" aria-label="Open employee portal">Employee</a>
    <button class="nav-toggle" id="navToggle" aria-label="Open menu" aria-expanded="false" aria-controls="mobileMenu">
      <span></span><span></span><span></span>
    </button>
  </div>
</header>
<div class="mobile-menu" id="mobileMenu" aria-hidden="true">
  <nav class="m-links" aria-label="Mobile">
    <a href="/index.html">Home</a>
    <a href="/new-construction.html">New Construction</a>
    <a href="/renovations.html">Renovations</a>
    <a href="/portfolio.html">Portfolio</a>
    <a href="/blog/">Blog</a>
    <a href="/contact.html">Contact</a>
  </nav>
  <div class="m-foot">
    <a href="/employee/" rel="nofollow">Employee Portal</a>
    <a href="tel:{PHONE_TEL}">{PHONE_DISP}</a>
    <a href="mailto:{EMAIL}">{EMAIL}</a>
  </div>
</div>"""

AUTHOR_BOX = """<div class="author-box">
      <img src="/assets/img/brian-owner.jpg" alt="Brian Stone, Owner of DFC Home Improvement">
      <div>
        <div class="a-name">Brian Stone</div>
        <div class="a-role">Owner, DFC Home Improvement · Class A Licensed &amp; Insured</div>
      </div>
    </div>"""

CTA_BAND = f"""<section class="section cta-band">
  <div class="wrap reveal">
    <p class="eyebrow">Have something in mind?</p>
    <h2>Let's build something worth coming home to.</h2>
    <div class="cta-actions">
      <a class="btn btn--light" href="/contact.html">Request a free consultation</a>
      <a class="link-arrow light" href="tel:{PHONE_TEL}">Call {PHONE_DISP} <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12h15M13 6l6 6-6 6"/></svg></a>
    </div>
  </div>
</section>"""

FOOTER = f"""<footer class="site-footer">
  <div class="wrap">
    <div class="footer-top">
      <div class="footer-brand">
        <img src="/assets/logo/dfc-logo-white.png" alt="DFC Home Improvement">
        <p>Class A licensed design-build general contractor. One accountable team from first concept to final walkthrough.</p>
        <a class="footer-bbb" href="https://www.bbb.org/us/va/fairfax/profile/residential-general-contractor/dfc-home-improvement-0241-236106972/#sealclick" target="_blank" rel="nofollow noopener"><img src="https://seal-dc-easternpa.bbb.org/seals/blue-seal-280-80-bbb-236106972.png" style="border: 0; margin-top: 18px; max-width: 220px; height: auto;" alt="DFC Home Improvement BBB Business Review" /></a>
      </div>
      <div class="footer-col">
        <h4>Explore</h4>
        <a href="/index.html">Home</a>
        <a href="/renovations.html">Renovations</a>
        <a href="/portfolio.html">Portfolio</a>
        <a href="/blog/">Blog</a>
        <a href="/contact.html">Contact</a>
      </div>
      <div class="footer-col">
        <h4>Services</h4>
        <a href="/kitchen-remodeling-northern-virginia.html">Kitchen Remodeling</a>
        <a href="/bathroom-remodeling-northern-virginia.html">Bathroom Remodeling</a>
        <a href="/home-additions-northern-virginia.html">Home Additions</a>
        <a href="/basement-finishing-northern-virginia.html">Basement Finishing</a>
        <a href="/deck-builder-northern-virginia.html">Deck Building</a>
      </div>
      <div class="footer-col footer-contact">
        <h4>Get in touch</h4>
        <a class="big" href="tel:{PHONE_TEL}">{PHONE_DISP}</a>
        <a href="mailto:{EMAIL}">{EMAIL}</a>
        <p>3060 Williams Drive Suite 300,<br>Fairfax, VA 22031</p>
        <p>Serving Northern Virginia, Richmond<br>&amp; Washington DC.</p>
        <iframe class="footer-map" title="DFC Home Improvement on Google Maps" loading="lazy" src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d397841.8167024655!2d-77.21790544999999!3d38.82927295!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x846a25461367bc67%3A0x736db6227d20323!2sDFC%20Home%20Improvement!5e0!3m2!1sen!2s!4v1787672110932!5m2!1sen!2s" allowfullscreen referrerpolicy="strict-origin-when-cross-origin"></iframe>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; 2026 DFC Home Improvement. Class A Licensed &amp; Insured. &middot; <a href="/privacy.html">Privacy Policy</a> &middot; <a href="/terms.html">Terms of Service</a></span>
    </div>
  </div>
</footer>
<script src="/assets/js/script.js" defer></script>
</body>
</html>"""


# ---------------------------------------------------------------- ARTICLES
ARTICLES = [
    {
        "slug": "kitchen-remodel-cost-northern-virginia",
        "tag": "Cost Guide",
        "title": "How Much Does a Kitchen Remodel Cost in Northern Virginia? (2026)",
        "card_title": "How much does a kitchen remodel cost in Northern Virginia?",
        "desc": "Real 2026 kitchen remodel prices in Fairfax, Vienna, McLean, Arlington and Alexandria: four price tiers, what sits inside each one, and the three decisions that move the total. From a Class A licensed design-build contractor.",
        "card_desc": "Real 2026 numbers from a contractor who builds them: four price tiers and what moves the total.",
        "hero": "/assets/img/kitchen-polecat-warm.jpg",
        "hero_alt": "Renovated kitchen with white cabinetry, range hood and warm wood floors in Northern Virginia",
        "date": "2026-08-05",
        "date_disp": "August 2026",
        "body": """
    <p>"What's this going to cost me?" is the first question every homeowner asks, and the one most contractors dodge until they are standing in your kitchen. So here are the real numbers we see building kitchens in Fairfax, Vienna, McLean, Arlington and Alexandria in 2026, along with what actually sits inside each tier.</p>

    <h2>$18,000 to $35,000 &middot; Cosmetic refresh</h2>
    <p>Cabinet reface or repaint, new countertops, backsplash, lighting and hardware. The layout stays exactly where it is, so there is no plumbing or electrical rerouting and no permit drama. This is the tier for a kitchen that functions fine but looks tired, and it is the fastest way to a dramatic visual change.</p>

    <h2>$55,000 to $90,000 &middot; Mid-range gut</h2>
    <p>Everything comes out. Semi-custom cabinets, quartz countertops, tile backsplash, new flooring, updated lighting and appliances, and usually some electrical work to bring the room up to current code. Minor layout changes live here too: moving a sink a few feet, widening a doorway, adding an island where the plumbing allows it.</p>

    <h2>$90,000 to $140,000 &middot; Full renovation with layout changes</h2>
    <p>This is where walls come down. Opening the kitchen to the living or dining room, relocating plumbing and gas lines, custom cabinetry, upgraded appliance packages and structural work with an engineer's stamp when a wall is load bearing. Most of the "before and after" transformations people picture live in this tier.</p>

    <h2>$140,000 and up &middot; High-end and additions</h2>
    <p>Full custom cabinetry, premium stone, professional appliance suites, and often an addition or bump-out that grows the footprint. At this level the kitchen is usually part of a larger whole-home project.</p>

    <h2>The three decisions that move your number the most</h2>
    <p><strong>Cabinets.</strong> They are typically 30 to 40 percent of a kitchen budget. The jump from stock to semi-custom is meaningful; the jump from semi-custom to full custom is where budgets get away from people. If you need to save, this is the most powerful lever you have.</p>
    <p><strong>Whether the layout moves.</strong> Keeping sink, stove and refrigerator where they are avoids rerouting plumbing, gas and electrical, and that alone can be the difference between two tiers. Moving them buys you the kitchen you actually want, which is often worth it, but it should be a decision you make on purpose rather than one that surprises you.</p>
    <p><strong>What is hiding behind the walls.</strong> In homes built before 1990 we regularly find outdated wiring, undersized panels or plumbing that has to be brought to code once it is exposed. A good contractor tells you this is possible before you sign, not after demolition.</p>

    <h2>How to compare quotes without getting burned</h2>
    <p>The cheapest quote is almost never the cheapest project. When you compare, look at what each proposal actually includes: are appliances in there, or excluded? Is the countertop a specific material and thickness, or a placeholder allowance that gets "adjusted" later? Are permits included? Is there a line for the unexpected, or will every surprise become a change order?</p>
    <p>On our projects, every material and every dollar is in writing before work begins, and you see a photoreal 3D design of your finished kitchen before we touch anything. That way the number you approve is the number you pay, and the kitchen you imagined is the kitchen that gets built.</p>

    <p>If you want a real number for your kitchen, not a range, we are happy to put one together. No obligation, and the 3D design is free.</p>
"""
    },
    {
        "slug": "end-of-summer-home-checklist",
        "tag": "Maintenance",
        "title": "Your End-of-Summer Home Checklist: 7 Quick Checks That Prevent Expensive Repairs",
        "card_title": "Your end-of-summer home checklist",
        "desc": "Seven 20-minute checks (A/C, deck, caulk, gutters, water heater, trim and roof) that catch problems while they're still cheap. From a Class A licensed NoVA contractor.",
        "card_desc": "Seven 20-minute checks that catch problems while they're still cheap to fix.",
        "hero": "/assets/img/patio-pergola-summer.jpg",
        "hero_alt": "Backyard pergola patio in summer",
        "date": "2026-07-03",
        "date_disp": "July 2026",
        "body": """
    <p>Most of the expensive repairs we get called for started as something small a season earlier: a hairline of failed caulk, a clogged downspout, a filter nobody changed. Here are seven quick checks, most of them 20 minutes or less, that catch problems while they're still cheap to fix.</p>

    <h2>1. Give your A/C room to breathe</h2>
    <p>Swap the filter, rinse the outdoor unit gently with a garden hose, and keep at least two feet of clearance around it, with no shrubs and no stacked patio furniture. Late summer is when overworked systems fail, and they usually pick the hottest weekend of the year to do it. If your system is 15+ years old, it's worth having it looked at before it becomes an emergency replacement.</p>

    <h2>2. Do the deck water test</h2>
    <p>Sprinkle water on a few boards. If it beads up, your sealer is still working. If it soaks straight in, the wood is drinking every storm. Time to clean and re-seal. While you're out there, check for popped nails, soft spots and wobbly railings. A loose railing is a safety issue, not a cosmetic one.</p>

    <h2>3. Check the caulk where tub meets tile</h2>
    <p>Dark, cracked or peeling caulk lets water get behind the wall, where it rots framing quietly for years before anything shows. An $8 tube of caulk today can prevent a four-figure repair later. If the grout around it is crumbling too, that's the wall telling you water is already finding a way in.</p>

    <h2>4. Clear gutters before the fall rain</h2>
    <p>Clogged gutters dump water right at your foundation, the number one cause of the wet-basement calls we get. Make sure downspouts push water at least four feet away from the house. It's the cheapest basement waterproofing there is.</p>

    <h2>5. Flush the water heater</h2>
    <p>Sediment builds up at the bottom of the tank and makes the heater work harder for less hot water. Draining a few gallons through the valve once a year extends its life, and it's a 20-minute job with a garden hose and a floor drain.</p>

    <h2>6. Poke the exterior trim</h2>
    <p>Press a screwdriver into window sills and door frames. Paint can look fine while the wood underneath has gone soft. Caught early, it's a trim repair; caught late, it's the whole frame, and sometimes what's behind it.</p>

    <h2>7. Look up after the next big storm</h2>
    <p>Scan your ceilings for new stains and take a quick sniff in the attic: a musty smell means moisture is getting in somewhere. Roof leaks show up inside long after they start outside, so the earlier you catch the signal, the smaller the fix.</p>

    <div class="callout">
      <p><strong>Found something that's more than a Saturday fix?</strong> Send us a photo and we'll tell you straight whether it's a quick repair or something bigger. From handyman fixes to full remodels, one licensed team. Call <a href="tel:+17035968375">(703) 596-8375</a> or <a href="/contact.html">get in touch</a>.</p>
    </div>
""",
    },
    {
        "slug": "5-remodeling-mistakes-homeowners-make",
        "tag": "Hiring a Contractor",
        "title": "5 Remodeling Mistakes That Cost Homeowners Thousands (and How to Avoid Them)",
        "card_title": "5 remodeling mistakes that cost homeowners thousands",
        "desc": "The lowest bid, the missing permit, the design you never saw: the five mistakes NoVA homeowners make when hiring a remodeler, and the 2-minute checks that avoid them.",
        "card_desc": "The lowest bid, the missing permit, the design you never saw, and how to avoid all five.",
        "hero": "/assets/img/wholehome-gallery-03.jpg",
        "hero_alt": "Finished living room renovation by DFC Home Improvement",
        "date": "2026-07-03",
        "date_disp": "July 2026",
        "body": """
    <p>A good chunk of our work is fixing projects that went sideways with someone else. The same five mistakes come up again and again. Here's how to avoid them, whoever you hire.</p>

    <h2>1. Taking the bid that's way below the others</h2>
    <p>If three bids land near each other and one is dramatically lower, that bid isn't a deal. It's missing scope. It comes back later as change orders, and by then you can't switch contractors without paying twice. The gap between a licensed contractor and the cheapest bid can run $20,000 to $40,000 on a mid-range kitchen. Compare what's <em>included</em>, not just the bottom line.</p>

    <h2>2. Letting anyone skip the permit</h2>
    <p>"We can save you money by skipping the permit" is a red flag, not a favor. In Fairfax, Arlington and Alexandria, moving plumbing, electrical or walls requires one, and unpermitted work surfaces at resale, when it's most expensive to fix. The permit also buys you a county inspector checking the work; that's protection you already paid taxes for.</p>

    <h2>3. Approving a design they've never actually seen</h2>
    <p>A quote and a handshake is not a plan. Insist on seeing the space (layout, finishes, colors) before demolition day. Changes on a screen are free; changes mid-build are not. It's why every DFC project starts with a true-to-life 3D walkthrough before we pick up a tool.</p>

    <h2>4. Paying too much before work happens</h2>
    <p>A reasonable deposit is normal. Half the project in cash up front is not. Payments should be tied to completed milestones in writing (demo done, rough-in passed inspection, cabinets installed) so the money always follows the work, never the promises.</p>

    <h2>5. Skipping the 2-minute license check</h2>
    <p>Virginia lets you verify any contractor's license free at <a href="https://www.dpor.virginia.gov" target="_blank" rel="noopener">dpor.virginia.gov</a>. Look for a Class A license, the state's highest classification, and ask for a certificate of insurance sent directly from the insurer, not a photocopy. Two minutes of checking beats two years of litigation.</p>

    <div class="callout">
      <p><strong>Planning a project this year?</strong> Keep this list handy when you're comparing bids, including ours. DFC is Class A licensed and insured, every project is permitted, designed in 3D before we build, and billed by milestone. <a href="/estimate.html">Get a free estimate</a> or call <a href="tel:+17035968375">(703) 596-8375</a>.</p>
    </div>
""",
    },
    {
        "slug": "nova-home-values-2026",
        "tag": "Market Watch",
        "title": "Your Home Is Worth More Again in 2026: Here's How Northern Virginia Homeowners Can Use That",
        "card_title": "Your home is worth more again: here's how to use that",
        "desc": "Fairfax County 2026 assessments rose ~4% on average and NoVA inventory stays tight. What rising values and ~6% rates mean for the move-vs-improve decision.",
        "card_desc": "Assessments up ~4%, rates near 6%. What that combination means for the move-vs-improve math.",
        "hero": "/assets/img/wholehome-gallery-01.jpg",
        "hero_alt": "Renovated living room by DFC Home Improvement",
        "date": "2026-07-03",
        "date_disp": "July 2026",
        "body": """
    <p>If you own a home in Northern Virginia, this year's numbers are worth two minutes of your time. Fairfax County's 2026 real estate assessments came in up about 4% on average for residential properties, putting the average improved home near $830,000. The Northern Virginia Association of Realtors, in its forecast with George Mason University's Center for Regional Analysis, expects prices to keep rising modestly through 2026 while mortgage rates hover around 6% and inventory stays tight.</p>

    <div class="stat-row">
      <div class="stat-box"><div class="n">+3.99%</div><div class="l">avg. Fairfax residential assessment increase, 2026</div></div>
      <div class="stat-box"><div class="n">$760K</div><div class="l">median NoVA sold price this spring</div></div>
      <div class="stat-box"><div class="n">~6%</div><div class="l">mortgage rates expected through 2026</div></div>
    </div>

    <h2>Moving got more expensive than improving</h2>
    <p>Selling into a tight market is the easy part. It's the buying back in that hurts. Trade a pandemic-era mortgage rate for roughly 6% on the next house and your monthly payment can jump even if the next house is smaller. For a lot of NoVA families, the math now clearly favors making the house you have into the house you want.</p>

    <h2>Your equity quietly grew again</h2>
    <p>Years of rising assessments mean many homeowners are sitting on significant equity that can fund a kitchen, bath or addition, often at better terms than any other borrowing available to them. The house has already earned the renovation; the question is whether you cash that in by selling or by staying and living better.</p>

    <h2>Updated homes do best in exactly this market</h2>
    <p>With buyers still competing over limited inventory, the homes that appraise and sell strongest are the updated ones. Whether you sell in two years or stay twenty, work done right (permitted, designed, documented) protects the value this market keeps adding.</p>

    <div class="callout">
      <p><strong>Thinking about what your equity could build?</strong> Tell us what you're dreaming about and we'll give you a real number to plan around, and a 3D design so you can see it before deciding anything. <a href="/estimate.html">See your price range in 60 seconds</a> or call <a href="tel:+17035968375">(703) 596-8375</a>.</p>
    </div>

    <p class="article-sources">Sources: <a href="https://www.fairfaxcounty.gov/taxes/real-estate/press-release-notices-sent" target="_blank" rel="noopener">Fairfax County Department of Tax Administration, 2026 assessments</a> · <a href="https://www.nvar.com/news/2025-12-29/2026-economic-market-forecast/" target="_blank" rel="noopener">NVAR 2026 Regional Housing Market Forecast</a></p>
""",
    },
    {
        "slug": "nova-home-insurance-rising-2026",
        "tag": "Market Watch",
        "title": "Home Insurance Is Jumping 15 to 25% in Northern Virginia: 5 Upgrades That Push Back",
        "card_title": "Home insurance is jumping in NoVA: here's how to push back",
        "desc": "Virginia is seeing some of the steepest homeowners insurance increases in the country in 2026. Five home upgrades that can actually bring your premium down.",
        "card_desc": "Virginia premiums are among the fastest-rising in the country. Five upgrades that fight back.",
        "hero": "/assets/img/bath-marble-suite.jpg",
        "hero_alt": "Renovated bathroom by DFC Home Improvement",
        "date": "2026-07-03",
        "date_disp": "July 2026",
        "body": """
    <p>If your homeowners insurance renewal made you wince this year, you're not alone. Industry analyses put Virginia among the states with the steepest premium increases in the country for 2026, with homeowners in Fairfax, Arlington, Loudoun and Prince William counties reporting 15 to 25% year-over-year jumps, often without ever filing a claim.</p>
    <p>The drivers are mostly out of your hands: storm losses across the region, pricier building materials pushing up replacement-cost estimates, and rising reinsurance costs that carriers pass straight through to premiums. But what your specific house costs to insure is <em>not</em> out of your hands. Five things that actually move the number:</p>

    <h2>1. Ask your carrier which upgrades earn discounts before you renew</h2>
    <p>Every insurer keeps a list: roof age, water protection, updated systems, security. Ten minutes on the phone tells you exactly which improvements pay twice: once in your home, once on your premium.</p>

    <h2>2. The roof matters more than anything else</h2>
    <p>Roof age is one of the first things underwriters look at, and an aging roof can mean surcharges, or a non-renewal letter. If yours is approaching 20 years, replacing it on your schedule beats replacing it on the insurer's.</p>

    <h2>3. Stop water before it starts</h2>
    <p>Water damage is the most common home claim there is. Leak sensors under sinks and behind the washing machine, plus an automatic shutoff valve, cost a few hundred dollars. Many carriers discount for them, and they prevent the claim that would spike your rate for years.</p>

    <h2>4. Update the systems insurers worry about</h2>
    <p>Older electrical panels, aging water heaters and outdated plumbing are quiet premium-inflators in NoVA's older neighborhoods. Some panel brands and pipe types can even make a home hard to insure at all. If your home is 30+ years old and largely untouched, a systems check is worth scheduling.</p>

    <h2>5. Document your renovations: they work in your favor</h2>
    <p>Permitted, documented renovations update your home's replacement-cost profile accurately and give you leverage when you shop your policy, which in this market you should do every couple of years.</p>

    <div class="callout">
      <p><strong>Already planning one of these upgrades?</strong> We handle roofing-to-plumbing updates as one licensed team: permitted, inspected and documented, so the work counts with your insurer too. <a href="/contact.html">Get in touch</a> or call <a href="tel:+17035968375">(703) 596-8375</a>.</p>
    </div>

    <p class="article-sources">Insurance guidance is general information, not advice. Confirm available discounts with your carrier.</p>
""",
    },
    {
        "slug": "federal-energy-tax-credits-ended-2026",
        "tag": "Market Watch",
        "title": "The Federal Energy Tax Credits Ended December 31: What Still Pays Homeowners Back in 2026",
        "card_title": "The federal energy credits are gone: what still pays you back",
        "desc": "The 25C and 25D credits for insulation, windows, HVAC and solar ended Dec 31, 2025. What NoVA homeowners can still claim, and what still saves money in 2026.",
        "card_desc": "Insulation, window and HVAC credits ended Dec 31. What you can still claim, and what still saves.",
        "hero": "/assets/img/sunroom-monteiro-ave.jpg",
        "hero_alt": "Sunlit living room with large windows by DFC Home Improvement",
        "date": "2026-07-03",
        "date_disp": "July 2026",
        "body": """
    <p>Quick heads-up if energy upgrades were on your list: the federal tax credits for insulation, windows, doors, HVAC systems and solar (the Energy Efficient Home Improvement Credit, 25C, and the Residential Clean Energy Credit, 25D) ended on December 31, 2025. They were originally scheduled to run through 2032, but last year's tax legislation moved the cutoff up. Projects completed in 2026 no longer qualify for a federal credit.</p>
    <p>Before you shelve those plans, here's what's still on the table:</p>

    <h2>1. Did work in 2025? Claim it this tax season</h2>
    <p>Upgrades completed and placed in service by December 31, 2025 still qualify on the return you file this year, up to $3,200 per year under the old home-improvement credit. Dig out the receipts and manufacturer certificates before you file, and confirm the details with your tax professional.</p>

    <h2>2. State and utility rebates didn't disappear</h2>
    <p>Virginia utilities and local programs still run their own rebates for efficient HVAC equipment, water heaters and insulation. They're smaller than the federal credits were, but they're real money and always worth a check before a project. We flag applicable programs when we quote.</p>

    <h2>3. Efficiency still pays the old-fashioned way</h2>
    <p>The credits sweetened the deal; they were never the deal. Air sealing and insulation remain the cheapest comfort-per-dollar upgrade in our climate, and a right-sized modern system beats a struggling 20-year-old unit on every summer bill, credit or no credit.</p>

    <h2>4. Replace on your schedule, not the equipment's</h2>
    <p>If your A/C or furnace is 15+ years old, the question isn't if. It's whether you replace it planned (compare options, catch rebates, schedule comfortably) or in an emergency during a heat wave, when you'll pay rush pricing for whatever's on the truck.</p>

    <div class="callout">
      <p><strong>A/C or furnace getting up there in years?</strong> Our HVAC team installs and replaces central systems across Northern Virginia. We'll tell you honestly whether yours has good years left or it's time to plan. <a href="/contact.html">Get in touch</a> or call <a href="tel:+17035968375">(703) 596-8375</a>.</p>
    </div>

    <p class="article-sources">Tax information is general. Confirm your situation with a tax professional. Sources: <a href="https://www.irs.gov/credits-deductions/energy-efficient-home-improvement-credit" target="_blank" rel="noopener">IRS: Energy Efficient Home Improvement Credit</a> · <a href="https://www.energystar.gov/about/federal-tax-credits" target="_blank" rel="noopener">ENERGY STAR: Federal Tax Credits</a></p>
""",
    },
]


def article_jsonld(a):
    return {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": a["title"],
        "description": a["desc"],
        "author": {"@type": "Organization", "name": "DFC Home Improvement", "url": SITE},
        "publisher": {
            "@type": "Organization",
            "name": "DFC Home Improvement",
            "logo": {"@type": "ImageObject", "url": f"{SITE}/assets/logo/dfc-logo-white.png"},
        },
        "datePublished": a["date"],
        "dateModified": a["date"],
        "image": f"{SITE}{a['hero']}",
        "url": f"{SITE}/blog/{a['slug']}",
        "mainEntityOfPage": f"{SITE}/blog/{a['slug']}",
    }


def build_article(a):
    body = f"""<main id="top">

<section class="page-head">
  <div class="wrap reveal">
    <p class="breadcrumb"><a href="/index.html">Home</a> / <a href="/blog/">Blog</a> / {html.escape(a['card_title'])}</p>
    <h1>{html.escape(a['title'])}</h1>
  </div>
</section>

<section class="section bg-paper">
  <div class="article-hero"><img src="{a['hero']}" alt="{html.escape(a['hero_alt'])}"></div>
  <div class="article-body">
    <p class="article-meta">By DFC Home Improvement &middot; {a['date_disp']} &middot; {html.escape(a['tag'])}</p>
{a['body']}
{AUTHOR_BOX}
  </div>
</section>
{CTA_BAND}
</main>
"""
    doc = (
        head_block(f"{a['title']} | DFC Home Improvement", a["desc"], f"/blog/{a['slug']}", a["hero"], article_jsonld(a))
        + HEADER + body + FOOTER
    )
    out = os.path.join(ROOT, "blog", a["slug"] + ".html")
    with open(out, "w") as f:
        f.write(doc)
    print("wrote", f"blog/{a['slug']}.html", f"({len(doc)//1024} kb)")


def build_index():
    cards = []
    for a in ARTICLES:
        cards.append(f"""      <a class="blog-card reveal" href="/blog/{a['slug']}">
        <img src="{a['hero']}" alt="{html.escape(a['hero_alt'])}" loading="lazy">
        <div class="bc-body">
          <span class="bc-tag">{html.escape(a['tag'])}</span>
          <h3>{html.escape(a['card_title'])}</h3>
          <p>{html.escape(a['card_desc'])}</p>
          <span class="bc-date">{a['date_disp']}</span>
        </div>
      </a>""")
    # existing cost guide, surfaced as part of the blog
    cards.append("""      <a class="blog-card reveal" href="/cost/kitchen-remodel-cost-northern-virginia">
        <img src="/assets/img/kitchen-polecat-warm.jpg" alt="Two-tone kitchen remodel by DFC Home Improvement" loading="lazy">
        <div class="bc-body">
          <span class="bc-tag">Cost Guide</span>
          <h3>How much does a kitchen remodel cost in Northern Virginia?</h3>
          <p>Real 2026 numbers by scope tier, and where the money actually goes.</p>
          <span class="bc-date">June 2026</span>
        </div>
      </a>""")
    cards_html = "\n".join(cards)
    body = f"""<main id="top">

<section class="page-head">
  <div class="wrap reveal">
    <p class="breadcrumb"><a href="/index.html">Home</a> / Blog</p>
    <h1>Home Notes: the DFC blog</h1>
    <p class="ph-desc">Practical advice for Northern Virginia, DC and Richmond homeowners: maintenance checklists, real cost numbers, market news and how to hire well. Written by the team that does the work.</p>
  </div>
</section>

<section class="section bg-paper">
  <div class="wrap">
    <div class="blog-grid">
{cards_html}
    </div>
  </div>
</section>
{CTA_BAND}
</main>
"""
    jsonld = {
        "@context": "https://schema.org",
        "@type": "Blog",
        "name": "Home Notes: the DFC Home Improvement blog",
        "url": f"{SITE}/blog/",
        "publisher": {"@type": "Organization", "name": "DFC Home Improvement", "url": SITE},
    }
    doc = (
        head_block(
            "Home Notes: Homeowner Advice & Local Market News | DFC Home Improvement",
            "Practical advice for NoVA, DC and Richmond homeowners: maintenance checklists, real remodel costs, market news and how to hire a contractor well.",
            "/blog/", "/assets/img/kitchen-polecat-warm.jpg", jsonld,
        )
        + HEADER + body + FOOTER
    )
    out = os.path.join(ROOT, "blog", "index.html")
    with open(out, "w") as f:
        f.write(doc)
    print("wrote", "blog/index.html", f"({len(doc)//1024} kb)")


if __name__ == "__main__":
    os.makedirs(os.path.join(ROOT, "blog"), exist_ok=True)
    for a in ARTICLES:
        build_article(a)
    build_index()
    print("done.")
