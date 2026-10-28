import numpy as np, trimesh
from shapely.geometry import Point, Polygon
from shapely.ops import unary_union
from matplotlib.textpath import TextPath
from matplotlib.font_manager import FontProperties
# cloud outline (mm)
circles=[(-40,0,22),(-15,12,26),(15,14,24),(40,2,20),(0,-8,24),(-28,-10,16),(28,-10,16)]
cloud=unary_union([Point(x,y).buffer(r,resolution=64) for x,y,r in circles])
cloud=cloud.buffer(2).buffer(-2)
base_h=5.0
base=trimesh.creation.extrude_polygon(cloud,base_h)
# rim (raised 2.5 mm, 3 mm wide)
rim=cloud.difference(cloud.buffer(-3))
rim_m=trimesh.creation.extrude_polygon(rim,2.5); rim_m.apply_translation([0,0,base_h])
# text
fp=FontProperties(fname='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf')
tp=TextPath((0,0),"C I J E",size=20,prop=fp)
polys=[]
for p in tp.to_polygons():
    if len(p)>=3: polys.append(Polygon(p))
# even-odd assemble: sort by area, xor
geom=Polygon()
for p in sorted(polys,key=lambda q:-q.area):
    geom=geom.symmetric_difference(p.buffer(0))
minx,miny,maxx,maxy=geom.bounds
from shapely import affinity
geom=affinity.translate(geom,-(minx+maxx)/2,-(miny+maxy)/2+2)
geom=geom.buffer(0.3)  # thicken strokes slightly
geoms=list(geom.geoms) if hasattr(geom,'geoms') else [geom]
txt=[trimesh.creation.extrude_polygon(g,2.5) for g in geoms]
for t in txt: t.apply_translation([0,0,base_h])
m=trimesh.boolean.union([base,rim_m]+txt,engine='manifold')
m.apply_translation(-m.bounds[0]*[1,1,1]+[0,0,0])
print(m.is_watertight,m.extents,len(m.faces))
m.export('cloud_cije.stl')
