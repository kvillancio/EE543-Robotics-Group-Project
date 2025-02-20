import PySimpleGUI as sg
import numpy as np
import sys
from robot_controller import robot_controller  # Ensure this import matches your setup

# Initialize robot controller (ensure correct initialization)
RC = robot_controller()
RC.communication_begin()
RC.joints_homing()

# Control parameters
increment = 5  # Increment angle (degrees)
goals = np.zeros(RC.joint_num)
speeds = np.ones(RC.joint_num) * 80  # Speed (degrees/second)

def update_joints():
    """Updates robot joint angles, ensuring they stay within limits."""
    global goals
    goals = np.clip(goals, RC.servo_angle_min, RC.servo_angle_max)
    RC.joints_goto(goals, speeds)

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
    sys.exit('Closing GUI controller')

# PySimpleGUI Layout
layout = [
    [sg.Text("Joint Control", font=("Helvetica", 14), justification='center', expand_x=True)],
    [sg.Button("Joint 1 +", key="-J1P-", size=(12, 1)), sg.Button("Joint 1 -", key="-J1M-", size=(12, 1))],
    [sg.Button("Joint 2 +", key="-J2P-", size=(12, 1)), sg.Button("Joint 2 -", key="-J2M-", size=(12, 1))],
    [sg.Button("Joint 3 +", key="-J3P-", size=(12, 1)), sg.Button("Joint 3 -", key="-J3M-", size=(12, 1))],
    [sg.Button("Joint 4 +", key="-J4P-", size=(12, 1)), sg.Button("Joint 4 -", key="-J4M-", size=(12, 1))],
    [sg.Text("Other Controls", font=("Helvetica", 14), justification='center', expand_x=True)],
    [sg.Button("Home Robot", key="-HOME-", size=(12, 1)),
     sg.Button("Grasper Open", key="-OPEN-", size=(12, 1)),
     sg.Button("Grasper Close", key="-CLOSE-", size=(12, 1)),
     sg.Button("Exit", key="-EXIT-", size=(12, 1), button_color=('white', 'red'))]
]

# Create the Window
window = sg.Window("EE543 Arm Controller", layout)

# Event Loop
while True:
    event, values = window.read()
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
