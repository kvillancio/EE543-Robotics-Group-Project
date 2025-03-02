# -*- coding: utf-8 -*-
import numpy as np

def rotz(psi: float) -> np.ndarray:
    """
    Compute the Direction Cosine Matrix (DCM) for rotation around the Z-axis.

    This function calculates the 3x3 rotation matrix corresponding to
    a rotation of 'psi' radians around the Z-axis.

    Version: 2.1.0

    Args:
        psi (float): The rotation angle in radians.

    Returns:
        np.ndarray: A 3x3 numpy array representing the rotation matrix (DCM).

    Example:
        >>> import numpy as np
        >>> np.set_printoptions(precision=4, suppress=True)
        >>> angle = np.pi/2
        >>> dcm = rotz(angle)
        >>> print(dcm)
        [[ 0.    -1.     0.    ]
         [ 1.     0.     0.    ]
         [ 0.     0.     1.    ]]

    Required Python packages:
        - numpy

    Subfunctions:
        None

    Required data files:
        None

    Notes:
        - The rotation follows the right-hand rule.
        - The matrix is orthogonal, meaning its transpose is its inverse.

    See Also:
        - https://en.wikipedia.org/wiki/Rotation_matrix
        - https://mathworld.wolfram.com/RotationMatrix.html

    Author: Ian Adelman
    Email: IanAdelman@outlook.com
    Created: 2023
    Revised: 2025-01-11
    Version: 2.1.0

    Version Notes:
        2.1.0 (2025-01-11): Converted from MATLAB to Python, updated function
                            header formatting with help from perplexity
        2.0.0 (2023-03-18): updated function header, improved code readability
    """
    
    return np.array([
        [np.cos(psi), -np.sin(psi), 0],
        [np.sin(psi), np.cos(psi), 0],
        [0, 0, 1]
    ])
