function joint_angles = robot_IK(desired_pos, q0, display_on)
    % q0 is current state
    % desired_pos is the desired end effector position

    if nargin < 3
        display_on = true;
    end
    
    % Inverse kinematics using optimization
    
    % Define objective function that properly updates with each new q value
    objective = @(q) norm(robot_FK(q).("T_0T6")(1:3, 4) - desired_pos);
    
    % Optimization options
    if display_on
        options = optimoptions('fmincon', 'Display', 'iter', 'Algorithm', 'sqp');
    else
        % Turn off display if user doesnt want it
        options = optimoptions('fmincon', 'Display', 'off', 'Algorithm', 'sqp');
    end

    % Solve using fmincon (can also try lsqnonlin or fminunc)
    joint_angles = fmincon(objective, q0, [], [], [], [], [], [], [], options);
end
