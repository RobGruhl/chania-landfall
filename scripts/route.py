"""Fetch the walking line between the route pins, in order, over OpenStreetMap's foot network
(routing.openstreetmap.de, OSRM). Writes data/route.json: {coords:[[lat,lon],...], legs:[...]}."""
import json, os, urllib.request
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pins = json.load(open(os.path.join(ROOT, 'data', 'pins.json')))
way = sorted([p for p in pins if p.get('cat') == 'route' and p.get('n') and not p.get('offroute')], key=lambda p: p['n'])
extra = {p['n']: p.get('via', []) for p in way}
pts = []
for p in way:
    pts.append((p['lat'], p['lon'], p['name']))
    for v in extra[p['n']]: pts.append((v[0], v[1], 'via'))
coords, legs = [], []
for a, b in zip(pts, pts[1:]):
    u = f"https://routing.openstreetmap.de/routed-foot/route/v1/foot/{a[1]},{a[0]};{b[1]},{b[0]}?overview=full&geometries=geojson"
    r = json.load(urllib.request.urlopen(u, timeout=30))['routes'][0]
    seg = [[round(y, 6), round(x, 6)] for x, y in r['geometry']['coordinates']]
    coords += seg if not coords else seg[1:]
    legs.append({'from': a[2], 'to': b[2], 'm': round(r['distance']), 'min': round(r['distance'] / 75, 1)})
json.dump({'coords': coords, 'legs': legs}, open(os.path.join(ROOT, 'data', 'route.json'), 'w'))
for l in legs: print(f"{l['m']:5d} m {l['min']:5.1f} min  {l['from']} -> {l['to']}")
print('total', sum(l['m'] for l in legs), 'm')
