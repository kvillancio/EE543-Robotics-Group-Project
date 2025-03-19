function [T, optional] = robot_FK(theta)
% robot_FK calculates the forward kinematics for the project robot
%
% Inputs:
% theta : 5x1 vector of joint angles (rad)
%
% Outputs:
% T : table containing the direction cosine matrices of the orientations
%     of all links and points of interest

%
% Example:
% T = robot_FK([0; pi; 12; 0; pi/2]);
%

if nargin == 0
    theta = zeros(5,1);
    warning("no input, assuming zero configuration")
end

% l1 = 0; % frames 0 and 1 are coincident
l2 = 62.8;   % mm
l3 = 92.77;  % mm
l4 = 52.5;   % mm
l5 = 165.39; % mm

optional = table(l2,l3,l4,l5);

% alpha, a, d, theta
DH = [           0,  0,  l2, theta(1);...
      deg2rad(-90),  0,   0, theta(2)-deg2rad(67.17);...
                 0, l3,   0, theta(3)+deg2rad(67.17);...
                 0, l4,   0, deg2rad(90);...
       deg2rad(90),  0,   0, theta(4);...
                 0,  0,  l5, theta(5)];

% IMPORTANT NOTES
%   FRAME 2 is coincident with frame 1, with a constant offset to make the
%   z-axis be correctly aligned
%   FRAME 5 is coincident with frame 4, with a constant offset to make the
%   z-axis be correctly aligned
%
%



% Get number of frames
n = size(DH, 1);

T_i = cell(1, n);  % initialize transformation matrix cells

% convert each DH row to a Transformation matrix
for i = 1:n
    T_i{i} = DH2T(DH(i,:));
end

% Calculate transformation matrices with respect to base frame
T_0 = cell(1, n); 
T_0{1} = T_i{1};
for i = 2:n
    T_0{i} = T_0{i-1} * T_i{i};
end


T_0T1 = T_i{1};
T_1T2 = T_i{2};
T_2T3 = T_i{3};
T_3T4 = T_i{4};
T_4T5 = T_i{5};
T_5T6 = T_i{6};


% T_0T1 = T_0{1};
T_0T2 = T_0{2};
T_0T3 = T_0{3};
T_0T4 = T_0{4};
T_0T5 = T_0{5};
T_0T6 = T_0{6};


T = table(T_0T1, T_0T2, T_0T3, T_0T4, T_0T5, T_0T6, T_1T2, T_2T3, T_3T4, T_4T5, T_5T6);
end