import gmsh
import math
import os
import sys

gmsh.initialize(sys.argv)

path = os.path.dirname(os.path.abspath(__file__))
gmsh.merge(os.path.join(path, os.pardir, "cylinder_open.stl"))
gmsh.model.mesh.classifySurfaces(math.pi, True, True)
gmsh.model.mesh.createGeometry()

gmsh.option.setNumber("Geometry.ExtrudeReturnLateralEntities", 0)

white = (255, 255, 255)
black = (0, 0, 0)


# 2次元メッシュの可視化オプションをONにするコマンド
gmsh.option.setNumber("Mesh.SurfaceFaces", 1)
gmsh.option.setNumber("General.MouseInvertZoom", 1)
# gmsh.option.setColor("General.Background", 100, 100, 100)
gmsh.option.setColor("General.Background", white[0], white[1], white[2])
# gmsh.option.setColor("General.Text", 255, 200, 200)

gmsh.model.geo.synchronize()
gmsh.model.mesh.generate(3)

if "-nopopup" not in sys.argv:
    gmsh.fltk.run()

gmsh.finalize()