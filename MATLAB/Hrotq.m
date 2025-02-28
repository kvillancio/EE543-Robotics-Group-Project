function [HTM] = Hrotq(q)
% Hrotq(q) calculates the Homogeneous Rotation Matrix (HTM) from an
% input unit quaternion q
%
% Inputs:
% q: 4x1 unit quaternion (radians)
%
% Outputs:
% HTM: 4x4 Homogeneous Rotation Matrix (radians, length)
%
% Example:
% q = [0; phi; theta; psi];
% HTM = Hrotq(q);
% 
% Description:
% with an input unit quaternion q, this function will return a 4x4 Homogeneous
% Transformation Matrix HTM, with zeros as the translation component,
% i.e. a Homogeneous Rotation Matrix.
%
% required m-files:
% % rotq.m:
% % % for converting unit quaternion q into a DCM
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
% % updated function header and changed variable names for increased readability
%

HTM = [rotq(q), zeros(3,1); zeros(1,3), 1];

end