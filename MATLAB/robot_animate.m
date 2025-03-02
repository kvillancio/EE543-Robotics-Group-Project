% filepath: /d:/School/UW/WINTER 2025/EE543_RoboticModels/FinalProject/EE543-Robotics-Group-Project/MATLAB/robot_animate.m

% Load necessary functions
addpath('robo_utils');


% initial joint angles
gamma0 = [0; 0; 0; 0; 0];
gammaf = [pi/2; pi/2; pi/2; pi/2; pi/2];
dot_gamma0 = [0; 0; 0; 0; 0];
dot_gammaf = [0; 0; 0; 0; 0];

t0 = 0; % initial time
tf = 5; % final time
dt = 0.01; % timestep

t = t0 : dt : tf;



% Generate cubic splines for each joint using cubicSpline
[a_0, a_1, a_2, a_3] = cubicSpline(t0, tf, gamma0, gammaf, dot_gamma0, dot_gammaf);
trajectories = a_0 + a_1.*t + a_2.*t.^2 + a_3.*t.^3;

% Create a figure for the animation
figure;
axis equal;
grid on;
hold on;

% Animate the robot movement
for k = 1:length(t)
    % Get the current joint angles
    current_angles = trajectories(:, k);
    
    % Compute the forward kinematics
    T = robot_FK(current_angles);
    
    % Draw the robot
    robot_draw(current_angles, gcf, k);
    
    % Pause to create animation effect
    pause(dt);
end

hold off;