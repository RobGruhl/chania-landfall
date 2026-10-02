"""Build docs/ from data/ and narration/: the map (index.html), the reader (read.html),
the service worker and the Home Screen manifest. Run from scripts/: python3 build.py"""
import json, os, math, hashlib
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = lambda *p: os.path.join(ROOT, *p)
read = lambda *p: open(D(*p), encoding='utf-8').read()

def hav(a, b):
    R = 6371000; la1, lo1, la2, lo2 = map(math.radians, (*a, *b))
    h = math.sin((la2-la1)/2)**2 + math.cos(la1)*math.cos(la2)*math.sin((lo2-lo1)/2)**2
    return 2*R*math.asin(math.sqrt(h))

pins = json.load(open(D('data', 'pins.json')))
day = json.load(open(D('data', 'day.json')))
route = json.load(open(D('data', 'route.json'))) if os.path.exists(D('data', 'route.json')) else {'coords': []}
# walk minutes from the shuttle stop: straight line plus a third for the alleys, at 75 m a minute
origin = next(p for p in pins if p.get('origin'))
for p in pins:
    d = hav((origin['lat'], origin['lon']), (p['lat'], p['lon'])) * 1.33
    p['walk'] = None if d > 4000 else max(1, round(d / 75))

stops = {}
for who in ('rob', 'jamie'):
    f = D('narration', who + '.json')
    stops[who] = sorted(json.load(open(f)), key=lambda x: x['n']) if os.path.exists(f) else []
readmap = {}
for who, lst in stops.items():
    for s in lst: readmap.setdefault(s['slug'], []).append(who)
places = {p['aud']: p['name'] for p in pins if p.get('aud')}

PWA_HEAD = '''<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="icon-180.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Chania">
<script>if('serviceWorker' in navigator&&(location.protocol==='https:'||location.hostname==='localhost'))navigator.serviceWorker.register('sw.js').catch(function(){});</script>'''
j = lambda o: json.dumps(o, ensure_ascii=False, separators=(',', ':'))

t = read('scripts', 'template.html')
t = t.replace('/*__LEAFLET_CSS__*/', read('data', 'leaflet.min.css'))
t = t.replace('/*__LEAFLET_JS__*/', read('data', 'leaflet.min.js').replace('//# sourceMappingURL=leaflet.js.map', ''))
t = t.replace('/*__ROUTE__*/[]', j(route['coords'])).replace('/*__PINS__*/[]', j(pins)).replace('/*__DAY__*/[]', j(day))
t = t.replace('/*__READ__*/{}', j(readmap)).replace('<!--__PWA_HEAD__-->', PWA_HEAD)
t = t.replace('<!--__MAST__-->', read('data', 'mast.html')).replace('<!--__CONTENT__-->', read('data', 'content.html'))
open(D('docs', 'index.html'), 'w').write(t)

r = read('scripts', 'reader.html')
r = r.replace('/*__STOPS__*/{}', j(stops)).replace('/*__PLACES__*/{}', j(places)).replace('<!--__PWA_HEAD__-->', PWA_HEAD)
open(D('docs', 'read.html'), 'w').write(r)

open(D('docs', 'manifest.webmanifest'), 'w').write(json.dumps({
    'name': 'Chania Landfall', 'short_name': 'Chania', 'display': 'standalone', 'scope': './', 'start_url': './',
    'background_color': '#FAF8F3', 'theme_color': '#1F6F8B',
    'icons': [{'src': 'icon-180.png', 'sizes': '180x180', 'type': 'image/png'}, {'src': 'icon-512.png', 'sizes': '512x512', 'type': 'image/png'}]}, indent=1))
v = hashlib.sha256()
for f in ('index.html', 'read.html', 'manifest.webmanifest'): v.update(open(D('docs', f), 'rb').read())
open(D('docs', 'sw.js'), 'w').write(read('scripts', 'sw.js').replace('__VERSION__', v.hexdigest()[:12]))
open(D('docs', '.nojekyll'), 'w').write('')
print('index', len(t), 'read', len(r), 'stops', {k: len(v) for k, v in stops.items()}, 'pins', len(pins))
for p in pins: print(f"{p['cat']:9s} {p.get('n') or '':>2} {p['walk']!s:>4} min  {p['name']}")
