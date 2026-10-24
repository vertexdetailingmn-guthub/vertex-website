#!/usr/bin/env python3
"""Assemble the Vertex site: pages/*.html (body only, with a leading META block) -> dist/*.html"""
import os, re, glob, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, 'dist')
BOOK = 'https://orbisx.ca/app/booknow/VSVwv'
PHONE = '(651) 363-4422'
SMS = 'sms:6513634422'

NAV = [('pricing.html', 'Pricing'), ('mobile-car-detailing.html', 'Detailing'), ('ceramic-coating.html', 'Ceramic Coating'),
       ('maintenance-plans.html', 'Maintenance'), ('reviews.html', 'Reviews'), ('contact.html', 'Contact')]

def head(title, desc, canonical):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="https://vertexdetailing.co/{canonical}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="https://vertexdetailing.co/img/hero.jpg">
<meta property="og:type" content="website">
<meta name="theme-color" content="#141518">
<link rel="icon" href="favicon.ico">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700;800&family=Barlow:wght@400;500;600&display=swap">
<link rel="stylesheet" href="site.css">
</head>
<body>'''

def header(current):
    items = ''.join(f'<li><a href="{h}"{" aria-current=\"page\"" if h == current else ""}>{t}</a></li>' for h, t in NAV)
    return f'''<header class="nav">
  <div class="wrap">
    <a class="logo" href="index.html"><img src="img/logo.png" alt="Vertex Detailing" width="640" height="293"></a>
    <ul>{items}</ul>
    <a class="btn btn-primary" href="book.html">Book Online</a>
  </div>
</header>'''

FOOTER = f'''<section class="final">
  <div class="wrap">
    <h2>Ready for that new-car feeling?</h2>
    <div class="cta-row" style="margin-top:0"><a class="btn btn-primary" href="book.html">Book Online Now</a><a class="btn btn-ghost" href="{SMS}">Text {PHONE}</a></div>
  </div>
</section>
<footer>
  <div class="wrap">
    <div>
      <a class="logo" href="index.html"><img src="img/logo.png" alt="Vertex Detailing" width="640" height="293" style="height:44px;width:auto"></a>
      <p style="margin-top:14px;max-width:40ch">Mobile car detailing and ceramic coating, Woodbury MN. Owner-operated and fully insured. Minnesota LLC.</p>
    </div>
    <div>
      <h4>Services</h4>
      <ul><li><a href="mobile-car-detailing.html">Mobile car detailing</a></li><li><a href="ceramic-coating.html">Ceramic coating</a></li><li><a href="maintenance-plans.html">Maintenance plans</a></li><li><a href="boat-rv-detailing.html">Boats &amp; RVs</a></li><li><a href="gift-cards.html">Gift cards</a></li></ul>
    </div>
    <div>
      <h4>Company</h4>
      <ul><li><a href="reviews.html">Reviews</a></li><li><a href="service-area.html">Service area</a></li><li><a href="faq.html">FAQ</a></li><li><a href="contact.html">Contact</a></li><li><a href="https://orbisx.ca/app/hublogin/VSVwv">Customer login</a></li><li><a href="privacy.html">Privacy</a> · <a href="terms.html">Terms</a></li></ul>
    </div>
  </div>
  <div class="copy"><div class="wrap"><span>© 2026 Vertex Detailing LLC · Woodbury, MN</span><span class="phone" style="font-size:20px">{PHONE}</span></div></div>
</footer>
<div class="stickybar">
  <a class="btn btn-outline" href="{SMS}">Text Us</a>
  <a class="btn btn-primary" href="book.html">Book Online</a>
</div>
<script src="site.js"></script>
</body>
</html>'''

def build():
    os.makedirs(DIST, exist_ok=True)
    for f in ['site.css', 'site.js']:
        shutil.copy(os.path.join(ROOT, f), DIST)
    if os.path.isdir(os.path.join(DIST, 'img')):
        shutil.rmtree(os.path.join(DIST, 'img'))
    shutil.copytree(os.path.join(ROOT, 'img'), os.path.join(DIST, 'img'))
    for ico in ['favicon.ico', 'apple-touch-icon.png', '_redirects', 'robots.txt']:
        p = os.path.join(ROOT, ico)
        if os.path.exists(p): shutil.copy(p, DIST)
    for src in glob.glob(os.path.join(ROOT, 'pages', '*.html')):
        body = open(src).read()
        m = re.match(r'<!--META\s+title:(.*?)\n\s*desc:(.*?)\n-->\s*', body, re.S)
        title, desc = m.group(1).strip(), m.group(2).strip()
        body = body[m.end():]
        name = os.path.basename(src)
        body = body.replace('{BOOK}', BOOK).replace('{SMS}', SMS).replace('{PHONE}', PHONE)
        out = head(title, desc, '' if name == 'index.html' else name) + '\n' + header(name) + '\n' + body + '\n' + FOOTER
        open(os.path.join(DIST, name), 'w').write(out)
        print('built', name)

if __name__ == '__main__':
    build()
