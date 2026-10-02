// Chania Landfall service worker: keeps the pages on the phone, plus any map tiles and fonts
// already seen, so the tour still opens when the signal drops in the old town's alleys.
const VERSION = '__VERSION__';
const SHELL = 'chania-shell-' + VERSION;
const TILES = 'chania-tiles';
const FONTS = 'chania-fonts';
const SHELL_FILES = ['./', 'index.html', 'read.html', 'manifest.webmanifest', 'icon-180.png', 'icon-512.png'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(SHELL).then(c => c.addAll(SHELL_FILES.map(f => new Request(f, {cache: 'reload'})))).then(() => self.skipWaiting()));
});

self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(keys => Promise.all(
    keys.filter(k => k.startsWith('chania-shell-') && k !== SHELL).map(k => caches.delete(k))
  )).then(() => self.clients.claim()));
});

// Pages: fresh from the network when there is signal (3 s grace), the phone's copy when not.
async function page(req) {
  const cache = await caches.open(SHELL);
  try {
    const res = await Promise.race([fetch(req, {cache: 'no-cache'}), new Promise((_, no) => setTimeout(() => no(new Error('slow')), 3000))]);
    if (res.ok) cache.put(req, res.clone());
    return res;
  } catch (e) {
    const hit = await cache.match(req, {ignoreSearch: true});
    if (hit) return hit;
    return fetch(req);
  }
}

// Fonts: the phone's copy at once, refreshed in the background.
async function stale(cacheName, req, event) {
  const cache = await caches.open(cacheName);
  const hit = await cache.match(req, {ignoreVary: true});
  const refresh = fetch(req).then(res => { if (res.ok || res.type === 'opaque') cache.put(req, res.clone()); return res; });
  if (hit) { event.waitUntil(refresh.catch(() => {})); return hit; }
  return refresh;
}

// Tiles do not change in a day: phone copy first, network only for tiles not yet seen.
async function tile(req) {
  const cache = await caches.open(TILES);
  const hit = await cache.match(req);
  if (hit) return hit;
  const res = await fetch(req);
  if (res.ok || res.type === 'opaque') cache.put(req, res.clone());
  return res;
}

self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.hostname === 'tile.openstreetmap.org') { e.respondWith(tile(req)); return; }
  if (url.hostname === 'fonts.googleapis.com' || url.hostname === 'fonts.gstatic.com') { e.respondWith(stale(FONTS, req, e)); return; }
  const base = new URL(self.registration.scope);
  if (url.origin !== base.origin || !url.pathname.startsWith(base.pathname)) return;
  e.respondWith(page(req));
});
