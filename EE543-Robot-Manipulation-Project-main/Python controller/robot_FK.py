#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 18:10:21 2025

@author: ian
"""

import numpy as np
import AdelmanPy as ap

def FK(theta):
    """
    Calculate the forward kinematics for the project robot.

    Args:
        theta (np.ndarray): A 5x1 vector of joint angles [theta1, theta2, theta3, theta4, theta5].

    Returns:
        T (np.ndarray): Homogeneous transormation matrix from base to end-effector.
    """
    
    # Link lengths
    l1 = .23
    l2 = .12
    l3 = .53
    l4 = .12
    l5 = .19

    # DH parameters [a, alpha, d, theta]
    DH = [
        [             0, l1,  0, theta[0]],
        [np.deg2rad(90), l2,  0, theta[1]],
        [             0, l3,  0, theta[2]],
        [np.deg2rad(90),  0, l4, theta[3]],
        [             0,  0, l5,        0]
    ]

    # Initialize transformation matrices
    T_0T1 = ap.DH2T([0, 0, 0, 0], DH[0])
    T_1T2 = ap.DH2T(DH[0], DH[1])
    T_2T3 = ap.DH2T(DH[1], DH[2])
    T_3T4 = ap.DH2T(DH[2], DH[3])
    T_4T5 = ap.DH2T(DH[3], DH[4])
    # Store all transformation matrices
    T_matrices = {
        'T_0T1': T_0T1,
        'T_1T2': T_1T2,
        'T_2T3': T_2T3,
        'T_3T4': T_3T4,
        'T_4T5': T_4T5
    }

    # Calculate all transformation matrices with respect to frame zero
    T_0T2 = T_0T1 @ T_1T2
    T_0T3 = T_0T2 @ T_2T3
    T_0T4 = T_0T3 @ T_3T4
    T_0T5 = T_0T4 @ T_4T5

    T_matrices_zero = {
        'T_0T1': T_0T1,
        'T_0T2': T_0T2,
        'T_0T3': T_0T3,
        'T_0T4': T_0T4,
        'T_0T5': T_0T5
    }

    # Return the results
    return T_matrices, T_matrices_zero



