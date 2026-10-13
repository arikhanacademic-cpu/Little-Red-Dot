# The Little Red Dot

A 3D atlas of software engineer pay in Singapore. Each company is a tower on a map of the island, and its height is the company's median total compensation for software engineers in Singapore, taken from Levels.fyi.

Inspired by Levels.fyi's [The Peninsula](https://www.levels.fyi/atlas).

## Features

- **Tour mode:** scroll across the island from Changi to one-north. Each chapter is labelled with its MRT station code.
- **Explore mode:** orbit, pan and zoom, then click a tower to see median pay, the base/stock/bonus split where published, and pay by level.
- **MRT ride:** ride the East-West Line from Pasir Ris to Tuas Link.
- **Search and ranking:** open with ⌘K / Ctrl+K.
- **SGD or USD**, light and dark themes, and layouts for desktop and mobile.

## Run it

It's a single static file with no build step.

```bash
python3 -m http.server 8000
# open http://localhost:8000
```

You can also open `index.html` directly in a browser.

### GitHub Pages

1. Push this folder to a repo.
2. Go to **Settings → Pages → Build and deployment**, choose **Deploy from a branch**, then pick `main` / root.
3. The site goes live at `https://<user>.github.io/<repo>/`.

## Project layout

```
index.html            The app (HTML, CSS and JS, with the map geometry inlined)
data/geo.json         Projected and simplified coastline, MRT lines and stations (km units)
data/companies.json   Company pay data and office locations (also inlined in index.html)
scripts/prep_geo.py   Builds geo.json from the source GeoJSON files
```

The company data lives in the `const C = [...]` array in `index.html`. `data/companies.json` holds the same data in a readable form. If you edit one, update the other.

### Rebuilding the geometry

```bash
pip install shapely
curl -LO https://raw.githubusercontent.com/yinshanyang/singapore/master/maps/0-country.geojson
curl -LO https://raw.githubusercontent.com/cheeaun/sgraildata/master/data/v1/sg-rail.geojson
curl -LO https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_10m_admin_0_countries.geojson
python3 scripts/prep_geo.py   # writes geo.json in the current folder
```

Then replace the `const GEO = {...}` object in `index.html` with the contents of the new `geo.json`.

## Data notes

- Pay figures are Levels.fyi Singapore software engineer medians, collected in October 2026. They are SGD per year.
- The USD figures use a fixed rate of 0.7834.
- The base/stock/bonus split is shown only where Levels.fyi publishes a Singapore median package.
- The submission counts for large companies cover all their locations worldwide, not only Singapore.
- Fifteen companies have no verified Singapore office address. They are placed together on a marked lot in Marina South and drawn with dashed outlines.
- Jump Trading, UOB and Alibaba have very little data, so their figures are flagged.

## Credits

- Coastline: [yinshanyang/singapore](https://github.com/yinshanyang/singapore)
- MRT lines and stations: [cheeaun/sgraildata](https://github.com/cheeaun/sgraildata), from © OpenStreetMap contributors (ODbL)
- Neighbouring coastlines: [Natural Earth](https://www.naturalearthdata.com/) (public domain)
- Rendering: [three.js](https://threejs.org/) r128, loaded from a CDN
- Pay data: [Levels.fyi](https://www.levels.fyi)

This is an unofficial fan project. It is not affiliated with Levels.fyi.
