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
gmsh.model.geo.synchronize()

# gmsh.option.setNumber("Geometry.ExtrudeReturnLateralEntities", 0)

# n = np.linspace(1, 1, 1)
# t = np.full(1, 0.2)
# e = gmsh.model.geo.extrudeBoundaryLayer(gmsh.model.getEntities(2), n, -t, True)
# gmsh.model.geo.synchronize()
# top_ent = [s for s in e if s[0] == 2]
# print(top_ent)
# top_surf = (s[1] for s in top_ent)
# print(top_surf)

gmsh.model.geo.synchronize()

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

if "-nopopup" not in sys.argv:
    gmsh.fltk.run()

gmsh.finalize()