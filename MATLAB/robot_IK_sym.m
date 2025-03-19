function [solutionA, solutionB] = robot_IK_analytical(EEx_d, EEy_d, EEz_d)
    % Perform forward kinematics to extract link lengths
    [~, o] = robot_FK(zeros(5, 1));
    l_3 = o.l3;
    l_4 = o.l4;
    l_5 = o.l5;

    % Calculate theta1
    theta1 = atan2(EEy_d, EEx_d);

    % Solve for theta2 and theta3 using two-link IK
    [t1a, t2a, t1b, t2b] = two_link_IK(EEx_d, EEy_d, l_3, l_4 + l_5);
    

    % Calculate solutions for theta2 and theta3
    theta2a = deg2rad(157.17) - t1a;
    theta3a = t2a + deg2rad(67.17);

    theta2b = deg2rad(157.17) - t1b;
    theta3b = t2b + deg2rad(67.17);


  

    % Combine solutions into output
    solutionA = [theta1; theta2a; theta3a];
    solutionB = [theta1; theta2b; theta3b];

    % Display solutions
    fprintf("Solution A:\nTheta1: %.2f°\nTheta2: %.2f°\nTheta3: %.2f°\n", ...
        rad2deg(solutionA(1)), rad2deg(solutionA(2)), rad2deg(solutionA(3)));

    fprintf("\nSolution B:\nTheta1: %.2f°\nTheta2: %.2f°\nTheta3: %.2f°\n", ...
        rad2deg(solutionB(1)), rad2deg(solutionB(2)), rad2deg(solutionB(3)));
end

% Validation section: verify the analytical IK solutions
fprintf("\n===== Validation =====\n");

% Create a set of test joint angles
test_joints = [deg2rad(20), deg2rad(-20), deg2rad(30), deg2rad(0), deg2rad(0)];
fprintf("Original joint angles (degrees):\n");
fprintf("Theta1: %.2f°\nTheta2: %.2f°\nTheta3: %.2f°\nTheta4: %.2f°\nTheta5: %.2f°\n", ...
    rad2deg(test_joints));

% Calculate forward kinematics to get the position
T_FK = robot_FK(test_joints);
pos = T_FK.T_0T6(1:3, 4);
fprintf("\nCalculated end-effector position:\n");
fprintf("X: %.2f mm, Y: %.2f mm, Z: %.2f mm\n", pos(1), pos(2), pos(3));

% Now use our analytical IK function to calculate joint angles for this position
[solutionA, solutionB] = robot_IK_analytical(pos(1), pos(2), pos(3));

% Display analytical IK solutions - already displayed in the function, but can add a header
fprintf("\nAnalytical IK solutions using robot_IK_analytical():\n");

% Verify the solutions by applying forward kinematics again
solution_a = [solutionA; test_joints(4); test_joints(5)];
T_a = robot_FK(solution_a);
pos_a = T_a.T_0T6(1:3, 4);

solution_b = [solutionB; test_joints(4); test_joints(5)];
T_b = robot_FK(solution_b);
pos_b = T_b.T_0T6(1:3, 4);

% Calculate and display position errors
error_a = norm(pos - pos_a);
error_b = norm(pos - pos_b);

fprintf("Verification:\n");
fprintf("Solution A position error: %.4f mm\n", error_a);
fprintf("Solution B position error: %.4f mm\n", error_b);

% Using numerical method (robot_IK.m) for comparison
fprintf("\nNumerical IK Solution (using robot_IK.m):\n");
q0 = zeros(5,1);  % Initial guess
num_solution = robot_IK(pos, q0, false);
fprintf("Theta1: %.2f°\nTheta2: %.2f°\nTheta3: %.2f°\nTheta4: %.2f°\nTheta5: %.2f°\n", ...
    rad2deg(num_solution));

% Verify numerical solution
T_num = robot_FK(num_solution);
pos_num = T_num.T_0T6(1:3, 4);
error_num = norm(pos - pos_num);
fprintf("Numerical solution position error: %.4f mm\n", error_num);


