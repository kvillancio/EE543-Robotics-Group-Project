function joint_angles = robot_IK(desired_pos, q0)
    % q0 is current state
    % desired_pos is the desired end effector position
    
    % Inverse kinematics using optimization
    
    % Define objective function that properly updates with each new q value
    objective = @(q) norm(robot_FK(q).("T_0T6")(1:3, 4) - desired_pos);
    
    % Optimization options
    options = optimoptions('fmincon', 'Display', 'iter', 'Algorithm', 'sqp');

    % Solve using fmincon (can also try lsqnonlin or fminunc)
    joint_angles = fmincon(objective, q0, [], [], [], [], [], [], [], options);
end
