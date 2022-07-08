import gmsh
import math
import os
import sys
import numpy as np

gmsh.initialize(sys.argv)

path = os.path.dirname(os.path.abspath(__file__))
gmsh.merge(os.path.join(path, os.pardir, "cylinder_open.stl"))
gmsh.model.mesh.classifySurfaces(math.pi, True, True)
gmsh.model.mesh.createGeometry()

gmsh.option.setNumber("Geometry.ExtrudeReturnLateralEntities", 0)

N = 5 # number of layers
r = 1.2 # ratio
# d = [0.5] # thickness of first layer
# for i in range(1, N):
    # d.append(d[-1] - (-d[0]) * r**i )
# print(type(d))
n = np.linspace(1, 1, N)
# print(n)
# d = np.logspace(-3, -1, N)
d = np.geomspace(0.01, 0.1, N)
# print(d)
# print(type(d))
# 法線が円筒の外側からさらに外側を向くように設定されるので、dにマイナスを付けている？
e = gmsh.model.geo.extrudeBoundaryLayer(gmsh.model.getEntities(2), n, -d, True)
# print(type([4]))
# print(type(d))
# e = gmsh.model.geo.extrudeBoundaryLayer(gmsh.model.getEntities(2), [4], -d, True)


top_ent = [s for s in e if s[0] == 2]
top_surf = [s[1] for s in top_ent]

gmsh.model.geo.synchronize()
bnd_ent = gmsh.model.getBoundary(top_ent)
bnd_curv = [c[1] for c in bnd_ent]

loops = gmsh.model.geo.addCurveLoops(bnd_curv)
for i in loops:
    top_surf.append(gmsh.model.geo.addPlaneSurface([i]))

gmsh.model.geo.addVolume([gmsh.model.geo.addSurfaceLoop(top_surf)])

# 2次元メッシュの可視化オプションをONにするコマンド
gmsh.option.setNumber("Mesh.SurfaceFaces", 1)
# マウスのホイールをズームイン・ズームアウトを自然な向きに変えるコマンド
gmsh.option.setNumber("General.MouseInvertZoom", 1)
# メッシュの線を見やすくするために、線の太さを変えるコマンド
gmsh.option.setNumber("Mesh.LineWidth", 5)

gmsh.model.geo.synchronize()
gmsh.model.mesh.generate(3)

if "-nopopup" not in sys.argv:
    gmsh.fltk.run()

gmsh.finalize()