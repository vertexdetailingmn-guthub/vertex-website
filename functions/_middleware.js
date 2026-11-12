// Send www.vertexdetailing.co to the bare domain so Google sees one copy of the site.
// (The same can be done with a Cloudflare Redirect Rule; if you add one, this file can go.)
export async function onRequest({ request, next }) {
  const url = new URL(request.url);
  if (url.hostname === 'www.vertexdetailing.co') {
    url.hostname = 'vertexdetailing.co';
    return Response.redirect(url.toString(), 301);
  }
  return next();
}
