

theta = [pi/2; pi/2; pi/2; pi/2];
l1 = .23;
l2 = .42;
l3 = .12;
l4 = .31;
l5 = .1;

DH = [          0, l1,  0, theta(1);...
      deg2rad(90), l2,  0, theta(2);...
                0, l3,  0, theta(3);...
      deg2rad(90),  0, l4, theta(4);...
                0,  0, l5,       0];


T_0T1 = DH2T(zeros(1,4), DH(1,1:4))