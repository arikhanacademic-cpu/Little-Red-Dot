import json, math, sys
from shapely.geometry import shape, box, mapping, Polygon, MultiPolygon, LineString
from shapely.ops import unary_union
LAT0, LNG0 = 1.35, 103.82
KX = 111.32*math.cos(math.radians(LAT0)); KZ = 110.57
def P(lng, lat): return [round((lng-LNG0)*KX,2), round(-(lat-LAT0)*KZ,2)]
c=json.load(open('0-country.geojson'))
sg=shape(c['features'][0]['geometry'])
polys=[p for p in sg.geoms if p.area>2e-6]  # ~ >0.025 km2
out_sg=[]
for p in polys:
    s=p.simplify(0.0004 if p.area>1e-3 else 0.0002, preserve_topology=True)
    if s.is_empty: continue
    for g in (s.geoms if hasattr(s,'geoms') else [s]):
        ring=[P(x,y) for x,y in g.exterior.coords]
        holes=[[P(x,y) for x,y in h.coords] for h in g.interiors if Polygon(h).area>1e-5]
        out_sg.append([ring]+holes)
ne=json.load(open('ne_10m_admin_0_countries.geojson'))
clip=box(103.45,1.0,104.25,1.62)
ctx=[]
for f in ne['features']:
    if f['properties'].get('ADMIN') in ('Malaysia','Indonesia'):
        g=shape(f['geometry']).intersection(clip)
        if g.is_empty: continue
        for p in (g.geoms if hasattr(g,'geoms') else [g]):
            if p.geom_type!='Polygon' or p.area<5e-5: continue
            p=p.difference(sg.buffer(0.002))
            for q in (p.geoms if hasattr(p,'geoms') else [p]):
                if q.geom_type=='Polygon' and q.area>5e-5:
                    ctx.append([[P(x,y) for x,y in q.simplify(0.001).exterior.coords]])
r=json.load(open('sg-rail.geojson'))
lines={}
COL={'North South Line':'#d42e12','East West Line':'#009645','North East Line':'#9900aa','Circle Line':'#fa9e0d','Downtown Line':'#005ec4','Thomson-East Coast Line':'#9d5b25'}
CODE={'North South Line':'NS','East West Line':'EW','North East Line':'NE','Circle Line':'CC','Downtown Line':'DT','Thomson-East Coast Line':'TE'}
for f in r['features']:
    n=f['properties'].get('name')
    if n not in COL: continue
    g=shape(f['geometry'])
    parts=g.geoms if hasattr(g,'geoms') else [g]
    lines[CODE[n]]={'name':n,'color':COL[n],'paths':[[P(x,y) for x,y in pt.simplify(0.0002).coords] for pt in parts]}
st=[]
for f in r['features']:
    p=f['properties']
    if p.get('stop_type')=='station' and p.get('network')=='singapore-mrt':
        x,y=f['geometry']['coordinates']
        st.append({'n':p['name'],'c':p['station_codes'],'p':P(x,y)})
json.dump({'sg':out_sg,'ctx':ctx,'lines':lines,'stations':st},open('geo.json','w'),separators=(',',':'))
import os; print(os.path.getsize('geo.json'), len(out_sg), len(ctx), len(st), {k:[len(p) for p in v['paths']] for k,v in lines.items()})
