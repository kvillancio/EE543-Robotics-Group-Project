#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 18:10:21 2025

@author: ian
"""

import numpy as np
import AdelmanPy as ap


def FK(gamma):
    """
    Calculate the forward kinematics of a 5 rotary joint robot using DH convention.

    Args:
        gamma (np.ndarray): A 5x1 vector of joint angles [theta1, theta2, theta3, theta4, theta5].

    Returns:
        np.ndarray: A 4x4 homogeneous transformation matrix representing the end-effector pose.
    """
    
    # Placeholder DH parameters [a, alpha, d, theta]
    dh_params = [
        [1, 0, 0, gamma[0]],  # Joint 1
        [1, np.pi/2, 0, gamma[1]],  # Joint 2
        [1, 0, 0, gamma[2]],  # Joint 3
        [1, 0, 0, gamma[3]],  # Joint 4
        [1, 0, 0, gamma[4]]  # Joint 5
    ]

    # Initialize transformation matrix
    T = np.eye(4)

    # Initialize a list to store individual transformation matrices
    T_matrices = []

    # Compute the transformation matrix for each joint
    for a, alpha, d, theta in dh_params:
        # Compute the transformation matrix for the current joint
        T_joint = ap.Hrotx(alpha) @ ap.Hroty(theta) @ ap.Hrotz(a) @ np.array([[1, 0, 0, d], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
        # Update the overall transformation matrix
        T = T @ T_joint
        # Store the current joint's transformation matrix
        T_matrices.append(T_joint)

    # T is the final transformation matrix representing the end-effector pose
    # T_matrices is a list of individual transformation matrices for each joint
    # T_matrices should have 5 elements, one for each joint
    return T, T_matrices





