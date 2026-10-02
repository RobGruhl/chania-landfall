# Chania Landfall

A self-guided reading tour and pin map for one day in Chania, Crete: Friday 2 October 2026, ashore 08:00 to 18:00 from Virgin Voyages' *Scarlet Lady* at Souda (diverted from Mykonos by the wind). A smaller sibling of [Rhodes Landfall](https://github.com/RobGruhl/rhodes-landfall), without the audio.

- **Map:** https://robgruhl.github.io/chania-landfall/
- **Reader:** https://robgruhl.github.io/chania-landfall/read.html (Rob's track: `#rob`, Jamie's: `#jamie`)

## What is in here

- `docs/` the published pages: `index.html` (map, pin ledger, day plan, briefing) and `read.html` (one stop per page; Rob's or Jamie's track; Short or Long; text size and theme). A service worker keeps the pages and any map tiles already viewed on the phone.
- `data/pins.json` every pin; `data/day.json` the day bar; `data/mast.html` and `data/content.html` the header and briefing; `data/route.json` the walking line over OpenStreetMap's foot network.
- `narration/rob.json`, `narration/jamie.json` the two reading tracks: ten stops, each with `short` and `long` text. Research and assembly by Claude Opus 5.5, prose by Claude Sonnet 5.5.
- `research/` the fact sheets the writers worked from.
- `scripts/` `route.py` (fetches the walking line from routing.openstreetmap.de), `build.py` (assembles `docs/`), `template.html`, `reader.html`, `sw.js`.

## Rebuild

```
cd scripts && python3 route.py && python3 build.py
```

`route.py` needs a Python with a modern TLS stack (Homebrew `python3`). Map data © OpenStreetMap contributors, ODbL.
