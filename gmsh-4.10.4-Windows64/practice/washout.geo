SetFactory("OpenCASCADE");
Mesh.CharacteristicLengthFromCurvature = 1;
Mesh.MinimumElementsPerTwoPi = 10;


CTP = 100; // Total well lenght

//---------------------------------------------------
// Creation of Well - First part before washout
//---------------------------------------------------
// DA>>DP;
// DP>>DC;
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
// Well data (meters) - bottom part (before washout)
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

DP = 0.31; // Well diameter before wahsout
CPA = 50; // Well lenght before washout (well base to beginning of washout)

//+++++++++++++++++++++++++++++++++++++
// Washout data (meter)
//+++++++++++++++++++++++++++++++++++++

DA = 0.46; // Diameter
CA = 2; // Lenght

Circle(1) = {0, 0, 0, DP/2, 0, 2*Pi};
Curve Loop(1) = {1};
Plane Surface(1) = {1};
Extrude {0, 0, CPA} {
  Curve{1}; 
}
Curve Loop(3) = {3};
Plane Surface(3) = {3};

//---------------------------------------------------
// Creation of washout
//---------------------------------------------------
Circle(4) = {0, 0, CPA, DA/2, 0, 2*Pi};
Curve Loop(4) = {4};
Plane Surface(4) = {4};
BooleanDifference{ Surface{4}; Delete; }{ Surface{3}; Delete; }
Extrude {0, 0, CA} {
  Curve{4}; 
}
Curve Loop(4) = {6};
Plane Surface(6) = {4};


//---------------------------------------------------
// Creation of well - Second part after washout
//---------------------------------------------------
Circle(7) = {0, 0, CA+CPA, DP/2, 0, 2*Pi};
Curve Loop(5) = {7};
Plane Surface(7) = {5};
BooleanDifference{ Surface{6}; Delete; }{ Surface{7}; Delete; }
Extrude {0, 0, CTP-(CA+CPA)} {
  Curve{7}; 
}
Curve Loop(5) = {9};
Plane Surface(8) = {5};

//-----------------------------------------
// Creation of Casing
//-----------------------------------------

//+++++++++++++++++++++++++++++++++++++
// Casing data (meters)
//+++++++++++++++++++++++++++++++++++++

DC = 0.25; // Casing diameter
STDOFF = 0.05; // Casing eccentricity -- x direction

//+++++++++++++++++++++++++++++++++++++++++++++++++

Circle(10) = {((DP/2)-(DC/2))*(1-STDOFF), 0, 0, DC/2, 0, 2*Pi};
Curve Loop(9) = {10};
Plane Surface(12) = {9};
BooleanDifference{ Surface{1}; Delete; }{ Surface{12}; Delete; }
Extrude {0, 0, CTP} {
  Curve{10}; 
}
Curve Loop(10) = {12};
Plane Surface(13) = {10};
BooleanDifference{ Surface{8}; Delete; }{ Surface{13}; Delete; }
Surface Loop(1) = {9, 8, 7, 6, 5, 4, 2, 1};
Volume(1) = {1};


//Boundary Conditons

Physical Surface("Inlet", 1) = {1}; // well bottom
Physical Surface("Outlet", 2) = {8}; // well top
Physical Surface("whashout", 3) = {6, 5, 4};// washout wall
Physical Surface("beforewash", 4) = {2};  // wall bottom before washout
Physical Surface("afterwash", 5) = {7}; // wall top after washout
Physical Surface("casing", 6) = {9}; // wall casing
Physical Volume("wellvolume", 7) = {1}; // well volume

//Coherence;