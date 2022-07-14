import gmsh
import sys

gmsh.initialize()
gmsh.model.add("square_scatter")

gmsh.model.geo.addPoint(0, 0, 0, 0.001, 1)
gmsh.model.geo.addPoint(1, 0, 0, 0.01, 2)
gmsh.model.geo.addPoint(1, 1, 0, 0.1, 3)
gmsh.model.geo.addPoint(0, 1, 0, 1, 4)

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

# メッシュを生成するコマンド
gmsh.model.mesh.generate(2)

# change some option
gmsh.option.setColor("Geometry.Color.Points", 255, 165, 0)
# gmsh.model.mesh.setVisibility(3, 1)

gmsh.write("square_scatter.msh")

if '-nopopup' not in sys.argv:
    gmsh.fltk.run()

gmsh.finalize()