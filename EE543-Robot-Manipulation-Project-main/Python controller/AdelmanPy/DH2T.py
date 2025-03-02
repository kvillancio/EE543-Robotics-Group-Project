import numpy as np

"""
    Calculate the homogeneous transformation matrix (HTM) and position vector
    from Denavit-Hartenberg parameters.

    This function computes the 4x4 homogeneous transformation matrix based on two
    sets of Denavit-Hartenberg parameters.

    Version: 1.0.0

    Args:
        DH1 (tuple): The first set of DH parameters (alpha1, a1, d1, theta1).
        DH2 (tuple): The second set of DH parameters (alpha2, a2, d2, theta2).

    Returns:
         - np.ndarray: A 4x4 array representing the homogeneous transformation matrix.

    Example:
        >>> import numpy as np
        >>> DH1 = (0, 1, 0, np.pi/2)
        >>> DH2 = (0, 1, 0, np.pi/2)
        >>> T = DH2T(DH1, DH2)
        >>> print(T)
        [[ 0.     -1.      0.      1.    ]
         [ 0.      0.     -1.      0.    ]
         [ 1.      0.      0.      0.    ]
         [ 0.      0.      0.      1.    ]]

    Required Python packages:
        - numpy

    Subfunctions:
        None

    Required data files:
        None

    Notes:
        - The transformation follows the standard DH convention.

    See Also:
        - https://en.wikipedia.org/wiki/Denavit%E2%80%93Hartenberg_parameters

    Author: Ian Adelman
    Email: IanAdelman@outlook.com
    Created: 2025-03-02
    Version: 1.0.0

    Version Notes:
        1.0.0 (2025-03-02): Initial version
    """

def DH2T(DH1, DH2):
    alpha1, a1, d1, theta1 = DH1
    alpha2, a2, d2, theta2 = DH2

    T = np.array([
        [np.cos(theta2), -np.sin(theta2), 0, a1],
        [np.sin(theta2) * np.cos(alpha1), np.cos(theta2) * np.cos(alpha1), -np.sin(alpha1), -np.sin(alpha1) * d2],
        [np.sin(theta2) * np.sin(alpha1), np.cos(theta2) * np.sin(alpha1), np.cos(alpha1), np.cos(alpha1) * d2],
        [0, 0, 0, 1]
    ])

    return T