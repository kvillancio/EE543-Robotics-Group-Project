import numpy as np
from math import sin, cos

def dh_transform(theta, d, a, alpha):
    """
    Compute the DH transformation matrix for a single joint.
    
<<<<<<< Updated upstream
    Args:
        theta: joint angle (rotation around z-axis)
        d: link offset (translation along z-axis)
        a: link length (translation along x-axis)
        alpha: link twist (rotation around x-axis)
    
    Returns:
        4x4 homogeneous transformation matrix
    """
    T = np.array([
        [           cos(theta),           -sin(theta),           0,             a],
        [sin(theta)*cos(alpha), cos(theta)*cos(alpha), -sin(alpha), -sin(alpha)*d],
        [sin(theta)*sin(alpha), cos(theta)*sin(alpha),  cos(alpha),  cos(alpha)*d],
        [                    0,                     0,           0,             1]]
    )
    return T
=======
    # Link lengths
    # l1 = .23
    # l2 = .12
    # l3 = .53
    # l4 = .12
    # l5 = .19
    
    l1 = 1
    l2 = 1
    l3 = 1
    l4 = 1
    l5 = 1

    # DH parameters [a, alpha, d, theta]
    DH = [
        [             0, l1,  0, theta[0]],
        [np.deg2rad(90), l2,  0, theta[1]],
        [             0, l3,  0, theta[2]],
        [np.deg2rad(90),  0, l4, theta[3]],
        [             0,  0, l5,        0]
    ]
>>>>>>> Stashed changes

def robot_FK(q, robot_params=None):
    """
    Compute the forward kinematics of the robot.
    
    Args:
        q: Joint angles [q1, q2, q3, q4, q5, q6] in radians
        robot_params: Dictionary containing robot parameters (optional)
    
    Returns:
        T: 4x4 homogeneous transformation matrix from base to end-effector
        Ts: List of 4x4 homogeneous transformation matrices for each joint
    """
    # Default DH parameters for a 6-DOF manipulator
    # These should be replaced with the actual parameters of your robot
    if robot_params is None:
        # Example DH parameters [a, alpha, d, theta_offset]
        # For a standard 6-DOF manipulator
        robot_params = {
            'DH': [
            [0, 0, 1, 0],                      # Joint 1
            [0, -np.pi/2, 0, 0],               # Joint 2
            [1, 0, 0, 0],                      # Joint 3
            [1, np.pi/2, 0, np.pi/2],          # Joint 4
            [0, np.pi/2, 0, 0],                # Joint 5
            [0, 0, 1, 0]                       # Joint 6
            ]
        }
    
    # Initialize transformation matrices
    T = np.eye(4)
    Ts = []
    
    # Compute forward kinematics
    for i in range(len(q)):
        # Extract DH parameters for current joint
        a, alpha, d, theta_offset = robot_params['DH'][i]
        
        # Compute joint transformation
        T_i = dh_transform(q[i] + theta_offset, d, a, alpha)
        
        # Accumulate transformation
        T = T @ T_i
        Ts.append(T.copy())
    
    return T, Ts

<<<<<<< Updated upstream
def get_position_orientation(T):
    """
    Extract position and orientation from transformation matrix.
    
    Args:
        T: 4x4 homogeneous transformation matrix
    
    Returns:
        position: [x, y, z]
        orientation: rotation matrix (3x3)
    """
    position = T[0:3, 3]
    orientation = T[0:3, 0:3]
    
    return position, orientation

if __name__ == "__main__":
    # Example usage
    q = np.array([0, 0, 0, 0, 0, 0])  # Zero configuration
    
    # Compute forward kinematics
    T, Ts = robot_FK(q)
    
    # Get position and orientation
    position, orientation = get_position_orientation(T)
    
    print("End-effector position:", position)
    print("End-effector orientation:\n", orientation)
=======
if __name__ == "__main__":
    # Define the zero configuration for the robot
    theta_zero = np.zeros(5)

    # Calculate the forward kinematics at the zero configuration
    T_matrices, T_matrices_zero = FK(theta_zero)

    # Print the results
    print("Transformation matrices with respect to each frame:")
    for key, value in T_matrices.items():
        print(f"{key}:\n{value}\n")

    print("Transformation matrices with respect to the base frame:")
    for key, value in T_matrices_zero.items():
        print(f"{key}:\n{value}\n")
>>>>>>> Stashed changes
