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

# Add these functions for Cartesian control
def move_x_plus():
    RC.move_end_effector_by(dx=5, speed=speeds[0])

def move_x_minus():
    RC.move_end_effector_by(dx=-5, speed=speeds[0])

def move_y_plus():
    RC.move_end_effector_by(dy=5, speed=speeds[0])

def move_y_minus():
    RC.move_end_effector_by(dy=-5, speed=speeds[0])

def move_z_plus():
    RC.move_end_effector_by(dz=5, speed=speeds[0])

def move_z_minus():
    RC.move_end_effector_by(dz=-5, speed=speeds[0])

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

# Label for Cartesian control area
lbl_cartesian = tk.Label(frame, text="Cartesian Control", font=("Helvetica", 14))
lbl_cartesian.grid(row=5, column=0, columnspan=4, pady=(10, 10))

# X-axis Controls
btn_x_plus = tk.Button(frame, text="X +", command=move_x_plus, width=12)
btn_x_plus.grid(row=6, column=0, padx=5, pady=5)

btn_x_minus = tk.Button(frame, text="X -", command=move_x_minus, width=12)
btn_x_minus.grid(row=6, column=1, padx=5, pady=5)

# Y-axis Controls
btn_y_plus = tk.Button(frame, text="Y +", command=move_y_plus, width=12)
btn_y_plus.grid(row=7, column=0, padx=5, pady=5)

btn_y_minus = tk.Button(frame, text="Y -", command=move_y_minus, width=12)
btn_y_minus.grid(row=7, column=1, padx=5, pady=5)

# Z-axis Controls
btn_z_plus = tk.Button(frame, text="Z +", command=move_z_plus, width=12)
btn_z_plus.grid(row=8, column=0, padx=5, pady=5)

btn_z_minus = tk.Button(frame, text="Z -", command=move_z_minus, width=12)
btn_z_minus.grid(row=8, column=1, padx=5, pady=5)

# Label for extra controls
lbl_extra = tk.Label(frame, text="Other Controls", font=("Helvetica", 14))
lbl_extra.grid(row=9, column=0, columnspan=4, pady=(10, 10))

# Additional control buttons
btn_home = tk.Button(frame, text="Home Robot", command=home_robot, width=12)
btn_home.grid(row=10, column=0, padx=5, pady=5)

btn_grasp_open = tk.Button(frame, text="Grasper Open", command=grasper_open, width=12)
btn_grasp_open.grid(row=10, column=1, padx=5, pady=5)

btn_grasp_close = tk.Button(frame, text="Grasper Close", command=grasper_close, width=12)
btn_grasp_close.grid(row=10, column=2, padx=5, pady=5)

btn_exit = tk.Button(frame, text="Exit", command=exit_app, width=12, bg="red", fg="white")
btn_exit.grid(row=10, column=3, padx=5, pady=5)

# Start the Tkinter event loop
root.mainloop()
