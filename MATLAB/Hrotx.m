function [HTM] = Hrotx(phi)
% Hrotx(phi) converts a rotation angle (radians) into a
% a Homogeneous Rotation Matrix HTM, with rotation about the
% X axis.
%
% Inputs:
% phi: rotation angle (radians)
%
% Outputs:
% HTM: Homogeneous Rotation Matrix (radians)
%
% Example:
% phi = pi/2;
% [HTM] = Hrotx(phi)
% 
% Description:
% with an angular input in radians, this function will calculate and return
% a 4x4 Homogeneous Transformation Matrix, with zeros for the translation component,
% i.e. a Homogeneous Rotation Matrix. The rotation axis is pre-selected as the X axis,
% given by the right hand rule.
%
% required m-files:
% % rotx.m:
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
% % Updated function header and variable names for increased readability
%
% Revised: 11-14-2024
% Ver#: 3.0
% Version Notes:
% % Made variable names consistent across similar functions

HTM = [rotx(phi), zeros(3,1); zeros(1,3), 1];

end