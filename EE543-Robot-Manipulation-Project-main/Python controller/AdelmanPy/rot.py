# -*- coding: utf-8 -*-
import numpy as np


def rot(axis: np.ndarray, angle: float) -> np.ndarray:
    """
    Calculate the Direction Cosine Matrix (DCM) representation from Euler
    axis and angle.

    This function computes the 3x3 rotation matrix corresponding to a rotation
    of 'angle' radians around the specified 'axis'.

    Version: 2.1.0

    Args:
        axis (np.ndarray): A 3x1 unit position vector representing the axis
        of rotation. angle (float): The angle of rotation in radians.

    Returns:
        np.ndarray: A 3x3 numpy array representing the Direction Cosine
                    Matrix (DCM).

    Example:
        >>> import numpy as np
        >>> np.set_printoptions(precision=4, suppress=True)
        >>> axis = np.array([1, 0, 0])
        >>> angle = np.pi/2
        >>> DCM = rot(axis, angle)
        >>> print(DCM)
        [[ 1.     0.     0.    ]
         [ 0.     0.    -1.    ]
         [ 0.     1.     0.    ]]

    Description:
        When given an input axis of rotation and an angle to rotate through,
        this function returns a 3x3 Direction Cosine Matrix equivalent to
        the input axis-angle rotation.

    Required Python packages:
        - numpy

    Subfunctions:
        None

    Required data files:
        None

    Notes:
        - The input axis vector is normalized before calculations.
        - The function uses the axis-angle rotation formula to compute the DCM.

    See Also:
        - https://en.wikipedia.org/wiki/Rotation_matrix#Rotation_matrix_from_axis_and_angle

    Author: Ian Adelman
    Email: IanAdelman@outlook.com
    Created: 2022
    Revised: 2025-01-11
    Version: 2.1.0

    Version Notes:
        2.1.0 (2025-01-11): Converted from MATLAB to Python, updated function
                            header formatting with help from perplexity
        2.0.0 (2023-03-18): updated function header, improved code readability
    """

    # normalize vector before rotating about it
    axis = axis / np.linalg.norm(axis)

    # define versin(angle)
    versin = 1-np.cos(angle)


    # compute axis-angle rotation matrix
    row1 = np.array([axis[0,0]**2 * versin + np.cos(angle), axis[0,0]*axis[1,0] * versin - axis[2,0]*np.sin(angle), axis[0,0]*axis[2,0]*versin + axis[1,0]*np.sin(angle)])
    row2 = np.array([axis[0,0]*axis[1,0]*versin + axis[2,0]*np.sin(angle), (axis[1,0])**2*versin + np.cos(angle), axis[1,0]*axis[2,0]*versin - axis[0,0]*np.sin(angle) ])
    row3 = np.array([axis[2,0]*axis[0,0]*versin - axis[1,0]*np.sin(angle), axis[1,0]*axis[2,0]*versin + axis[0,0]*np.sin(angle), axis[2,0]**2 * versin + np.cos(angle)])
    
    DCM = np.vstack((row1,row2,row3))
    
    return DCM
