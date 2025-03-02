function plot_workspace(num_samples, joint_limits)
% plot_workspace plots the workspace of the robot's end effector position
% using a Monte Carlo simulation.
%
% Inputs:
% num_samples : Number of samples for the Monte Carlo simulation
% joint_limits : 5x2 matrix of joint limits [min, max] for each joint
%
% Example:
% plot_workspace(1000, [-pi, pi; -pi/2, pi/2; -pi, pi; -pi/2, pi/2; -pi, pi]);


if nargin == 0
    num_samples = 100000;
    joint_limits = [    0, pi;...
                    -pi/2, pi/2;...
                    -pi/2, pi/2;...
                    -pi/2, pi/2;...
                    -pi/2, pi/2];

end



% Initialize arrays to store end effector positions
x = zeros(num_samples, 1);
y = zeros(num_samples, 1);
z = zeros(num_samples, 1);

for i = 1:num_samples
    % Generate random joint angles within the specified limits
    theta = zeros(5, 1);
    for j = 1:5
        theta(j) = joint_limits(j, 1) + (joint_limits(j, 2) - joint_limits(j, 1)) * rand();
    end
    
    % Calculate forward kinematics
    T = robot_FK(theta);
    
    % Extract end effector position
    T_0T5 = T.T_0T5;
    x(i) = T_0T5(1, 4);
    y(i) = T_0T5(2, 4);
    z(i) = T_0T5(3, 4);
end

% Plot the workspace
figure;
scatter3(x, y, z, 'filled', 'MarkerFaceAlpha', 0.1);
axis("equal")
xlabel('X');
ylabel('Y');
zlabel('Z');
title('Robot Workspace');
grid on;
end