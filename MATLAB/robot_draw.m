function robot_draw(gamma, fig, frameNum)
% Draw the robot in 3D for given joint angles with coordinate frames
% gamma: a vector of joint angles

persistent p

if nargin < 1
    gamma = zeros(1,5);
end

if nargin < 2
    fig = figure();
    frameNum = 1;
    camlight;
end

% Compute the forward kinematics
T = robot_FK(gamma);

r_00r1 = T.("T_0T1")(1:3,4);
r_00r2 = T.("T_0T1")(1:3,4);
r_00r3 = T.("T_0T2")(1:3,4);
r_00r4 = T.("T_0T3")(1:3,4);
r_00r5 = T.("T_0T4")(1:3,4);
r_00r6 = T.("T_0T5")(1:3,4);


line01 = line('Xdata', [0, r_00r1(1)],...
              'Ydata', [0, r_00r1(2)],...
              'Zdata', [0, r_00r1(3)],...
              'color', 'red');

line12 = line('Xdata', [r_00r1(1), r_00r2(1)],...
              'Ydata', [r_00r1(2), r_00r2(2)],...
              'Zdata', [r_00r1(3), r_00r2(3)],...
              'color', 'black');

line23 = line('Xdata', [r_00r2(1), r_00r3(1)],...
              'Ydata', [r_00r2(2), r_00r3(2)],...
              'Zdata', [r_00r2(3), r_00r3(3)],...
              'color', 'red');

line34 = line('Xdata', [r_00r3(1), r_00r4(1)],...
              'Ydata', [r_00r3(2), r_00r4(2)],...
              'Zdata', [r_00r3(3), r_00r4(3)],...
              'color', 'black');

line45 = line('Xdata', [r_00r4(1), r_00r5(1)],...
              'Ydata', [r_00r4(2), r_00r5(2)],...
              'Zdata', [r_00r4(3), r_00r5(3)],...
              'color', 'red');

line56 = line('Xdata', [r_00r5(1), r_00r6(1)],...
              'Ydata', [r_00r5(2), r_00r6(2)],...
              'Zdata', [r_00r5(3), r_00r6(3)],...
              'color', 'black');





figure(fig)
view(3)
grid on
axis equal
xlabel('X');ylabel('Y');zlabel('Z');
axis([-1,1, -1,1, -1,1]*3);