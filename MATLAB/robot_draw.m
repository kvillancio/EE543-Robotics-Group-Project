function [fig] = robot_draw(gamma, fig, frameNum)
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

% clear axes
cla
view(3)

% Compute the forward kinematics
T = robot_FK(gamma);

r_00r1 = T.("T_0T1")(1:3,4);
r_00r2 = T.("T_0T1")(1:3,4);
r_00r3 = T.("T_0T2")(1:3,4);
r_00r4 = T.("T_0T3")(1:3,4);
r_00r5 = T.("T_0T4")(1:3,4);
r_00r6 = T.("T_0T6")(1:3,4);


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

% Draw coordinate frames at each joint
% Set the length of coordinate frame axes for visualization
axis_length = 20;

% Draw base frame (frame 0)
line('Xdata', [0, axis_length], 'Ydata', [0, 0], 'Zdata', [0, 0], 'Color', 'r', 'LineWidth', 2);
line('Xdata', [0, 0], 'Ydata', [0, axis_length], 'Zdata', [0, 0], 'Color', 'g', 'LineWidth', 2);
line('Xdata', [0, 0], 'Ydata', [0, 0], 'Zdata', [0, axis_length], 'Color', 'b', 'LineWidth', 2);

% Draw frames for each joint
% Frame 1
drawFrame(T.("T_0T1"), axis_length);
% Frame 2
drawFrame(T.("T_0T2"), axis_length);
% Frame 3
drawFrame(T.("T_0T3"), axis_length);
% Frame Constant rotation 3 -> 4
drawFrame(T.("T_0T4"), axis_length);
% Frame 4
drawFrame(T.("T_0T5"), axis_length);
% Frame 5
drawFrame(T.("T_0T6"), axis_length);

figure(fig)
% view(3)
grid on
axis equal
xlabel('X');ylabel('Y');zlabel('Z');
axis([-1,1, -1,1, -.3,1]*200);
end

% Helper function to draw a coordinate frame at a specific transformation
function drawFrame(T, length)
    % Extract position and rotation from transformation matrix
    pos = T(1:3,4);
    
    % X axis (red)
    line('Xdata', [pos(1), pos(1) + length*T(1,1)],...
         'Ydata', [pos(2), pos(2) + length*T(2,1)],...
         'Zdata', [pos(3), pos(3) + length*T(3,1)],...
         'Color', 'r', 'LineWidth', 2);
    
    % Y axis (green)
    line('Xdata', [pos(1), pos(1) + length*T(1,2)],...
         'Ydata', [pos(2), pos(2) + length*T(2,2)],...
         'Zdata', [pos(3), pos(3) + length*T(3,2)],...
         'Color', 'g', 'LineWidth', 2);
    
    % Z axis (blue)
    line('Xdata', [pos(1), pos(1) + length*T(1,3)],...
         'Ydata', [pos(2), pos(2) + length*T(2,3)],...
         'Zdata', [pos(3), pos(3) + length*T(3,3)],...
         'Color', 'b', 'LineWidth', 2);
end