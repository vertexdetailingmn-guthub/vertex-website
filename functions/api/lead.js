// Cloudflare Pages Function: POST /api/lead
// Forwards a quick-quote request to the OrbisX Lead API. The API key lives in
// the Pages project's secrets (ORBISX_LEAD_KEY), never in the page.
export async function onRequestPost({ request, env }) {
  const allowed = ['contact', 'phone', 'email', 'city', 'interest', 'notes', 'auto_year', 'auto_make', 'auto_model'];
  let body;
  try { body = await request.json(); } catch { return json({ ok: false, error: 'bad json' }, 400); }
  if (!body.contact || !body.phone) return json({ ok: false, error: 'missing fields' }, 400);
  const key = (env.ORBISX_LEAD_KEY || '').trim();
  if (!key) return json({ ok: false, error: 'server not configured' }, 500);
  const p = new URLSearchParams({ key, dothis: 'saveLead', source: 'Website', leadTag: 'Quick quote' });
  for (const k of allowed) if (body[k]) p.set(k, String(body[k]).slice(0, 300));
  const r = await fetch('https://orbisx.ca/app/api/VSVwv?' + p.toString());
  const text = await r.text();
  let ok = false, message = '';
  try { const d = JSON.parse(text); ok = d.success === true; message = d.message || ''; } catch { message = text.slice(0, 120); }
  return json({ ok, message }, ok ? 200 : 502);
}
function json(obj, status) {
  return new Response(JSON.stringify(obj), { status, headers: { 'content-type': 'application/json' } });
}
