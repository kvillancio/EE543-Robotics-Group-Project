import numpy as np

def rotq(q: np.ndarray) -> np.ndarray:
    """
    Convert a quaternion to a direction cosine matrix (DCM).

    This function computes the 3x3 direction cosine matrix (DCM) corresponding
    to the input quaternion.

    Args:
        q (np.ndarray): A 4x1 quaternion in scalar-first format
                        [q0, q1, q2, q3].

    Returns:
        np.ndarray: A 3x3 numpy array representing the Direction Cosine Matrix

    Example:
        >>> import numpy as np
        >>> np.set_printoptions(precision=4, suppress=True)
        >>> q = np.array([[1], [0], [0], [0]])  # Identity quaternion
        >>> dcm = rotq(q)
        >>> print(dcm)
        [[ 1.  0.  0.]
         [ 0.  1.  0.]
         [ 0.  0.  1.]]

    Description:
        This function converts a quaternion to a direction cosine matrix (DCM).
        The DCM is a 3x3 rotation matrix that describes the orientation of an
        object in 3D space.

    Required Python packages:
        - numpy

    Subfunctions:
        None

    Required data files:
        None

    Notes:
        - The input quaternion is assumed to be in scalar-first format
          [q0, q1, q2, q3].
        - The function uses the standard quaternion-to-DCM conversion formula.

    See Also:
        - https://en.wikipedia.org/wiki/Quaternions_and_spatial_rotation#Conversion_to_and_from_the_matrix_representation

    Author: Ian Adelman
    Email: IanAdelman@outlook.com
    Created: 2023
    Revised: 2025-02-01
    Version: 2.1.0

    Version Notes:
        2.1.0 (2025-02-01): Converted from MATLAB to Python, updated function
                            header formatting
        2.0.0 (2023-02-11): Original MATLAB version
    """
    
    q0, q1, q2, q3 = q.flatten()
    
    dcm = np.array([
        [2*q0**2 - 1 + 2*q1**2, 2*q1*q2 - 2*q0*q3, 2*q1*q3 + 2*q0*q2],
        [2*q1*q2 + 2*q0*q3, 2*q0**2 - 1 + 2*q2**2, 2*q2*q3 - 2*q0*q1],
        [2*q1*q3 - 2*q0*q2, 2*q2*q3 + 2*q0*q1, 2*q0**2 - 1 + 2*q3**2]
    ])
    
    return dcm
