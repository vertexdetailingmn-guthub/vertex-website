// Cloudflare Pages Function: POST /api/lead
// Forwards a quick-quote request to the OrbisX Lead API. The API key lives in
// the Pages project's environment variables (ORBISX_LEAD_KEY), never in the page.
export async function onRequestPost({ request, env }) {
  const allowed = ['contact', 'phone', 'email', 'city', 'interest', 'notes', 'auto_year', 'auto_make', 'auto_model'];
  let body;
  try { body = await request.json(); } catch { return new Response('bad json', { status: 400 }); }
  if (!body.contact || !body.phone) return new Response('missing fields', { status: 400 });
  const p = new URLSearchParams({ key: env.ORBISX_LEAD_KEY, dothis: 'saveLead', source: 'Website', leadTag: 'Quick quote' });
  for (const k of allowed) if (body[k]) p.set(k, String(body[k]).slice(0, 300));
  const r = await fetch('https://orbisx.ca/app/api/VSVwv?' + p.toString(), { method: 'GET' });
  return new Response(JSON.stringify({ ok: r.ok }), { status: r.ok ? 200 : 502, headers: { 'content-type': 'application/json' } });
}
