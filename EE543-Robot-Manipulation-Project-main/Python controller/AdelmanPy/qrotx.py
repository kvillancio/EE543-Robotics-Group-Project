import numpy as np

def qrotx(angle: float) -> np.ndarray:
    """
    Calculate the quaternion representation of a rotation around the x-axis.

    This function computes the quaternion corresponding to a rotation of
    'angle' radians around the x-axis.

    Args:
        angle (float): The angle of rotation in radians.

    Returns:
        np.ndarray: A 4x1 numpy array representing the quaternion in
                    scalar-first format [w, x, y, z].

    Example:
        >>> import numpy as np
        >>> np.set_printoptions(precision=4, suppress=True)
        >>> angle = np.pi/4
        >>> q = qrotx(angle)
        >>> print(q)
        [[ 0.9239]
         [ 0.3827]
         [ 0.    ]
         [ 0.    ]]

    Description:
        This function calculates the quaternion representation of a rotation
        around the x-axis. The quaternion is returned in scalar-first format.

    Required Python packages:
        - numpy

    Subfunctions:
        None

    Required data files:
        None

    Notes:
        - The quaternion is normalized to ensure it represents a valid rotation

    See Also:
        - https://en.wikipedia.org/wiki/Quaternions_and_spatial_rotation

    Author: Ian Adelman
    Email: IanAdelman@outlook.com
    Created: 2023-04-01
    Revised: 2025-02-01
    Version: 2.0.0

    Version Notes:
        2.0.0 (2025-02-01): Converted from MATLAB to Python, updated function
                            header formatting
        1.5.0 (2023-03-18): updated header, increased readability
        1.0.0 (2022)
    """
    
    q = np.array([[np.cos(angle/2)],
                  [np.sin(angle/2)],
                  [0],
                  [0]])
    
    return q
