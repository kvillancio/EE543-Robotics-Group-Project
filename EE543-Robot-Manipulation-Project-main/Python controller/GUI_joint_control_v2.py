import PySimpleGUI as sg
import numpy as np
import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from robot_controller import robot_controller  # Ensure this import matches your setup
from robot_draw import draw_robot  # Import the draw_robot function instead of RobotDraw class

# Initialize robot controller (ensure correct initialization)
RC = robot_controller()
RC.communication_begin()
RC.joints_homing()

# Initialize robot visualization
fig = plt.figure(figsize=(5, 4))
ax = fig.add_subplot(111, projection='3d')

# Control parameters
increment = 5  # Increment angle (degrees)
goals = np.zeros(RC.joint_num)
speeds = np.ones(RC.joint_num) * 80  # Speed (degrees/second)
frame_num = 1  # For tracking visualization updates
figure_canvas_agg = None  # Will hold the canvas for drawing

def update_joints():
    """Updates robot joint angles, ensuring they stay within limits."""
    global goals, frame_num
    goals = np.clip(goals, RC.servo_angle_min, RC.servo_angle_max)
    RC.joints_goto(goals, speeds)
    
    # Update the visualization
    update_visualization()
    frame_num += 1

def update_visualization():
    """Updates the robot visualization with current joint angles."""
    global fig, ax, frame_num, figure_canvas_agg
    
    # Clear the axis for redrawing
    ax.clear()
    
    # Convert degrees to radians for visualization
    # Assuming your robot uses 6 joints in the model
    joint_angles_rad = np.radians(goals)
    
    # If your hardware has fewer joints than the model expects,
    # pad with zeros (e.g., 4 hardware joints, 6 expected in model)
    if len(joint_angles_rad) < 6:
        joint_angles_rad = np.pad(joint_angles_rad, (0, 6 - len(joint_angles_rad)))
    
    # Draw the robot using the draw_robot function
    draw_robot(joint_angles_rad, ax=ax)
    
    # Update the title with current frame number
    ax.set_title(f'Robot Configuration (Frame {frame_num})')
    
    # Update the canvas
    if figure_canvas_agg is not None:
        figure_canvas_agg.draw()

def joint_control(joint_index, direction):
    """Adjusts a specific joint angle."""
    global goals
    if direction == '+':
        goals[joint_index] += increment
    else:
        goals[joint_index] -= increment
    update_joints()

def home_robot():
    """Moves the robot to its home pose."""
    global goals
    goals = RC.robot_homing_joint_poses.copy()
    update_joints()

def grasper_control(action):
    """Opens or closes the robot's grasper."""
    if action == 'open':
        # RC.gripper_open()
        goals[4] += increment
        update_joints()
    else:
        # RC.gripper_close()
        goals[4] -= increment
        update_joints()

def exit_app():
    """Closes communication with the robot and exits the GUI."""
    RC.communication_end()
    plt.close('all')
    sys.exit('Closing GUI controller')

def draw_figure(canvas, figure):
    """Draw a matplotlib figure onto a PySimpleGUI canvas."""
    global figure_canvas_agg
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

# PySimpleGUI Layout with added visualization canvas
layout = [
    [sg.Text("Joint Control", font=("Helvetica", 14), justification='center', expand_x=True)],
    [sg.Column([
        [sg.Button("Joint 1 +", key="-J1P-", size=(12, 1)), sg.Button("Joint 1 -", key="-J1M-", size=(12, 1))],
        [sg.Button("Joint 2 +", key="-J2P-", size=(12, 1)), sg.Button("Joint 2 -", key="-J2M-", size=(12, 1))],
        [sg.Button("Joint 3 +", key="-J3P-", size=(12, 1)), sg.Button("Joint 3 -", key="-J3M-", size=(12, 1))],
        [sg.Button("Joint 4 +", key="-J4P-", size=(12, 1)), sg.Button("Joint 4 -", key="-J4M-", size=(12, 1))],
        [sg.Text("Other Controls", font=("Helvetica", 14), justification='center', expand_x=True)],
        [sg.Button("Home Robot", key="-HOME-", size=(12, 1)),
         sg.Button("Grasper Open", key="-OPEN-", size=(12, 1)),
         sg.Button("Grasper Close", key="-CLOSE-", size=(12, 1)),
         sg.Button("Exit", key="-EXIT-", size=(12, 1), button_color=('white', 'red'))]
    ]), 
    sg.Column([
        [sg.Canvas(key='-CANVAS-', size=(400, 400))]
    ])]
]

# Create the Window
window = sg.Window("EE543 Arm Controller", layout, finalize=True)

# Initialize the visualization
update_visualization()

# Event Loop
while True:
    event, values = window.read(timeout=100)  # Added timeout for periodic updates
    
    if event == sg.WIN_CLOSED or event == "-EXIT-":
        exit_app()
        break  # Ensure proper exit

    # Joint controls
    if event == "-J1P-":
        joint_control(0, '+')
    if event == "-J1M-":
        joint_control(0, '-')
    if event == "-J2P-":
        joint_control(1, '+')
    if event == "-J2M-":
        joint_control(1, '-')
    if event == "-J3P-":
        joint_control(2, '+')
    if event == "-J3M-":
        joint_control(2, '-')
    if event == "-J4P-":
        joint_control(3, '+')
    if event == "-J4M-":
        joint_control(3, '-')

    # Other controls
    if event == "-HOME-":
        home_robot()
    if event == "-OPEN-":
        grasper_control('open')
    if event == "-CLOSE-":
        grasper_control('close')

window.close()
