import numpy as np
import math
import gmsh
import os
import sys

def genMesh(airfoilFile, structure=False):
    # print("test")

    # read airfoil file
    # skiprows=1 1行目を飛ばす
    ar = np.loadtxt(airfoilFile, skiprows=1)

    # removing duplicate end point
    # 最初の点と最後の点が一致していたら、最後の点が重複しているので除外する
    # ar.shape[0]はarの一次元目の要素の数を表している
    if np.max(np.abs(ar[0] - ar[(ar.shape[0] - 1)])) < 1e-6:
        ar = ar[:-1]

    # print(ar.shape)
    # print(ar.shape[0])
    # print(ar.shape[1])
    # for i in range(ar.shape[0]):
    #     print(f"{i} {ar[i][0]}")

    # calculate TE angle
    # 後縁 (trailing edge, T.E.)
    TE_angle_U=math.atan((ar[1][1]-ar[0][1])/(ar[1][0]-ar[0][0]))
    TE_angle_D=math.atan((ar[ar.shape[0]-1][1]-ar[0][1])/(ar[ar.shape[0]-1][0]-ar[0][0]))

    # initialize gmsh and add model
    gmsh.initialize()
    # デフォルトでは、物理グループが定義されている場合、Gmshは少なくとも1つの物理グループに属する要素のみを出力メッシュファイルにエクスポートすることに留意してください。Gmshがすべての要素を保存するように強制するには、以下のようにします。
    # gmsh.option.setNumber("General.Terminal", 1)を加えると，gmshが実行されているときのログを画面に出力することができる．デバッグのときなどはエラーを見つけるのに役に立つ
    gmsh.option.setNumber("General.Terminal", 1)
    gmsh.model.add("airfoil")

    # set point index
    TE_pointIndex = 1000
    # 前縁 (leading edge, L.E.)
    # argminはarの0次元の要素のおける最小値を記録するindexを返す
    # print(np.argmin(ar, axis=0)[0])
    LE_pointIndex = TE_pointIndex + np.argmin(ar, axis=0)[0]
    MAX_pointIndex = TE_pointIndex + ar.shape[0] - 1

    # add airfoil points
    pointIndex = TE_pointIndex
    for i in range(ar.shape[0]):
        if i != np.argmin(ar, axis=0)[0]:
            lc = 1e-2
        else:
            lc = 1e-3
        gmsh.model.geo.addPoint(ar[i][0], ar[i][1], 0, lc, pointIndex)
        pointIndex += 1

    # add points
    lc = 2
    R = 50
    gmsh.model.geo.addPoint(1.+R*math.cos(math.pi/2+TE_angle_U),R*math.sin(math.pi/2+TE_angle_U),0.,lc,1)
    gmsh.model.geo.addPoint(1.-R,0.,0.,lc,2)
    gmsh.model.geo.addPoint(1.+R*math.cos(math.pi/2+TE_angle_D),-R*math.sin(math.pi/2+TE_angle_D),0.,lc,3)
    gmsh.model.geo.addPoint(R,-R*math.sin(math.pi/2+TE_angle_D),0.,lc,4)
    gmsh.model.geo.addPoint(R,0.,0.,lc,5)
    gmsh.model.geo.addPoint(R,R*math.sin(math.pi/2+TE_angle_U),0.,lc,6)

    # 円弧を追加
    # gmsh.model.geo.addCircleArc(始点のタグ,原点のタグ,終点のタグ,Circleのタグ)
    # 直線を追加
    # gmsh.model.geo.addLine(始点のタグ,終点のタグ,Lineのタグ)
    # スプラインを追加
    # gmsh.model.geo.addSpline([点のタグのlist],Splineのタグ)

    # add Circle and Line
    # 外領域の定義
    gmsh.model.geo.addCircleArc(1, TE_pointIndex, 2, 1)
    gmsh.model.geo.addCircleArc(2, TE_pointIndex, 3, 2)
    gmsh.model.geo.addLine(3, 4, 3)
    gmsh.model.geo.addLine(4, 5, 4)
    gmsh.model.geo.addLine(5, 6, 5)
    gmsh.model.geo.addLine(6, 1, 6)
    gmsh.model.geo.addLine(TE_pointIndex,1,7)
    gmsh.model.geo.addLine(LE_pointIndex,2,8)
    gmsh.model.geo.addLine(TE_pointIndex,3,9)
    gmsh.model.geo.addLine(TE_pointIndex,5,10)

    # add airfoil spline (upper surface and under surface)
    # 曲線の追加
    list_index = [pointIndex for pointIndex in range(TE_pointIndex, LE_pointIndex + 1)]
    gmsh.model.geo.addSpline(list_index, 11)
    list_index = [pointIndex for pointIndex in range(LE_pointIndex, MAX_pointIndex + 1)]
    list_index.append(TE_pointIndex)
    gmsh.model.geo.addSpline(list_index, 12)

    # 
    if structure:
        # add CurveLoop and PlainSurface
        gmsh.model.geo.addCurveLoop([-11,7,1,-8], 1)
        gmsh.model.geo.addCurveLoop([8,2,-9,-12],2)
        gmsh.model.geo.addCurveLoop([9,3,4,-10], 3)
        gmsh.model.geo.addCurveLoop([10,5,6,-7], 4)

        gmsh.model.geo.addPlaneSurface([1],1)
        gmsh.model.geo.addPlaneSurface([2],2)
        gmsh.model.geo.addPlaneSurface([3],3)
        gmsh.model.geo.addPlaneSurface([4],4)
    else:
        #add CurveLoop and PlenSurface
        # 外側の閉曲線
        gmsh.model.geo.addCurveLoop([1,2,3,4,5,6], 1)
        # 内側の閉曲線
        gmsh.model.geo.addCurveLoop([11,12], 2)

        # addPlaneSurfaceメソッドの閉曲線のlistは，[一番外側の閉曲線，くり抜く閉曲線1，くり抜く閉曲線，・・・]と指定する
        # 上のやつ意味わからんからたぶんこう
        # addPlaneSurfaceメソッドの閉曲線のlistは，([一番外側の閉曲線，くり抜く閉曲線],定義する曲線の番号)と指定する
        gmsh.model.geo.addPlaneSurface([1,2],1)

        #set BoundaryLayer field
        gmsh.model.mesh.field.add("BoundaryLayer",1)
        gmsh.model.mesh.field.setNumbers(1,"EdgesList",[11,12])
        gmsh.model.mesh.field.setNumber(1,"Quads",1)
        gmsh.model.mesh.field.setNumber(1,"hwall_n",1e-3)
        gmsh.model.mesh.field.setNumber(1,"thickness",1e-2)
        gmsh.model.mesh.field.setAsBoundaryLayer(1)
    
        #extrude
        gmsh.model.geo.extrude([(2,1)],0.,0.,1.,[1],[1.],recombine=True)
        
        #add PhysicalGroup and set Name
        # これまでに作ったsurfaceやvolumeをphysicalgroupに追加する
        # gmsh.model.addPhysicalGroup(次元数,[タグのlist],PhysicalGroupのタグ)
        # extrudeメソッドで新たに追加されたSurfaceやVolumeのタグは自動的に振られるので，現時点ではどのSurfaceに何番のタグが振られているのかわからない
        gmsh.model.addPhysicalGroup(2,[1],1)    ;gmsh.model.setPhysicalName(2,1,"front")
        gmsh.model.addPhysicalGroup(2,[54],2)   ;gmsh.model.setPhysicalName(2,2,"back")
        gmsh.model.addPhysicalGroup(2,[25,29],3);gmsh.model.setPhysicalName(2,3,"inlet")
        gmsh.model.addPhysicalGroup(2,[37,41],4);gmsh.model.setPhysicalName(2,4,"exit")
        gmsh.model.addPhysicalGroup(2,[45],5)   ;gmsh.model.setPhysicalName(2,5,"top")
        gmsh.model.addPhysicalGroup(2,[33],6)   ;gmsh.model.setPhysicalName(2,6,"bottom")
        gmsh.model.addPhysicalGroup(2,[49,53],7);gmsh.model.setPhysicalName(2,7,"aerofoil")
        gmsh.model.addPhysicalGroup(3,[1],8)    ;gmsh.model.setPhysicalName(3,8,"internal")


    # ここでやっとモデルが可視化出来る
    gmsh.model.geo.synchronize()
    gmsh.model.mesh.generate(3)
    # 2次元メッシュの可視化オプションをONにするコマンド
    gmsh.option.setNumber("Mesh.SurfaceFaces", 1)
    # マウスのホイールをズームイン・ズームアウトを自然な向きに変えるコマンド
    gmsh.option.setNumber("General.MouseInvertZoom", 1)

    gmsh.write("airfoil.msh")    

    if '-nopopup' not in sys.argv:
        gmsh.fltk.run()

genMesh("NACA4412.dat")