// Chania Landfall service worker: keeps the pages on the phone, plus any map tiles and fonts
// already seen, so the tour still opens when the signal drops in the old town's alleys.
const VERSION = '957cac0cb710';
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

// Answer from the phone at once, refresh the copy in the background when there is signal.
async function stale(cacheName, req, event) {
  const cache = await caches.open(cacheName);
  const hit = await cache.match(req, {ignoreSearch: cacheName === SHELL, ignoreVary: true});
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
  e.respondWith(stale(SHELL, req, e));
});
