function position = robot_get_position(joint_angles)
    % Get the current end-effector position from joint angles
    % This simplifies the structure extraction that was causing errors
    
    % Calculate forward kinematics
    T = robot_FK(joint_angles);
    
    % Extract the position (first 3 elements of 4th column)
    position = T.T_0T6(1:3, 4);
end