
Point(1) = {0,0,0,1};
Point(2) = {1,0,0,1};
Point(3) = {1,1,0,1};
Point(4) = {0,1,0,1};
Line(1) = {2,3};
Line(2) = {3,4};
Line(3) = {4,1};
Line(4) = {1,2};
Line Loop(5) = {2,3,4,1};
Plane Surface(6) = {5};
Extrude Surface {6, {0,0,1}};
Surface Loop(29) = {15,6,19,23,27,28};
Volume(30) = {29};

/*Transfinite Line {9,10,11,8,13,18,22,4,1,3,2,14} = 10;
Transfinite Surface {19} = {1,10,6,4};
Transfinite Surface {23} = {14,2,1,10};
Transfinite Surface {27} = {14,2,3,5};
Transfinite Surface {15} = {3,5,6,4};
Transfinite Surface {28} = {6,5,14,10};
Transfinite Surface {6} = {2,3,4,1};
Transfinite Volume{30} = {10,14,5,6,1,2,3,4};*/
//Recombine Surface {15,28,19,6,27,23};

//Physical Volume(50) = {30};
Physical Surface(101) = {19};
Physical Surface(102) = {27};
Physical Surface(103) = {28, 15, 6, 23};
Physical Volume(50) = {1};
