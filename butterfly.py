import numpy as np, trimesh
from shapely.geometry import Point, LineString
from shapely import affinity
from shapely.ops import unary_union
def ell(cx,cy,a,b,ang):
    return affinity.rotate(affinity.translate(affinity.scale(Point(0,0).buffer(1,resolution=64),a,b),cx,cy),ang,origin=(cx,cy))
R=[ell(22,14,24,15,35), ell(17,-15,15,11,-35)]
L=[affinity.scale(g,-1,1,origin=(0,0)) for g in R]
wings=unary_union(R+L)
# decorative holes (kept well inside, leaving >=2.5mm walls)
holes=[]
for s in (1,-1):
    holes+= [Point(s*28,20).buffer(6), Point(s*16,9).buffer(3.5), Point(s*19,-17).buffer(4.5)]
wings=wings.difference(unary_union(holes))
body=affinity.scale(Point(0,0).buffer(1,resolution=64),3.5,24)
ant=unary_union([LineString([(0,20),(-6,32),(-10,36)]).buffer(1.2), LineString([(0,20),(6,32),(10,36)]).buffer(1.2),
                 Point(-10,36).buffer(2.2), Point(10,36).buffer(2.2)])
base=unary_union([wings,body,ant])
m1=trimesh.creation.extrude_polygon(base,3.0)
m2=trimesh.creation.extrude_polygon(body,6.0)
mesh=trimesh.boolean.union([m1,m2],engine='manifold')
mesh.export('butterfly.stl')
print(mesh.is_watertight, mesh.bounds, len(mesh.faces))
