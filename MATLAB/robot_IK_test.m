
clear
clc


input_joint_angles = ones(5,1)*pi/2;
T = robot_FK(input_joint_angles);
T_0T6 = T.("T_0T6");
pos_desired = T_0T6(1:3,4);


q0 = zeros(5,1);



q = robot_IK(pos_desired, q0)




q =

  -83.2522
   16.4818
   84.0491
         0
         0