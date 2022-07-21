import gmsh
import sys

gmsh.initialize()
gmsh.model.add("t1")

# gmsh.option.setNumber("General.Terminal", 1)
lc = 1e-2
gmsh.model.geo.addPoint(0, 0, 0, lc, 1)
gmsh.model.geo.addPoint(0.1, 0, 0, lc, 2)
gmsh.model.geo.addPoint(0.1, 0.3, 0, lc, 3)
gmsh.model.geo.addPoint(0, 0.3, 0, lc, 4)
p4 = gmsh.model.geo.addPoint(0, 0.3, 0, lc)
p5 = gmsh.model.geo.addPoint(0, 0.3, 0, lc)
# print(f"p4 is {p4}")
# print(f"p5 is {p5}")
# gmsh.option.setNumber("General.Terminal", 2)
gmsh.model.geo.addLine(1, 2, 1)
gmsh.model.geo.addLine(3, 2, 2)
gmsh.model.geo.addLine(3, 4, 3)
gmsh.model.geo.addLine(4, 1, 4)

gmsh.model.geo.addCurveLoop([4, 1, -2, 3], 1)

gmsh.model.geo.addPlaneSurface([1], 1)

# ここでやっとモデルが可視化出来る
gmsh.model.geo.synchronize()

gmsh.model.addPhysicalGroup(1, [1, 2, 4], 5)
gmsh.model.addPhysicalGroup(2, [1], name = "My surface")

gmsh.model.mesh.generate(2)

gmsh.write("t1.msh")

if '-nopopup' not in sys.argv:
    gmsh.fltk.run()

gmsh.finalize()