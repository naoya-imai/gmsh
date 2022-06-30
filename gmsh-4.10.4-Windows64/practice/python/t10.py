import gmsh
import sys

gmsh.initialize(sys.argv)
gmsh.model.add("t10")

# まずは簡単な長方形形状作成
lc = .15
gmsh.model.geo.addPoint(0.0, 0.0, 0.0, lc, 1)
gmsh.model.geo.addPoint(1.0, 0.0, 0.0, lc, 2)
gmsh.model.geo.addPoint(1.0, 1.0, 0.0, lc, 3)
gmsh.model.geo.addPoint(0.0, 1.0, 0.0, lc, 4)
gmsh.model.geo.addPoint(0.2, 0.5, 0.0, lc ,5)
gmsh.model.geo.addLine(1, 2, 1)
gmsh.model.geo.addLine(2, 3, 2)
gmsh.model.geo.addLine(3, 4, 3)
gmsh.model.geo.addLine(4, 1, 4)
gmsh.model.geo.addCurveLoop([1, 2, 3, 4], 5)
gmsh.model.geo.addPlaneSurface([5], 6)

gmsh.model.geo.synchronize()

# ここからがよくわからん

gmsh.model.mesh.field.add("Distance", 1)
gmsh.model.mesh.field.setNumbers(1, "PointsList", [5])
gmsh.model.mesh.field.setNumbers(1, "CurvesList", [2])
gmsh.model.mesh.field.setNumber(1, "Sampling", 100)

gmsh.write("t10.msh")

if "-nopopup" not in sys.argv:
    gmsh.fltk.run()

gmsh.finalize()