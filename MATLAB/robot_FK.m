function [r, q, T] = robot_FK(theta)
% robot_FK calculates the forward kinematics for the project robot
%
% Inputs:
% theta : 5x1 vector of joint angles (rad)
%
% Outputs:
% r : table containing the position vectors for all links and points of
%     interest.
% T : table containing the direction cosine matricies of the orientations
%     of all links and points of interest
% q : table containing the unit quaternions specifying the orientations of
%     all links and points of interest
%
% Example:
% [r, q, T] = robot_FK([0; pi; 12; 0; pi/2], current_fig, frameNum);
%

if nargin == 0
    theta = zeros(5,1);
    warning("no input, assuming zero configuration")
end


l1 = .23;
l2 = .12;
l3 = .53;
l4 = .12;
l5 = .19;


DH = [          0, l1,  0, theta(1);...
      deg2rad(90), l2,  0, theta(2);...
                0, l3,  0, theta(3);...
      deg2rad(90),  0, l4, theta(4);...
                0,  0, l5,       0];

T_0T1 = DH2T(zeros(1,4), DH(1,1:4));
T_1T2 = DH2T(DH(1,1:4), DH(2,1:4));
T_2T3 = DH2T(DH(2,1:4), DH(3,1:4));
T_3T4 = DH2T(DH(3,1:4), DH(4,1:4));
T_4T5 = DH2T(DH(4,1:4), DH(5,1:4));

T_0T5 = T_0T1*T_1T2*T_2T3*T_3T4*T_4T5;



T = table(T_0T1, T_1T2, T_2T3, T_3T4, T_4T5, T_0T5);
end