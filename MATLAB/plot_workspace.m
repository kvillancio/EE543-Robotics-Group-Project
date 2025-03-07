function plot_workspace(num_samples, joint_limits, test_points, threshold)
% plot_workspace plots the workspace of the robot's end effector position
% using a Monte Carlo simulation.
%
% Inputs:
% num_samples : Number of samples for the Monte Carlo simulation
% joint_limits : 5x2 matrix of joint limits [min, max] for each joint
% test_points : Optional - Nx3 matrix of test points to check if they are within the workspace
% threshold : Optional - Distance threshold to determine if a point is reachable (default: 0.1)
%
% Example:
% plot_workspace(1000, [-pi, pi; -pi/2, pi/2; -pi, pi; -pi/2, pi/2; -pi, pi]);
% plot_workspace(1000, [-pi, pi; -pi/2, pi/2; -pi, pi; -pi/2, pi/2; -pi, pi], [0.2 0.3 0.1; 0.5 0 0.2; 0.1 -0.4 0.3]);
% plot_workspace(1000, [-pi, pi; -pi/2, pi/2; -pi, pi; -pi/2, pi/2; -pi, pi], [0.2 0.3 0.1; 0.5 0 0.2], 0.05);

if nargin < 4
    % Default threshold - increased from 0.02 to 0.1
    threshold = 0.1; 
end

if nargin < 3
    % Generate some random test points within a reasonable range
    num_test_points = 10;
    test_points = 2 * rand(num_test_points, 3) - 1; % Random points in the range [-1, 1]
end

if nargin < 2 || isempty(joint_limits)
    num_samples = 10000;
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
h_workspace = scatter3(x, y, z, 'filled', 'MarkerFaceAlpha', 0.1);
axis("equal")
xlabel('X');
ylabel('Y');
zlabel('Z');
title('Robot Workspace');
grid on;

% Check if test points are within the workspace
if ~isempty(test_points)
    hold on;
    
    % For each test point, check if it's reachable
    reachable = zeros(size(test_points, 1), 1);
    h_sphere = [];
    for i = 1:size(test_points, 1)
        % Calculate minimum distance to any point in the workspace
        point = test_points(i, :);
        distances = sqrt((x - point(1)).^2 + (y - point(2)).^2 + (z - point(3)).^2);
        min_distance = min(distances);
        
        % If the minimum distance is less than threshold, consider it reachable
        reachable(i) = (min_distance < threshold);
        
        % Visualize the threshold as a small sphere
        [sx, sy, sz] = sphere(20);
        h = surf(sx*threshold + point(1), sy*threshold + point(2), sz*threshold + point(3), ...
             'FaceAlpha', 0.1, 'EdgeColor', 'none', 'FaceColor', [0.7 0.7 0.7]);
        if isempty(h_sphere)
            h_sphere = h;  % Save only the first sphere handle for the legend
        end
    end
    
    % Plot reachable test points in green
    h_reachable = [];
    reachable_points = test_points(reachable == 1, :);
    if ~isempty(reachable_points)
        h_reachable = scatter3(reachable_points(:, 1), reachable_points(:, 2), reachable_points(:, 3), 100, 'g', 'filled', 'MarkerEdgeColor', 'k');
    end
    
    % Plot unreachable test points in red
    h_unreachable = [];
    unreachable_points = test_points(reachable == 0, :);
    if ~isempty(unreachable_points)
        h_unreachable = scatter3(unreachable_points(:, 1), unreachable_points(:, 2), unreachable_points(:, 3), 100, 'r', 'filled', 'MarkerEdgeColor', 'k');
    end
    
    % Create legend with the appropriate handles
    legend_handles = [h_workspace, h_sphere];
    legend_labels = {'Workspace', 'Threshold Sphere'};
    
    if ~isempty(h_reachable)
        legend_handles = [legend_handles, h_reachable];
        legend_labels = [legend_labels, {'Reachable Points'}];
    end
    
    if ~isempty(h_unreachable)
        legend_handles = [legend_handles, h_unreachable];
        legend_labels = [legend_labels, {'Unreachable Points'}];
    end
    
    legend(legend_handles, legend_labels, 'Location', 'best');
    
    % Print results
    disp('Test points reachability:');
    disp(['Using threshold: ' num2str(threshold)]);
    for i = 1:size(test_points, 1)
        if reachable(i)
            status = 'REACHABLE';
        else
            status = 'UNREACHABLE';
        end
        fprintf('Point [%.2f, %.2f, %.2f]: %s\n', test_points(i,1), test_points(i,2), test_points(i,3), status);
    end
end
end