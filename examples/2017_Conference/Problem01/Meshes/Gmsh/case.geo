mesh_size = 9; // number of vertices on each direction

Point(1) = {0,0,0,0.1};
Point(2) = {2,0,0,0.1};
Point(3) = {2,1,0,0.1};
Point(4) = {0,1,0,0.1};
Point(5) = {0,0,1,0.1};
Point(6) = {2,0,1,0.1};
Point(7) = {2,1,1,0.1};
Point(8) = {0,1,1,0.1};
Line(1) = {2,3};
Line(2) = {3,4};
Line(3) = {4,1};
Line(4) = {1,2};
Line(5) = {5,6};
Line(6) = {6,7};
Line(7) = {7,8};
Line(8) = {8,5};
Line(9) = {8, 4};
Line(10) = {5, 1};
Line(11) = {6, 2};
Line(12) = {7, 3};

Line Loop(13) = {5, 6, 7, 8};
Line Loop(14) = {4, 1, 2, 3};
Line Loop(17) = {10, -3, -9, 8};
Line Loop(19) = {11, 1, -12, -6};
Line Loop(21) = {2, -9, -7, 12};
Line Loop(23) = {4, -11, -5, 10};
Surface Loop(25) = {22, 15, 24, 20, 16, 18};

Plane Surface(15) = {14};
Plane Surface(16) = {13};
Plane Surface(18) = {17};
Plane Surface(20) = {19};
Plane Surface(22) = {21};
Plane Surface(24) = {23};

Volume(26) = {25};

Transfinite Line {7, 5, 6, 8, 11, 10, 12, 9, 4, 1, 2, 3} = mesh_size;
Transfinite Surface {16};
Transfinite Surface {20};
Transfinite Surface {15};
Transfinite Surface {18};
Transfinite Surface {22};
Transfinite Surface {24};
Transfinite Volume{26};
Recombine Surface {16, 24, 22, 20, 18, 15};

Physical Volume(50) = {26};
Physical Surface(101) = {18};
Physical Surface(102) = {20};
Physical Surface(103) = {24, 16, 22, 15};
