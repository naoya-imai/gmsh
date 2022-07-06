import numpy as np
import math
import gmsh
import os

def genMesh(airfoilFile,structure=True):
    print("test")
    
    #read airfoil file
    ar = np.loadtxt(airfoilFile, skiprows=1)

    #removing duplicate end point
    if np.max(np.abs(ar[0] - ar[(ar.shape[0]-1)]))<1e-6:
        ar = ar[:-1]
    
    #calculate TE angle
    TE_angle_U=math.atan((ar[1][1]-ar[0][1])/(ar[1][0]-ar[0][0]))
    TE_angle_D=math.atan((ar[ar.shape[0]-1][1]-ar[0][1])/(ar[ar.shape[0]-1][0]-ar[0][0]))
    
    #initialize gmsh and add model
    gmsh.initialize()
    gmsh.option.setNumber("General.Terminal", 1)
    gmsh.model.add("airfoil")
    
    #set point index
    TE_pointIndex = 1000
    LE_pointIndex = TE_pointIndex+np.argmin(ar,axis=0)[0]
    MAX_pointIndex = TE_pointIndex+ar.shape[0]-1

    #add airfoil points
    pointIndex = TE_pointIndex
    for n in range(ar.shape[0]):
        lc = 1e-2 if n != np.argmin(ar,axis=0)[0] else 1e-3
        gmsh.model.geo.addPoint(ar[n][0],ar[n][1],0.,lc,pointIndex)
        pointIndex += 1

    #add poiuts
    lc = 2.
    R=50.
    gmsh.model.geo.addPoint(1.+R*math.cos(math.pi/2+TE_angle_U),R*math.sin(math.pi/2+TE_angle_U),0.,lc,1)
    gmsh.model.geo.addPoint(1.-R,0.,0.,lc,2)
    gmsh.model.geo.addPoint(1.+R*math.cos(math.pi/2+TE_angle_D),-R*math.sin(math.pi/2+TE_angle_D),0.,lc,3)
    gmsh.model.geo.addPoint(R,-R*math.sin(math.pi/2+TE_angle_D),0.,lc,4)
    gmsh.model.geo.addPoint(R,0.,0.,lc,5)
    gmsh.model.geo.addPoint(R,R*math.sin(math.pi/2+TE_angle_U),0.,lc,6)

    #add Circle and Line
    gmsh.model.geo.addCircleArc(1,TE_pointIndex,2,1)
    gmsh.model.geo.addCircleArc(2,TE_pointIndex,3,2)
    gmsh.model.geo.addLine(3,4,3)
    gmsh.model.geo.addLine(4,5,4)
    gmsh.model.geo.addLine(5,6,5)
    gmsh.model.geo.addLine(6,1,6)
    gmsh.model.geo.addLine(TE_pointIndex,1,7)
    gmsh.model.geo.addLine(LE_pointIndex,2,8)
    gmsh.model.geo.addLine(TE_pointIndex,3,9)
    gmsh.model.geo.addLine(TE_pointIndex,5,10)

    #add airfoil spline (upper surface and under surface)
    list_index=[pointIndex for pointIndex in range(TE_pointIndex,LE_pointIndex+1)]
    gmsh.model.geo.addSpline(list_index,11)
    list_index=[pointIndex for pointIndex in range(LE_pointIndex,MAX_pointIndex+1)]
    list_index.append(TE_pointIndex)
    gmsh.model.geo.addSpline(list_index,12)

    if structure:
        #add CurveLoop and PlenSurface
        gmsh.model.geo.addCurveLoop([-11,7,1,-8], 1)
        gmsh.model.geo.addCurveLoop([8,2,-9,-12], 2)
        gmsh.model.geo.addCurveLoop([9,3,4,-10], 3)
        gmsh.model.geo.addCurveLoop([10,5,6,-7], 4)

        gmsh.model.geo.addPlaneSurface([1],1)
        gmsh.model.geo.addPlaneSurface([2],2)
        gmsh.model.geo.addPlaneSurface([3],3)
        gmsh.model.geo.addPlaneSurface([4],4)
        
        #set TransfiniteCurve
        NH=128;NW=128;NA=128
        list_index=[1,2]
        for CurveIndex in [1,2]:
            gmsh.model.geo.mesh.setTransfiniteCurve(CurveIndex,NA)
        prog=1.05
        for (CurveIndex,direction) in zip([4,5,7,9],[False,True,True,True]):
            prog_tmp = prog if direction else -prog
            gmsh.model.geo.mesh.setTransfiniteCurve(CurveIndex,NH,meshType="Progression",coef=prog_tmp)
        prog=1.04
        CurveIndex=10
        gmsh.model.geo.mesh.setTransfiniteCurve(CurveIndex,NW,meshType="Progression",coef=prog_tmp)
        for CurveIndex in [3,6]:
            gmsh.model.geo.mesh.setTransfiniteCurve(CurveIndex,NW)
        prog=1.07
        CurveIndex=8
        gmsh.model.geo.mesh.setTransfiniteCurve(CurveIndex,NW,meshType="Progression",coef=prog)
        prog=1.03
        for (CurveIndex,direction) in zip([11,12],[False,True]):
            prog_tmp = prog if direction else -prog
            gmsh.model.geo.mesh.setTransfiniteCurve(CurveIndex,NA,meshType="Progression",coef=prog_tmp)
        
        for SurfaceIndex in [1,2,3,4]:
            gmsh.model.geo.mesh.setTransfiniteSurface(SurfaceIndex)
            gmsh.model.geo.mesh.setRecombine(2,SurfaceIndex)
            
            #extrude
            gmsh.model.geo.extrude([(2,SurfaceIndex)],0.,0.,1.,[1],[1.],recombine=True)
        
        #add PhysicalGroup and set Name
        gmsh.model.addPhysicalGroup(2,[1,2,3,4],1)      ;gmsh.model.setPhysicalName(2,1,"front")
        gmsh.model.addPhysicalGroup(2,[34,56,78,100],2) ;gmsh.model.setPhysicalName(2,2,"back")
        gmsh.model.addPhysicalGroup(2,[29,47],3)        ;gmsh.model.setPhysicalName(2,3,"inlet")
        gmsh.model.addPhysicalGroup(2,[73,91],4)        ;gmsh.model.setPhysicalName(2,4,"exit")
        gmsh.model.addPhysicalGroup(2,[95],5)           ;gmsh.model.setPhysicalName(2,5,"top")
        gmsh.model.addPhysicalGroup(2,[69],6)           ;gmsh.model.setPhysicalName(2,6,"bottom")
        gmsh.model.addPhysicalGroup(2,[21,55],7)        ;gmsh.model.setPhysicalName(2,7,"aerofoil")
        gmsh.model.addPhysicalGroup(3,[1,2,3,4],8)      ;gmsh.model.setPhysicalName(3,8,"internal")
    else:
        #add CurveLoop and PlenSurface
        gmsh.model.geo.addCurveLoop([1,2,3,4,5,6], 1)
        gmsh.model.geo.addCurveLoop([11,12], 2)

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
        gmsh.model.addPhysicalGroup(2,[1],1)    ;gmsh.model.setPhysicalName(2,1,"front")
        gmsh.model.addPhysicalGroup(2,[54],2)   ;gmsh.model.setPhysicalName(2,2,"back")
        gmsh.model.addPhysicalGroup(2,[25,29],3);gmsh.model.setPhysicalName(2,3,"inlet")
        gmsh.model.addPhysicalGroup(2,[37,41],4);gmsh.model.setPhysicalName(2,4,"exit")
        gmsh.model.addPhysicalGroup(2,[45],5)   ;gmsh.model.setPhysicalName(2,5,"top")
        gmsh.model.addPhysicalGroup(2,[33],6)   ;gmsh.model.setPhysicalName(2,6,"bottom")
        gmsh.model.addPhysicalGroup(2,[49,53],7);gmsh.model.setPhysicalName(2,7,"aerofoil")
        gmsh.model.addPhysicalGroup(3,[1],8)    ;gmsh.model.setPhysicalName(3,8,"internal")
    
    #generate mesh and finalize gmsh
    gmsh.model.geo.synchronize()
    gmsh.model.mesh.generate(3)
    gmsh.write('airfoil.msh')
    gmsh.finalize()
    
    print("gmsh > done!")

    if os.system("gmshToFoam airfoil.msh > /dev/null") != 0:
        print("error during conversion to OpenFoam mesh!")
        return(-1)

    print("gmshToFOAM > done!")

    #set boundary
    with open("constant/polyMesh/boundary", "rt") as inFile:
        with open("constant/polyMesh/boundaryTemp", "wt") as outFile:
            inBlock = False
            inAerofoil = False
            for line in inFile:
                if "front" in line or "back" in line:
                    inBlock = True
                elif "aerofoil" in line:
                    inAerofoil = True
                if inBlock and "type" in line:
                    line = line.replace("patch", "empty")
                    inBlock = False
                if inAerofoil and "type" in line:
                    line = line.replace("patch", "wall")
                    inAerofoil = False
                outFile.write(line)
    os.rename("constant/polyMesh/boundaryTemp","constant/polyMesh/boundary")

    return(0)


genMesh("NACA4412.dat")