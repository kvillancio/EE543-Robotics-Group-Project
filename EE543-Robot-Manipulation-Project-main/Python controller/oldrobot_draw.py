from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from robot_FK import FK

# Persistent variables to store the figure and axes
fig = None 
ax = None
line = None
joints = None

def robot_draw(gamma):
    """
    Plots a 3D line with small spheres at each joint.

    Parameters:
    gamma (array): Joint angles for the robot.
    """
    global fig, ax, line, joints

    _, T_matrices_zero = FK(gamma)  # Perform forward kinematics to get the transformation matrices

    # Extract the position vectors from the transformation matrices
    positions = [T[:3, 3] for T in T_matrices_zero.values()]

    # Convert positions to numpy array for easier manipulation
    positions = np.array(positions)

    # Extract x, y, z coordinates
    x = positions[:, 0]
    y = positions[:, 1]
    z = positions[:, 2]

    if fig is None or ax is None:
        # Create a new figure for plotting
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Plot the line with a bold width
        line, = ax.plot(x, y, z, linewidth=3, label='Bold Line')

        # Plot small spheres at each joint
        joints = ax.scatter(x, y, z, color='r', s=50, label='Joints')

        # Add labels and a legend
        ax.set_xlabel('X axis')
        ax.set_ylabel('Y axis')
        ax.set_zlabel('Z axis')
        ax.legend()
        
        plt.show()
    else:
        # Update the data in the existing plot
        line.set_data(x, y)
        line.set_3d_properties(z)
        joints._offsets3d = (x, y, z)
        
    # Redraw the figure
    plt.draw()
    plt.pause(0.01)
    
    
# Example usage
if __name__ == "__main__":
    # Example joint angles for the robot
    gamma = [0, 0, 0, 0, 0]
    
    # Call the robot_draw function with the example joint angles
    robot_draw(gamma)