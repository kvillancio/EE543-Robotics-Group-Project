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
T, T_matrices = FK(gamma)

# Print each transformation matrix
for i, T_matrix in enumerate(T_matrices):
    print(f"T_matrix {i+1}:\n{T_matrix}\n")

# Print the final transformation matrix
print(f"Final transformation matrix T:\n{T}\n")