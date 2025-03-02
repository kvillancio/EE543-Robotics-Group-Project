#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 19:16:19 2025

@author: ian
"""

import numpy as np
from robot_FK import FK

# Set numpy print options to display 3 significant figures
np.set_printoptions(precision=3, suppress=True)

# Define the joint angles for the robot (all set to 0 for this test)
gamma = np.array([0, 0, 0, 0, 0])

# Perform forward kinematics to get the transformation matrices
T = FK(gamma)

# Print the final transformation matrix
print(f"Final transformation matrix T:\n{T}\n")