import numpy as np
from math import sin, cos

def dh_transform(alpha, a, d, theta):
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

def FK(gamma):
    """
    Compute the forward kinematics of the robot.
    
    Args:
        gamma: 5x1 vector of joint angles (rad)
    
    Returns:
        T_matrices: Dictionary of transformation matrices for each frame relative to its parent
        T_matrices_zero: Dictionary of transformation matrices for each frame relative to base frame
    """
    if len(gamma) != 5:
        raise ValueError("Expected 5 joint angles, got {}".format(len(gamma)))
    
    # Link lengths in mm
    l1 = 0     # frames 0 and 1 are coincident
    l2 = 62.8  # mm
    l3 = 92.77 # mm
    l4 = 52.5  # mm
    l5 = 165.39 # mm
    
    # DH parameters [alpha, a, d, theta]
    DH = [
        [0,           0, 1,          gamma[0]],  # Joint 1
        [-np.pi/2,    0, 0,          gamma[1]],  # Joint 2
        [0,           1, 0,          gamma[2]],  # Joint 3
        [np.pi/2,     1, 0,  np.pi/2+gamma[3]],  # Joint 4
        [np.pi/2,     0, 0,          gamma[4]],  # Joint 5
        [0,           0, 1,                 0]   # End effector frame - fixed offset
    ]
    
    # Initialize transformation matrices
    T_matrices = {}
    T_matrices_zero = {}
    T_0_i = np.eye(4)
    
    # Calculate transformation matrices
    for i in range(len(DH)):
        # Extract DH parameters
        alpha, a, d, theta = DH[i]
        
        # Compute transformation matrix
        T_i_minus1_i = dh_transform(theta, d, a, alpha)
        
        # Store the transformation matrix from frame i-1 to frame i
        key = f"T_{i}T{i+1}"
        T_matrices[key] = T_i_minus1_i
        
        # Compute and store the transformation matrix from base frame to frame i
        T_0_i = T_0_i @ T_i_minus1_i
        key_zero = f"T_0T{i+1}"
        T_matrices_zero[key_zero] = T_0_i.copy()
    
    return T_matrices, T_matrices_zero

if __name__ == "__main__":
    # Example usage
    gamma = np.array([0, 0, 0, 0, 0])  # Zero configuration
    
    # Compute forward kinematics
    T_matrices, T_matrices_zero = FK(gamma)
    
    # Print the results
    print("Transformation matrices with respect to each frame:")
    for key, value in T_matrices.items():
        print(f"{key}:\n{value}\n")
    
    print("Transformation matrices with respect to the base frame:")
    for key, value in T_matrices_zero.items():
        print(f"{key}:\n{value}\n")
    
    # Print end effector position
    end_effector_position = T_matrices_zero["T_0T6"][0:3, 3]
    print(f"End-effector position: {end_effector_position}")
    
    # Example with non-zero joint angles
    gamma = np.array([1, 1, 1, 1, 1])
    T_matrices, T_matrices_zero = FK(gamma)
    end_effector_position = T_matrices_zero["T_0T6"][0:3, 3]
    print(f"End-effector position with non-zero joint angles: {end_effector_position}")