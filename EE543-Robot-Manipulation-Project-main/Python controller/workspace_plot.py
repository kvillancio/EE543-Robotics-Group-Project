import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from robot_FK import FK

def plot_workspace(num_samples=100000, joint_limits=None):
    """
    plot_workspace plots the workspace of the robot's end effector position
    using a Monte Carlo simulation.

    Inputs:
    num_samples : Number of samples for the Monte Carlo simulation
    joint_limits : 5x2 matrix of joint limits [min, max] for each joint

    Example:
    plot_workspace(1000, [[0, 2*np.pi], [-np.pi/2, np.pi/2], [-np.pi/2, np.pi/2], [-np.pi/2, np.pi/2], [-np.pi/2, np.pi/2]])
    """
    if joint_limits is None:
        joint_limits = [
            [0, np.pi],
            [-np.pi/2, np.pi/2],
            [-np.pi/2, np.pi/2],
            [-np.pi/2, np.pi/2],
            [-np.pi/2, np.pi/2]
        ]

    # Initialize arrays to store end effector positions
    x_coords = np.zeros(num_samples)
    y_coords = np.zeros(num_samples)
    z_coords = np.zeros(num_samples)

    for i in range(num_samples):
        # Generate random joint angles within the specified limits
        gamma = [np.random.uniform(joint_limits[j][0], joint_limits[j][1]) for j in range(5)]
        
        # Calculate forward kinematics
        T = FK(gamma)
        
        # Extract the end-effector position
        x_coords[i] = T[0, 3]
        y_coords[i] = T[1, 3]
        z_coords[i] = T[2, 3]

    # Create a 3D plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x_coords, y_coords, z_coords, c='b', marker='o', alpha=0.1)

    # Set plot labels
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Reachable Workspace of the Robot')

    # Show the plot
    plt.show()

# Call the function to plot the workspace
plot_workspace()