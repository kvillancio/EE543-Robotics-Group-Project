import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from robot_FK import FK

def plot_workspace():
    # Define the range of joint angles (in radians)
    joint_ranges = [
        np.linspace(0, 2*np.pi, 10),  # Joint 1
        np.linspace(-np.pi/2, np.pi/2, 10),  # Joint 2
        np.linspace(-np.pi/2, np.pi/2, 10),  # Joint 3
        np.linspace(-np.pi/2, np.pi/2, 10),  # Joint 4
        np.linspace(-np.pi/2, np.pi/2, 10)   # Joint 5 (Gripper)
    ]

    # Initialize lists to store the end-effector positions
    x_coords, y_coords, z_coords = [], [], []

    # Iterate through all combinations of joint angles
    for theta1 in joint_ranges[0]:
        for theta2 in joint_ranges[1]:
            for theta3 in joint_ranges[2]:
                for theta4 in joint_ranges[3]:
                    for theta5 in joint_ranges[4]:
                        # Calculate the forward kinematics
                        gamma = [theta1, theta2, theta3, theta4, theta5]
                        T, _ = FK(gamma)
                        
                        # Extract the end-effector position
                        x_coords.append(T[0, 3])
                        y_coords.append(T[1, 3])
                        z_coords.append(T[2, 3])

    # Create a 3D plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x_coords, y_coords, z_coords, c='b', marker='o')

    # Set plot labels
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Reachable Workspace of the Robot')

    # Show the plot
    plt.show()

# Call the function to plot the workspace
plot_workspace()