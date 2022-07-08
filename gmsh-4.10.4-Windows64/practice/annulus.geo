SetFactory("OpenCASCADE");

//---------------------------------------------------
// CRIAÇÃO DO POÇO 
//---------------------------------------------------

//Criação dos pontos para o poço
lc=1;
DP = 0.31;
Point(1) = {0,0,0,lc};
Point(2) = {DP/2,0,0,lc};
Point(3) = {0,DP/2,0,lc};
Point(4) = {-DP/2,0,0,lc};
Point(5) = {0,-DP/2,0,lc};

// Criando círculos a partir de arcos para o poço

Circle(1) = {2,1,3};
Circle(2) = {3,1,4};
Circle(3) = {4,1,5};
Circle(4) = {5,1,2};

// Criando superfície para a base do poço

Line Loop(5) = {1,2,3,4};
Plane Surface(6) = {5};

// Extrudando círculo para criar poço até o compirmento total topo (CTP)
CTP = 100;
Extrude {0,0,CTP} {
  Surface{6}; 
}

//---------------------------------------------------
// CRIAÇÃO DO ARROMBAMENTO 
//---------------------------------------------------
DA = 0.46; // Diâmetro do arrombamento
CA = 2; // Comprimento do arrombamento
PBA = 50;

Cylinder(2) = {0, 0, PBA, 0, 0, CA, DA/2, 2*Pi};
BooleanUnion{ Volume{2}; Delete; }{ Volume{1}; Delete; }


//---------------------------------------------------
// CRIAÇÃO DA COLUNA 
//---------------------------------------------------
DC = 0.25; //Diâmetro da coluna

Point(8) = {0,0,0,lc};
Point(9) = {DC/2,0,0,lc};
Point(10) = {0,DC/2,0,lc};
Point(11) = {-DC/2,0,0,lc};
Point(12) = {0,-DC/2,0,lc};


Circle(10) = {9, 1, 11};
Circle(11) = {11, 1, 9};

Extrude {0, 0, CTP} {
  Curve{10}; Curve{11}; 
}

//+
Curve Loop(12) = {14, 15};
//+
Plane Surface(10) = {12};
//+
Curve Loop(13) = {11, 10};
//+
Plane Surface(11) = {13};
//+
BooleanDifference{ Surface{6}; Delete; }{ Surface{10}; Delete; }
BooleanDifference{ Surface{7}; Delete; }{ Surface{11}; Delete; }
//+
Surface Loop(2) = {5, 7, 8, 9, 6, 4, 2, 1, 3};
//+
Volume(2) = {2};
