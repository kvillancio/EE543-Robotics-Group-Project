function robot_draw(gamma, fig, frameNum)
    % Draw the robot in 3D for given joint parameters
    % gamma: a vector of joint angles

    persistent p

    if nargin < 1
        gamma = zeros(1,5);
    end

    if nargin < 2
        fig = gcf;
        frameNum = 1;
        camlight;
    end

    % Compute the forward kinematics
    [T,r] = robot_FK(gamma);

    % Extract the positions of the frames
    num_joints = length(gamma);
    positions = zeros(3, num_joints);
    % positions(:, 1) = [0; 0; 0]; % Base frame position

    % Extract positions from the transformation matrices
    % for i = 1:num_joints
    %     T_matrix = T{:, i};
    % 
    %     positions(:, i) = T_matrix(1:3, 4);
    % end

    positions = r{:,:};
    positions = [zeros(3,1), positions];


    axis_scale = 1;
    if frameNum < 2
        % Set up figure
        fig = gcf;
        axis([-1, 1, -1, 1, -1.7, 1.7]*axis_scale);
        xlabel('X');
        ylabel('Y');
        zlabel('Z');
        title('Robot 3D Visualization');
        view([1,1,1]);
        axis equal;
        camlight left;

        % Plot the links
        hold on;
        grid on;
        p.links = gobjects(1, num_joints);
        for i = 1:num_joints
            p.links(i) = plot3([positions(1, i), positions(1, i+1)], ...
                               [positions(2, i), positions(2, i+1)], ...
                               [positions(3, i), positions(3, i+1)], 'b-', 'LineWidth', 2);
        end

        % Plot the frames
        p.frames = gobjects(1, num_joints + 1);
        for i = 1:num_joints + 1
            p.frames(i) = plot3(positions(1, i), positions(2, i), positions(3, i), 'ro', 'MarkerSize', 8, 'MarkerFaceColor', 'r');
        end
        hold off;
    else
        % Update the links
        for i = 1:num_joints
            set(p.links(i), 'XData', [positions(1, i), positions(1, i+1)], ...
                            'YData', [positions(2, i), positions(2, i+1)], ...
                            'ZData', [positions(3, i), positions(3, i+1)]);
        end

        % Update the frames
        for i = 1:num_joints + 1
            set(p.frames(i), 'XData', positions(1, i), ...
                             'YData', positions(2, i), ...
                             'ZData', positions(3, i));
        end
    end
    axis([-1, 1, -1, 1, -1.7, 1.7]*axis_scale);
end