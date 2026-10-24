# Vertex Detailing website

Static site. No WordPress, no database.

- `pages/*.html`  page content (one file per page). Edit these.
- `site.css`, `site.js`  shared styles and scripts
- `img/`  web-sized photos (plates blurred)
- `functions/api/lead.js`  Cloudflare Pages Function: forwards the quick-quote form to the OrbisX Lead API.
  Needs an environment variable ORBISX_LEAD_KEY set in the Cloudflare Pages project. The key is NOT in this repo.
- `_redirects`  old WordPress URLs -> new pages (Cloudflare Pages format)
- `build.py`  assembles pages + header/footer into `dist/`. Run: `python3 build.py`
- `dist/`  what gets deployed. Never edit by hand.

OrbisX embeds:
- Booking: multi-step form "Default 2.0" (config VSnKt). Embed is in pages/book.html.
- Gift cards: iframe of https://orbisx.ca/app/gift-cards/VSVwv in pages/gift-cards.html.
- Thank-you redirect in OrbisX points to /thanks.html.
