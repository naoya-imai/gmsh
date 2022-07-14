import gmsh
import math
import os
import sys


def createGeometryAndMesh():
  gmsh.initialize()
  # すべてのモデルをクリアし、リメッシュしたいSTLメッシュを呼び出す
  gmsh.clear()
  # ここからはファイルのpathの設定
  path = os.path.dirname(os.path.abspath(__file__))
  print(path)
  # 実際に呼び出しているのはここ
  # ファイルのパスを記述している
  # gmsh.merge(os.path.join(path, os.pardir, "tutorials", "t13_data.stl"))
  gmsh.merge(os.path.join(path, os.pardir, "cylinder.stl"))


  # ます元の表面を鋭い幾何学的特徴に沿って分割することで、表面を色付けする
  # これによって新しい離散的なsurfaceが作成される
  # パラメータのセッティングを下のgmsh.onlab.setでしている
  angle = gmsh.onelab.getNumber('Parameters/Angle for surface detection')[0]
  print(f"angle is {angle}")

  forceParametrizablePatches = gmsh.onelab.getNumber(
      'Parameters/Create surfaces guaranteed to be parametrizable')[0]
  print(f"forceParametrizablePatches is {forceParametrizablePatches}")

  includeBoundary = True

  curveAngle = 180

  gmsh.model.mesh.classifySurfaces(angle * math.pi / 180., includeBoundary, forceParametrizablePatches, curveAngle * math.pi / 180.)

  gmsh.model.mesh.createGeometry()

  gmsh.write("cylinder.msh")
  if '-nopopup' not in sys.argv:
      gmsh.fltk.run()

# Create ONELAB parameters with remeshing options:
gmsh.onelab.set("""[
  {
    "type":"number",
    "name":"Parameters/Angle for surface detection",
    "values":[40],
    "min":20,
    "max":120,
    "step":1
  },
  {
    "type":"number",
    "name":"Parameters/Create surfaces guaranteed to be parametrizable",
    "values":[0],
    "choices":[0, 1]
  },
  {
    "type":"number",
    "name":"Parameters/Apply funny mesh size field?",
    "values":[0],
    "choices":[0, 1]
  }
]""")

createGeometryAndMesh()

gmsh.finalize()