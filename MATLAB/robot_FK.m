function [r, q, T] = robot_FK(gamma)
% robot_FK calculates the forward kinematics for the project robot
%
% Inputs:
% gamma : 5x1 vector of joint angles (rad)
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
% [r, q, T] = VP_6242_FK([0; pi; 12; 0; pi/2], current_fig, frameNum);
%
% required m-files:
%   rotx.m
%     DCM rotation about x axis
%   roty.m
%     DCM rotation about y axis
%   rotz.m
%     DCM rotation about z axis
%   qrotx.m
%     quaternion rotation about x axis
%   qroty.m
%     quaternion rotation about y axis
%   qrotz.m
%     quaternion rotation about z axis
%   rotq.m
%     convert quaternion to DCM
%   quatmult.m
%     multiply two quaternions together
%
% Subfunctions:
%   None
%
% required MAT-files:
%   None
%
% Author: Ian Adelman
% Email: IanAdelman@outlook.com
% Created: 04/08/2023
% Revised: revisedDate
%
% Ver#: 1.1 : revised_date
% Version Notes:
%   [[notes about changes since previous versions or important info]
%


%% initialzie robot geometry vectors
% initialize position vector table:
r = table();

% initialize position vectors in their respective frames
r.('IIr1') = [ 0     ; 0; 0.1550]*1000; % (m)
r.('11r2') = [ 0     ; 0; 0.1235]*1000; % (m)
r.('22r3') = [ 0     ; 0; 0.2100]*1000; % (m)
r.('33r4') = [-0.0750; 0; 0.0860]*1000; % (m)
r.('44rE') = [ 0.1250; 0; 0     ]*1000; % (m)


%% calculate quaternions
% initialzie quaternion table
q = table();

% calculate quaternions from current robot joint angles
q.('Iq1') = qrotz(gamma(1));
q.('1q2') = qroty(gamma(2));
q.('2q3') = qroty(gamma(3));
q.('3q4') = quatmult(qroty(-pi/2), qrotx(gamma(4)));
q.('4qE') = qrotx(gamma(5));


% transform quaternions into base frame
q.('Iq2') = quatmult(q.('Iq1'), q.('1q2'));
q.('Iq3') = quatmult(q.('Iq2'), q.('2q3'));
q.('Iq4') = quatmult(q.('Iq3'), q.('3q4'));
q.('IqE') = quatmult(q.('Iq4'), q.('4q5'));


%% calculate DCMs from quaternions
% initialize DCM table
T = table();

% calculate DCMs
T.('IT1') = rotq(q.('Iq1'));
T.('IT2') = rotq(q.('Iq2'));
T.('IT3') = rotq(q.('Iq3'));
T.('IT4') = rotq(q.('Iq4'));
T.('ITE') = rotq(q.('IqE'));


%% calculate position vectors in the base frame
r.('IIr2') = r.('IIr1') + T.('IT1')*r.('11r2');
r.('IIr3') = r.('IIr2') + T.('IT2')*r.('22r3');
r.('IIr4') = r.('IIr3') + T.('IT3')*r.('33r4');
r.('IIrE') = r.('IIr4') + T.('IT4')*r.('44rE');


end