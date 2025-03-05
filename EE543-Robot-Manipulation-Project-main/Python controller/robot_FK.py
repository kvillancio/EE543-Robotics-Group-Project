import numpy as np
from math import sin, cos

def dh_transform(theta, d, a, alpha):
    """
    Compute the DH transformation matrix for a single joint.
    
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