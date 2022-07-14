import gmsh
import math
import os
import sys
import numpy as np

gmsh.initialize(sys.argv)

path = os.path.dirname(os.path.abspath(__file__))
gmsh.merge(os.path.join(path, "cylinder_open.stl"))
gmsh.model.mesh.classifySurfaces(math.pi, True, True)
gmsh.model.mesh.createGeometry()

gmsh.option.setNumber("Geometry.ExtrudeReturnLateralEntities", 0)

N = 5 # number of layers
r = 1.2 # ratio
n = np.linspace(1, 1, N) # [1,1,1,1,1]
t = np.full(N, 0.02) # distance from the reference line
for i in range(0, N):
    t[i] = t[i] * r ** i
for i in range(1, N):
    t[i] += t[i - 1]
# 法線が円筒の外側からさらに外側を向くように設定されるので、dにマイナスを付けている

# ---重要---
# それぞれのd[i]の厚さをi番目の層の厚さとしているのではなく、i番目の層を元々の基準線からどれくらいの距離に取るかを設定している模様
# 法線が円筒の外側からさらに外側を向くように設定されるので、dにマイナスを付けている
# ----------
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

gmsh.model.geo.synchronize()

# ここは完璧な手作業、ボトルネックがここになる
# gmsh.model.addPhysicalGroupしてからsetPhysicalNameで名前をつける、これでワンセットなのでセミコロンを使って1行で書く
gmsh.model.addPhysicalGroup(2,[2],1);gmsh.model.setPhysicalName(2,1,"wall")
gmsh.model.addPhysicalGroup(2,[11,17],2);gmsh.model.setPhysicalName(2,2,"inlet")
gmsh.model.addPhysicalGroup(2,[15,18],3);gmsh.model.setPhysicalName(2,3,"outlet")
gmsh.model.addPhysicalGroup(3,[1,2],1);gmsh.model.setPhysicalName(3,1,"internal")


# 2次元メッシュのメッシュ作成アルゴリズムの選択
gmsh.option.setNumber('Mesh.Algorithm', 1)

# 2次元メッシュの可視化オプションをONにするコマンド
gmsh.option.setNumber("Mesh.SurfaceFaces", 1)
# マウスのホイールをズームイン・ズームアウトを自然な向きに変えるコマンド
gmsh.option.setNumber("General.MouseInvertZoom", 1)
# メッシュの線を見やすくするために、線の太さを変えるコマンド
gmsh.option.setNumber("Mesh.LineWidth", 4)
# 目盛りのついたboxを表示
gmsh.option.setNumber("General.Axes", 3)
# メッシュの法線を表示
# gmsh.option.setNumber("Mesh.Normals", 20)

gmsh.model.geo.synchronize()
gmsh.option.setNumber("Mesh.MeshSizeMin", 0.2)
gmsh.option.setNumber("Mesh.MeshSizeMax", 0.2)
gmsh.model.mesh.generate(3)
# print("finish meshing")
# print("=============================")
# gmsh.model.mesh.optimize('Netgen', True)
# print("=============================")
gmsh.write('cylinder_open.msh')
gmsh.write('cylinder_open.msh2')

if "-nopopup" not in sys.argv:
    gmsh.fltk.run()

gmsh.finalize()