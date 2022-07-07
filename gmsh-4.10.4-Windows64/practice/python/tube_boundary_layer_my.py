from asyncio import format_helpers
import gmsh
import sys
import math
import numpy as np

gmsh.initialize(sys.argv)
gmsh.model.add("Tube boundary layer")

# meshing constraints
# メッシュ制約
gmsh.option.setNumber("Mesh.MeshSizeMax", 0.1)
order2 = False

# fuse 2 cylinders and only keep outside shell
# 2つの円柱を融合し、外殻のみを維持する

# 始端の円の中心座標、終端の円の中心座標、半径
c1 = gmsh.model.occ.addCylinder(0, 0, 0, 5, 0, 0, 0.5)
c2 = gmsh.model.occ.addCylinder(2, 0, -2, 0, 0, 2, 0.3)
s = gmsh.model.occ.fuse([(3, c1)], [(3, c2)])
gmsh.model.occ.remove(gmsh.model.occ.getEntities(3))
gmsh.model.occ.remove([(2,2), (2,3), (2,5)]) # fixme: automate this
gmsh.model.occ.synchronize()

# create boundary layer extrusion, and make extrusion only return "top" surfaces
# and volumes, not lateral surfaces
# 境界層押し出しを作成し、押し出しが側面ではなく「上面」の表面と体積のみを返すようにする。
gmsh.option.setNumber("Geometry.ExtrudeReturnLateralEntities", 0)
n = np.linspace(1, 1, 5)
print(n)
d = np.logspace(-3, -1, 5)
e = gmsh.model.geo.extrudeBoundaryLayer(gmsh.model.getEntities(2), n, -d, True)

# get "top" surfaces created by extrusion
top_ent = [s for s in e if s[0] == 2]
top_surf = [s[1] for s in top_ent]

gmsh.model.geo.synchronize()
bnd_ent = gmsh.model.getBoundary(top_ent)
bnd_curv = [c[1] for c in bnd_ent]

# create plane surfaces filling the holes
loops = gmsh.model.geo.addCurveLoops(bnd_curv)
for l in loops:
    top_surf.append(gmsh.model.geo.addPlaneSurface([l]))

# create the inner volume
gmsh.model.geo.addVolume([gmsh.model.geo.addSurfaceLoop(top_surf)])
gmsh.model.geo.synchronize()

# generate the mesh
gmsh.model.mesh.generate(3)

gmsh.option.setNumber("Mesh.SurfaceFaces", 1)
gmsh.option.setNumber("General.MouseInvertZoom", 1)

if order2:
    gmsh.model.mesh.setOrder(2)
    gmsh.model.mesh.optimize('HighOrderFastCurving')

if '-nopopup' not in sys.argv:
    gmsh.fltk.run()

gmsh.finalize()