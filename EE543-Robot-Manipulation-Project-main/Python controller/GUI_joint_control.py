import tkinter as tk
import numpy as np
import sys, os
from robot_controller import robot_controller

# Initialize the robot controller
RC = robot_controller()
RC.communication_begin()
RC.joints_homing()  # Force homing of the robot
 
# Control parameters
increment = 5               # Increment angle (in degrees)
goals = np.zeros(RC.joint_num)
speeds = np.ones(RC.joint_num) * 80   # Speed in degrees per second

def update_joints():
    global goals
    # Ensure joint targets remain within limits
    goals = np.clip(goals, RC.servo_angle_min, RC.servo_angle_max)
    RC.joints_goto(goals, speeds)

def joint1_plus():
    global goals
    goals[0] += increment
    update_joints()

def joint1_minus():
    global goals
    goals[0] -= increment
    update_joints()

def joint2_plus():
    global goals
    goals[1] += increment
    update_joints()

def joint2_minus():
    global goals
    goals[1] -= increment
    update_joints()

def joint3_plus():
    global goals
    goals[2] += increment
    update_joints()

def joint3_minus():
    global goals
    goals[2] -= increment
    update_joints()

def joint4_plus():
    global goals
    goals[3] += increment
    update_joints()

def joint4_minus():
    global goals
    goals[3] -= increment
    update_joints()

def home_robot():
    global goals
    # Reset joints to the robot's home pose.
    goals = RC.robot_homing_joint_poses.copy()
    update_joints()

def grasper_open():
    global goals
    goals[4] += increment
    update_joints()

def grasper_close():
    global goals
    goals[4] -= increment
    update_joints()

def exit_app():
    root.destroy()
    RC.communication_end()
    sys.exit('Closing GUI controller')

# Create the main GUI window
root = tk.Tk()
root.title("EE543 Arm Controller")

# Create a frame for organizing the buttons
frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

# Label for joint control area
lbl_joints = tk.Label(frame, text="Joint Control", font=("Helvetica", 14))
lbl_joints.grid(row=0, column=0, columnspan=4, pady=(0, 10))

# Joint 1 Controls
btn_joint1_plus = tk.Button(frame, text="Joint 1 +", command=joint1_plus, width=12)
btn_joint1_plus.grid(row=1, column=0, padx=5, pady=5)

btn_joint1_minus = tk.Button(frame, text="Joint 1 -", command=joint1_minus, width=12)
btn_joint1_minus.grid(row=1, column=1, padx=5, pady=5)

# Joint 2 Controls
btn_joint2_plus = tk.Button(frame, text="Joint 2 +", command=joint2_plus, width=12)
btn_joint2_plus.grid(row=2, column=0, padx=5, pady=5)

btn_joint2_minus = tk.Button(frame, text="Joint 2 -", command=joint2_minus, width=12)
btn_joint2_minus.grid(row=2, column=1, padx=5, pady=5)

# Joint 3 Controls
btn_joint3_plus = tk.Button(frame, text="Joint 3 +", command=joint3_plus, width=12)
btn_joint3_plus.grid(row=3, column=0, padx=5, pady=5)

btn_joint3_minus = tk.Button(frame, text="Joint 3 -", command=joint3_minus, width=12)
btn_joint3_minus.grid(row=3, column=1, padx=5, pady=5)

# Joint 4 Controls
btn_joint4_plus = tk.Button(frame, text="Joint 4 +", command=joint4_plus, width=12)
btn_joint4_plus.grid(row=4, column=0, padx=5, pady=5)

btn_joint4_minus = tk.Button(frame, text="Joint 4 -", command=joint4_minus, width=12)
btn_joint4_minus.grid(row=4, column=1, padx=5, pady=5)

# Label for extra controls
lbl_extra = tk.Label(frame, text="Other Controls", font=("Helvetica", 14))
lbl_extra.grid(row=5, column=0, columnspan=4, pady=(10, 10))

# Additional control buttons
btn_home = tk.Button(frame, text="Home Robot", command=home_robot, width=12)
btn_home.grid(row=6, column=0, padx=5, pady=5)

btn_grasp_open = tk.Button(frame, text="Grasper Open", command=grasper_open, width=12)
btn_grasp_open.grid(row=6, column=1, padx=5, pady=5)

btn_grasp_close = tk.Button(frame, text="Grasper Close", command=grasper_close, width=12)
btn_grasp_close.grid(row=6, column=2, padx=5, pady=5)

btn_exit = tk.Button(frame, text="Exit", command=exit_app, width=12, bg="red", fg="white")
btn_exit.grid(row=6, column=3, padx=5, pady=5)

# Add input fields for x, y, z coordinates
lbl_xyz = tk.Label(frame, text="XYZ Control", font=("Helvetica", 14))
lbl_xyz.grid(row=7, column=0, columnspan=4, pady=(10, 10))

entry_x = tk.Entry(frame, width=10)
entry_x.grid(row=8, column=0, padx=5, pady=5)
entry_x.insert(0, "X")

entry_y = tk.Entry(frame, width=10)
entry_y.grid(row=8, column=1, padx=5, pady=5)
entry_y.insert(0, "Y")

entry_z = tk.Entry(frame, width=10)
entry_z.grid(row=8, column=2, padx=5, pady=5)
entry_z.insert(0, "Z")

# Add button to trigger inverse kinematics
btn_ik = tk.Button(frame, text="Move to XYZ", command=move_to_xyz, width=12)
btn_ik.grid(row=8, column=3, padx=5, pady=5)

# Function to handle inverse kinematics

def move_to_xyz():
    try:
        x = float(entry_x.get())
        y = float(entry_y.get())
        z = float(entry_z.get())
        desired_pos = np.array([x, y, z])
        # Call robot_IK to get joint angles
        joint_angles = robot_IK(desired_pos, goals)
        # Update goals with new joint angles
        global goals
        goals = joint_angles
        update_joints()
    except ValueError:
        print("Invalid input for XYZ coordinates")

# Start the Tkinter event loop
root.mainloop()
