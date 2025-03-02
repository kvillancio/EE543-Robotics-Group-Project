# -*- coding: utf-8 -*-
import numpy as np
from AdelmanPy.rotx import rotx

def Hrotx(phi: float) -> np.ndarray:
    """
    Convert a rotation angle (radians) about the X-axis into a 4x4 homogeneous
    transformation matrix (HTM).

    This function calculates the homogeneous transformation matrix
    corresponding to a rotation of 'phi' radians about the X-axis. The
    translation components are set to zero.

    Version: 3.0.0

    Args:
        phi (float): The rotation angle in radians.

    Returns:
        np.ndarray: A 4x4 array representing the homogeneous rotation matrix.

    Example:
        >>> import numpy as np
        >>> np.set_printoptions(precision=4, suppress=True)
        >>> angle = np.pi/2
        >>> HTM = Hrotx(angle)
        >>> print(HTM)
        [[ 1.     0.     0.     0.    ]
         [ 0.     0.    -1.     0.    ]
         [ 0.     1.     0.     0.    ]
         [ 0.     0.     0.     1.    ]]

    Required Python packages:
        - numpy

    Subfunctions:
        None

    Required data files:
        None

    Notes:
        - The rotation follows the right-hand rule.
        - This function requires my rotx function which should be present in
          this module.

    See Also:
        - rotx
        - https://en.wikipedia.org/wiki/Homogeneous_coordinates
        - https://en.wikipedia.org/wiki/Transformation_matrix

    Author: Ian Adelman
    Email: IanAdelman@outlook.com
    Created: 2022
    Revised: 2025-01-25
    Version: 3.1.0

    Version Notes:
        3.1.0 (2025-01-25): Translated function to python
        3.0.0 (2024-11-14): Made variable names and format consistent 
        2.0.0 (2023-03-18): Updated function header, improved code readability
    """

    return np.block([[rotx(phi), np.zeros((3,1))], [np.zeros((1,3)), 1]])