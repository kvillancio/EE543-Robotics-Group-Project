
clear
clc


input_joint_angles = ones(5,1)*.1;
T = robot_FK(input_joint_angles);
T_0T6 = T.("T_0T6");
pos_desired = T_0T6(1:3,4);


q0 = zeros(5,1);



q = robot_IK(pos_desired, q0)

