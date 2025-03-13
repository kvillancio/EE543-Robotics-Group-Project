import time
import numpy as np
import serial
import sys, os
import matlab.engine  # Add this import for MATLAB engine

np.set_printoptions(precision=2, suppress=False)
np.set_printoptions(formatter={'all': lambda x: f'{x:.2f}'})

class robot_controller():
    def __init__(self, use_visualization=True) -> None:
        #define robot parameter
        self.joint_num = 5
        self.joints_goto_tolerance = 10e-3

        #define robot state
        self.robotstate_joint_poses = np.zeros(self.joint_num)
        self.robotstate_joint_vels = np.zeros(self.joint_num)
        self.robotState_endeffector_orientation = np.zeros(3)
        self.robotstate_endeffector_pose = np.zeros(3)
        self.robotstate_gripper_close = False

        #define homing position in joint space
        self.robot_homing_joint_poses = np.zeros(self.joint_num)

        """
        ---------------------------------------------------------------
         Below are the parameters related to robot link geometry
        ---------------------------------------------------------------
        """

        #define the DH parameter for the arm link
        # [a, alpha, d, theta (will be replaced by joint_positions)]
        self.dh_params = [ # this is for 4 joints setting
            [0, 0, 0, 0],  # Joint 1
            [0, 0, 0, 0],  # Joint 2
            [0, 0, 0, 0],  # Joint 3
            [0, 0, 0, 0]   # Joint 4
        ]

        self.angle_offsets = np.array([0, 0, 0, 0]) # this is for 4 joints setting

        # the transformation matrices from first to last link 
        self.T_matrices = np.empty(self.joint_num) # no value when init

        #define the base frame
        self.base_frame = np.eye(self.joint_num)

        """
        ---------------------------------------------------------------
         Below are the parameters related to hardware and communciation
        ---------------------------------------------------------------
        """

        #here define the specification for MG996R servo motors
        self.servo_angle_max = 90 #degree
        self.servo_angle_min = -90 #degree
        self.servo_pulse_max = 440 #+90 for mg996R, This is the 'maximum' pulse length count (out of 4096)
        self.servo_pulse_min = 70 #-90 for mg996R, This is the 'minimum' pulse length count (out of 4096)

        #here defind the operating parameters for magnetic gripper
        self.gripper_pulse_close = 4095 #This is the pulse length count (out of 4096) of 100% duty cycle
        self.gripper_pulse_open = 0     #This is the pulse length count (out of 4096) of 0% duty cycle


        #define the serial communication parameter
        self.com_port = '/dev/tty.usbserial-A5069RR4' # change it if needed
        self.com_baudrate = 115200 #bps
        self.com_frequency = 30 #Hz
        
        # Initialize MATLAB visualization if requested
        self.use_visualization = use_visualization
        if self.use_visualization:
            self.initialize_matlab_visualization()

    """
    ---------------------------------------------------------------
     Functions below set up the serial communication
    ---------------------------------------------------------------
    """

    def communication_begin(self):
        self.ser = serial.Serial(self.com_port, self.com_baudrate)
        # Reset input/output buffer and wait for initialization
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()
        time.sleep(1)

        # Wait for Arduino to initialize
        while True:
            if self.ser.read() == b'I':
                break

        # Send signaling byte
        self.ser.write(b'S')
        time.sleep(0.1)
    
    def communication_end(self):
        self.ser.close()

    """
    ---------------------------------------------------------------
     Functions below set up the visualization
    ---------------------------------------------------------------
    """
    
    def initialize_matlab_visualization(self):
        """Initialize MATLAB engine for robot visualization"""
        print("Starting MATLAB engine for visualization...")
        self.matlab_engine = matlab.engine.start_matlab()
        
        # Get current directory of the Python script
        import os
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Fix the path to point to the correct MATLAB directory
        matlab_dir = "/Users/ian/Documents/FinalProject/EE543-Robotics-Group-Project/MATLAB"      
        
        # Add both the main directory and the robo_utils subdirectory
        self.matlab_engine.addpath(matlab_dir, nargout=0)
        self.matlab_engine.addpath(os.path.join(matlab_dir, "robo_utils"), nargout=0)
        
        self.matlab_engine.cd(script_dir)
        
        # Convert angles from degrees to radians before sending to MATLAB
        joint_poses_radians = np.deg2rad(self.robotstate_joint_poses)
        matlab_array = matlab.double(joint_poses_radians.tolist())
        
        # Store the figure handle returned by robot_draw for reuse
        self.fig_handle = self.matlab_engine.robot_draw(matlab_array, nargout=1)
        print("MATLAB visualization initialized")

    def update_matlab_visualization(self):
        """Update the MATLAB visualization with current robot state"""
        if hasattr(self, 'matlab_engine') and hasattr(self, 'fig_handle'):
            # Convert angles from degrees to radians before sending to MATLAB
            joint_poses_radians = np.deg2rad(self.robotstate_joint_poses)
            matlab_array = matlab.double(joint_poses_radians.tolist())
            
            # Pass the stored figure handle to robot_draw
            self.matlab_engine.robot_draw(matlab_array, self.fig_handle, nargout=0)
    
    def close_matlab_visualization(self):
        """Close the MATLAB engine"""
        if hasattr(self, 'matlab_engine'):
            print("Closing MATLAB visualization engine")
            self.matlab_engine.quit()
        
    """
    ---------------------------------------------------------------
     Functions below setup the transformation matrix for 
     forward kinematics
    ---------------------------------------------------------------
    """

    # input: DH parameters of a specific link, angle in degree, length in mm
    # output: the transformation matrix of that link
    def dh_to_transformation_matrix(self, alpha, a, d, theta):

        return None
    
    def update_forward_kinematics(self):
        
       return None



    """
    ---------------------------------------------------------------
     Functions below convert the joint command into proper form for
     serial communication
    ---------------------------------------------------------------
    """
    # convert the multiple joint poses in angle into pulse lengths array
    # map the angle from -90 to 90 degree to minimal till maximal servo pulse length
    def angle_to_pulse_length(self, angles):
        clipped_angles = np.clip(angles, self.servo_angle_min, self.servo_angle_max)
        pulse_lengths = ((clipped_angles - self.servo_angle_min) * (self.servo_pulse_max - self.servo_pulse_min) / (self.servo_angle_max - self.servo_angle_min) + self.servo_pulse_min).astype(int)
        return pulse_lengths

    # convert the multiple joint poses in pulse lengths into 8 bytes array
    # format will be JP1_H, JP1_L, ..., unit: length count
    def pulse_length_to_byte(self, pulse_lengths):
        # clipped_pulse_lengths = (list)(np.clip(pulse_lengths, self.servo_pulse_min, self.servo_pulse_max))
        clipped_pulse_lengths = (list)(pulse_lengths)
        ret = []
        for pulse_length in clipped_pulse_lengths:
            # convert the number into high and low bytes
            # pulse_length = (int)pulse_length
            pulse_length_byte = int(pulse_length).to_bytes(2, byteorder='big')
            ret.append(pulse_length_byte[0])
            ret.append(pulse_length_byte[1])
        return ret
    
    
    # Set the joint to the homing position
    # Cautious: The robot will move rapidly if this is executed
    def joints_homing(self):
        # reset robot state
        self.robotstate_joint_poses = self.robot_homing_joint_poses.copy()
        self.robotstate_gripper_close = False

        # compose command
        joint_pulse_lengthes = self.angle_to_pulse_length(self.robotstate_joint_poses)
        joint_pulse_lengthes = np.append(joint_pulse_lengthes,self.gripper_pulse_open)
        # print(joint_pulse_lengthes)
        numbers = self.pulse_length_to_byte(joint_pulse_lengthes)
        # print(numbers)
        # Poll for acknowledgement
        while self.ser.in_waiting == 0:
            continue
        # ser.reset_input_buffer()

        # # Send data if acknowledgement received
        if self.ser.read() == b'A':
            self.ser.write(numbers)
            self.ser.flush()


    
    # this is the goto function in joint space
    def joints_goto(self, goals, speeds):
        # get the current robot joint poses
        start_poses = self.robotstate_joint_poses.copy()
        # calculate the rotation direction of each joints
        angle_diff = goals - start_poses
        # calculate the angle increments under 20Hz update rates
        angle_increments = np.sign(angle_diff) * (speeds / self.com_frequency)
        
        reached_goal = False        
        # update the robot joint poses by adding the angle increments
        while not reached_goal:
            start = time.time()

            # Generate 8 uint8_t numbers
            self.robotstate_joint_poses += angle_increments
            # check if the individual joint reach the goal
            for i in range(self.joint_num):
                if goals[i] > start_poses[i]: # the angle is increasing
                    self.robotstate_joint_poses[i] = np.clip(self.robotstate_joint_poses[i], start_poses[i], goals[i])
                elif goals[i] < start_poses[i]: # the angle is decreasing
                    self.robotstate_joint_poses[i] = np.clip(self.robotstate_joint_poses[i], goals[i], start_poses[i])
                else:
                    self.robotstate_joint_poses[i] = start_poses[i].copy()
                    
            # Enhanced state display with degrees, radians, and XYZ position
            sys.stdout.write('\r' + ' ' * 100 + '\r')  # clear the line with more space
            
            # Get current joint angles in radians and position using FK
            current_rad = np.deg2rad(self.robotstate_joint_poses)
            position_str = "Unknown"
            
            if hasattr(self, 'matlab_engine'):
                try:
                    # Convert to MATLAB format and get FK
                    matlab_joint_angles = matlab.double(current_rad.tolist())
                    
                    # Use MATLAB workspace to safely extract position
                    self.matlab_engine.workspace['joints'] = matlab_joint_angles
                    self.matlab_engine.eval("T = robot_FK(joints);", nargout=0)
                    self.matlab_engine.eval("pos = T.T_0T6(1:3, 4);", nargout=0)
                    position = self.matlab_engine.workspace['pos']
                    
                    # Format position as a string with 2 decimal places
                    x = float(position[0][0])
                    y = float(position[1][0])
                    z = float(position[2][0])
                    position_str = f"X:{x:.2f}, Y:{y:.2f}, Z:{z:.2f}"
                except Exception as e:
                    position_str = f"FK Error: {str(e)}"
            
            # Display all state information
            # Clear terminal completely before writing new status
            os.system('clear')  # For macOS/Linux
            # For Windows, we would use: os.system('cls')

            state_info = (f"Joint angles (deg): {str(self.robotstate_joint_poses)} | " + 
                         f"Joint angles (rad): {str(current_rad)} | " + 
                         f"Position (mm): {position_str}")
            print(state_info, end="")
            sys.stdout.flush()
            
            # Update MATLAB visualization with current state
            if hasattr(self, 'matlab_engine'):
                self.update_matlab_visualization()
                
            #check if the robot reach the goal joint poses
            if np.all(np.abs(self.robotstate_joint_poses - goals) <= self.joints_goto_tolerance):
                reached_goal = True

            #convert the joint_pose to pulse length
            joint_pulse_lengthes = self.angle_to_pulse_length(self.robotstate_joint_poses)

            #add one more byte in the pulse length array to as gripper command
            if self.robotstate_gripper_close:
                joint_pulse_lengthes = np.append(joint_pulse_lengthes,self.gripper_pulse_close)
            else:
                joint_pulse_lengthes = np.append(joint_pulse_lengthes,self.gripper_pulse_open)
            # print(joint_pulse_lengthes)
            numbers = self.pulse_length_to_byte(joint_pulse_lengthes)
            # print(numbers)   

            # Poll for acknowledgement
            while self.ser.in_waiting == 0:
                continue

            # Send data if acknowledgement received
            if self.ser.read() == b'A':
                self.ser.write(numbers)
                self.ser.flush()
                dur = time.time() - start
                time.sleep(np.clip((1/self.com_frequency)-dur-0.005, 0, (1/self.com_frequency)))#50Hz

    # The function below control the end effector
    def gripper_open(self):
        #modify the robot state
        self.robotstate_gripper_close = False

        #send out the command
        #convert the joint_pose to pulse length
        joint_pulse_lengthes = self.angle_to_pulse_length(self.robotstate_joint_poses)

        #add one more byte in the pulse length array to as gripper command
        if self.robotstate_gripper_close:
            joint_pulse_lengthes = np.append(joint_pulse_lengthes,self.gripper_pulse_close)
        else:
            joint_pulse_lengthes = np.append(joint_pulse_lengthes,self.gripper_pulse_open)
        # print(joint_pulse_lengthes)
        numbers = self.pulse_length_to_byte(joint_pulse_lengthes)
        # print(numbers)   

        # Poll for acknowledgement
        while self.ser.in_waiting == 0:
            continue

        # Send data if acknowledgement received
        if self.ser.read() == b'A':
            self.ser.write(numbers)
            self.ser.flush()

    def gripper_close(self):
        #modify the robot state
        self.robotstate_gripper_close = True
        #send out the command
        #convert the joint_pose to pulse length
        joint_pulse_lengthes = self.angle_to_pulse_length(self.robotstate_joint_poses)

        #add one more byte in the pulse length array to as gripper command
        if self.robotstate_gripper_close:
            joint_pulse_lengthes = np.append(joint_pulse_lengthes,self.gripper_pulse_close)
        else:
            joint_pulse_lengthes = np.append(joint_pulse_lengthes,self.gripper_pulse_open)
        # print(joint_pulse_lengthes)
        numbers = self.pulse_length_to_byte(joint_pulse_lengthes)
        # print(numbers)   

        # Poll for acknowledgement
        while self.ser.in_waiting == 0:
            continue

        # Send data if acknowledgement received
        if self.ser.read() == b'A':
            self.ser.write(numbers)
            self.ser.flush()

    def move_end_effector_by(self, dx=0, dy=0, dz=0, speed=80):
        """
        Move the end effector by the specified increments in X, Y, and Z directions.
        
        Args:
            dx: Increment in X direction (mm)
            dy: Increment in Y direction (mm)
            dz: Increment in Z direction (mm)
            speed: Joint speed in degrees/second
        
        Returns:
            bool: True if the movement was successful, False otherwise
        """
        if not hasattr(self, 'matlab_engine'):
            print("MATLAB engine not initialized. Cannot perform inverse kinematics.")
            return False
        
        try:
            # Convert current joint angles to radians for MATLAB
            current_joint_angles_rad = np.deg2rad(self.robotstate_joint_poses)
            matlab_joint_angles = matlab.double(current_joint_angles_rad.tolist())
            
            # Use workspace variables to handle data conversion more reliably
            self.matlab_engine.workspace['joints'] = matlab_joint_angles
            self.matlab_engine.eval("T = robot_FK(joints);", nargout=0)
            self.matlab_engine.eval("pos = T.T_0T6(1:3, 4);", nargout=0)
            
            # Get the position as a proper MATLAB array
            matlab_position = self.matlab_engine.workspace['pos']
            
            # Extract the values from the MATLAB array directly
            x = float(matlab_position[0][0])
            y = float(matlab_position[1][0]) 
            z = float(matlab_position[2][0])
            
            # Calculate desired position by adding increments
            desired_x = x + dx
            desired_y = y + dy
            desired_z = z + dz
            
            # Create MATLAB array for desired position
            matlab_desired_position = matlab.double([[desired_x], [desired_y], [desired_z]])
            
            # Call IK function to get new joint angles
            self.matlab_engine.workspace['target_pos'] = matlab_desired_position
            self.matlab_engine.workspace['initial_joints'] = matlab_joint_angles
            self.matlab_engine.eval("new_joints = robot_IK(target_pos, initial_joints);", nargout=0)
            new_joint_angles_rad = self.matlab_engine.workspace['new_joints']
            
            # Convert to numpy array and then to degrees, ensuring proper shape
            # Fix the shape mismatch by converting to a flat array first
            new_joint_angles = np.array(new_joint_angles_rad).flatten()
            new_joint_angles_deg = np.rad2deg(new_joint_angles)
            
            # Make sure it matches the expected shape for joints_goto
            if new_joint_angles_deg.shape != self.robotstate_joint_poses.shape:
                new_joint_angles_deg = new_joint_angles_deg[:self.joint_num]
            
            # Move the robot to the new joint positions
            speeds = np.ones(self.joint_num) * speed
            self.joints_goto(new_joint_angles_deg, speeds)
            
            return True
        
        except Exception as e:
            print(f"Error in inverse kinematics calculation: {e}")
            return False