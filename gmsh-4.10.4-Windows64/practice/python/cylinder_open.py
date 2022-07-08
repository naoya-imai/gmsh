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
t = np.full(N, 0.02)
for i in range(0, N):
    t[i] = t[i] * r ** i
print(t)
for i in range(1, N):
    t[i] += t[i - 1]
print(t)
# for i in range(0, N):
#     print(t[i])
# for i in range(0, N):
    # print(d[i])
for i in range(1, N):
    d[i] = d[i] + d[i - 1]
print(d)
# print(type(d))
# 法線が円筒の外側からさらに外側を向くように設定されるので、dにマイナスを付けている？

# 重要
# それぞれのd[i]の厚さをi番目の層の厚さとしているのではなく、i番目の層を元々の基準線からどれくらいの距離に取るかを設定している模様

e = gmsh.model.geo.extrudeBoundaryLayer(gmsh.model.getEntities(2), n, -t, True)
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
gmsh.option.setNumber("Mesh.LineWidth", 4)
# 目盛りのついたboxを表示
gmsh.option.setNumber("General.Axes", 3)
# メッシュの法線を表示
gmsh.option.setNumber("Mesh.Normals", 30)

gmsh.model.geo.synchronize()
# gmsh.option.setNumber("Mesh.MeshSizeMin", 0.3)
# gmsh.option.setNumber("Mesh.MeshSizeMax", 0.3)
gmsh.model.mesh.generate(3)
print("finish meshing")
print("=============================")
gmsh.model.mesh.optimize('Netgen', True)
print("=============================")
gmsh.write('cylinder_open.vtk')

if "-nopopup" not in sys.argv:
    gmsh.fltk.run()

gmsh.finalize()