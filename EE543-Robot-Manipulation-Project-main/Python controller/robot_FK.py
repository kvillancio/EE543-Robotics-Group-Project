#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 18:10:21 2025

@author: ian
"""

import numpy as np
import AdelmanPy as ap


gamma = np.array([0, np.pi/4, np.pi/4, np.pi/4, np.pi/4])

def FK(gamma):
    """
    Calculate the forward kinematics of a 5 rotary joint robot using DH convention.

    Args:
        gamma (np.ndarray): A 5x1 vector of joint angles [theta1, theta2, theta3, theta4, theta5].

    Returns:
        np.ndarray: A 4x4 homogeneous transformation matrix representing the end-effector pose.
    """
    
    # Re-organize variables
    theta1 = gamma[0]  # base joint
    theta2 = gamma[1]  # joint 1
    theta3 = gamma[2]  # joint 2
    theta4 = gamma[3]  # joint 3
    theta5 = gamma[4]  # grasper angle

    # Placeholder DH parameters [a, alpha, d, theta]
    dh_params = [
        [0, 0, 0, theta1],  # Joint 1
        [0, 0, 0, theta2],  # Joint 2
        [0, 0, 0, theta3],  # Joint 3
        [0, 0, 0, theta4],  # Joint 4
        [0, 0, 0, theta5]   # Joint 5
    ]

    # Initialize transformation matrix
    T = np.eye(4)

    # Compute the transformation matrix for each joint
    for params in dh_params:
        a, alpha, d, theta = params
        T = T @ ap.Hrotx(alpha) @ ap.Hroty(theta) @ ap.Hrotz(a) @ np.array([[1, 0, 0, d], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])

    return T

# Example usage
gamma = np.array([0, np.pi/4, np.pi/4, np.pi/4, np.pi/4])
end_effector_pose = FK(gamma)
print(end_effector_pose)





