import numpy as np
import matplotlib.pyplot as plt
import AdelmanPy as ap
from robot_draw import robot_draw

# Initial and final joint angles
gamma0 = np.array([0, 0, 0, 0, 0])
gammaf = np.array([np.pi/2, np.pi/2, np.pi/2, np.pi/2, np.pi/2])
dot_gamma0 = np.zeros(5)
dot_gammaf = np.zeros(5)

# Time parameters
t0 = 0
tf = 5
dt = 0.01
t = np.arange(t0, tf, dt)

# Generate cubic splines for each joint
a_0, a_1, a_2, a_3 = ap.cubic_spline(t0, tf, gamma0, gammaf, dot_gamma0, dot_gammaf)

# Reshape coefficients to match the dimensions of t
a_0 = a_0[:, np.newaxis]
a_1 = a_1[:, np.newaxis]
a_2 = a_2[:, np.newaxis]
a_3 = a_3[:, np.newaxis]

# Compute trajectories
trajectories = a_0 + a_1 * t + a_2 * t**2 + a_3 * t**3

# Initialize the plot
fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
plt.ion()  # Turn on interactive mode

# Animate the robot movement
for k in range(len(t)):
    current_angles = trajectories[:, k]
    ax.clear()  # Clear the previous plot
    positions = robot_draw(current_angles)
    
    # Ensure positions is a numpy array
    positions = np.array(positions)
    
    # Extract x, y, z coordinates
    x = positions[:, 0]
    y = positions[:, 1]
    z = positions[:, 2]
    
    # Update axis limits
    ax.set_xlim([x.min() - 1, x.max() + 1])
    ax.set_ylim([y.min() - 1, y.max() + 1])
    ax.set_zlim([z.min() - 1, z.max() + 1])
    
    plt.draw()  # Draw the updated plot
    plt.pause(dt)  # Pause to create the animation effect

plt.ioff()  # Turn off interactive mode
plt.show()  # Display the final plot

