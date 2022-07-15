import gmsh
import sys
import numpy as np

gmsh.initialize(sys.argv)
gmsh.model.add("Tube boundary layer")


# 設定はまとめて最初に書いたほうが良いと思う
gmsh.option.setNumber("Mesh.MeshSizeMax", 0.3)
order2 = False

# surfaceとvolumeを見えるようにする設定
gmsh.option.setNumber("Geometry.Surfaces", 1)
gmsh.option.setNumber("Geometry.Volumes", 1)
# 2次元メッシュの可視化オプションをONにするコマンド
gmsh.option.setNumber("Mesh.SurfaceFaces", 1)
# マウスのホイールをズームイン・ズームアウトを自然な向きに変えるコマンド
gmsh.option.setNumber("General.MouseInvertZoom", 1)
# メッシュの法線を表示
# gmsh.option.setNumber("Mesh.Normals", 20)
# メッシュの線を見やすくするために、線の太さを変えるコマンド
gmsh.option.setNumber("Mesh.LineWidth", 4)
# 目盛りのついたboxを表示
gmsh.option.setNumber("General.Axes", 3)
# gmsh.option.setNumber("")

c1 = gmsh.model.occ.addCylinder(0, 0, 0, 10, 0, 0, 1)
gmsh.model.occ.remove(gmsh.model.occ.getEntities(3))
# ここは自動化したい
gmsh.model.occ.remove([(2,2), (2,3)]) # fixme: automate this
gmsh.model.occ.synchronize()

gmsh.option.setNumber("Geometry.ExtrudeReturnLateralEntities", 0)
n = np.linspace(1, 1, 5)
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
for i in loops:
    top_surf.append(gmsh.model.geo.addPlaneSurface([i]))

# create the inner volume
gmsh.model.geo.addVolume([gmsh.model.geo.addSurfaceLoop(top_surf)])
gmsh.model.geo.synchronize()

gmsh.model.addPhysicalGroup(2,[1],1);gmsh.model.setPhysicalName(2,1,"wall")
gmsh.model.addPhysicalGroup(2,[20,27],2);gmsh.model.setPhysicalName(2,2,"inlet")
gmsh.model.addPhysicalGroup(2,[12,26],3);gmsh.model.setPhysicalName(2,3,"outlet")
gmsh.model.addPhysicalGroup(3,[1,2],1);gmsh.model.setPhysicalName(3,1,"internal")

gmsh.model.geo.synchronize()
# generate the mesh
gmsh.option.setNumber('Mesh.Algorithm', 1)
gmsh.model.mesh.generate(3)

if order2:
    gmsh.model.mesh.setOrder(2)
    gmsh.model.mesh.optimize("HighOrderFastCurving")

gmsh.write('tube.msh')
gmsh.write('tube.msh2')

if "-nopopup" not in sys.argv:
    gmsh.fltk.run()

gmsh.finalize()