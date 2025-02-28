function [HTM] = Hrot(axis, angle)
% Hrot(axis, angle) calculates the Homogeneous Rotation matrix from
% an input unit vector of direction, and a rotation angle theta.
%
% Inputs:
% axis: 3x1 unit axis of direction (length)
% angle: angle of rotation (radians)
%
% Outputs:
% DCM: 4x4 Homogeneous rotation matrix (radians, length)
%
% Example:
% axis = [1; 0; 0];
% angle = pi/2;
% [HTM] = Hrot(axis, angle)
% 
% Description:
% this function will return a homogeneous rotation matrix when given
% a unit vector of axis, and an angle of rotation in radians, I.E an 
% Euler rotation vector and angle.
%
% required m-files:
% % rot.m:
% % % for converting input angle to a DCM, for concattonating into the HTM
%
% Subfunctions:
% % None
%
% required MAT-files:
% % None
%
% Author: Ian Adelman
% Email: IanAdelman@outlook.com
% Created: 2022
% Revised: 03-18-2023
% Ver#: 2.0
% Version Notes:
% % added better function header, changed some variable names for readability.
%
% Revised: 11-14-2024
% Ver#: 3.0
% Version Notes:
% % Made variable names consistent across similar functions

HTM = [rot(axis, angle), zeros(3, 1); zeros(1, 3), 1];

end

