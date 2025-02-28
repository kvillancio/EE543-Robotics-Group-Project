function [HTM] = Htrans(vector)
% Htrans(vector) converts a 3x1 translational vector into a
% Homogeneous Translation Matrix
%
% Inputs:
% vector: 3x1 position vector (length)
%
% Outputs:
% HTM: Homogeneous Translation Matrix (length)
%
% Example:
% r = [1; 1; 1];
% [HTM] = Htrans(r);
% 
% Description:
% with an input 3x1 position vector, this function will return a Homogeneous
% Transformation Matrix HTM, with zeros for the rotational component, i.e. 
% a Homogeneous Translation Matrix.
%
% required m-files:
% % None
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
%
% Revised: 03-18-2023
% Ver#: 2.0
% Version Notes:
% % Updated function header and variable names for increased readability
%
% Revised 11-14-2024
% Ver#: 3.0
% Version Notes:
% % Suppressed output, made variable names consistent with similar
% % functions
%

% calculate HTM
HTM = [eye(3,3), vector; zeros(1,3), 1];

end