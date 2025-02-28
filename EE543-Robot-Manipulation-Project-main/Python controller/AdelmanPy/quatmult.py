import numpy as np
import warnings

def quatmult(qA: np.ndarray, qB: np.ndarray) -> np.ndarray:
    """
    Multiply two unit quaternions to create a combined rotation quaternion.

    This function calculates the product of two unit quaternions, representing
    the composition of their rotations in 3D space.

    Args:
        qA (np.ndarray): 4x1 unit quaternion (scalar-first format)
        qB (np.ndarray): 4x1 unit quaternion (scalar-first format)

    Returns:
        np.ndarray: 4x1 combined unit quaternion (scalar-first format)

    Example:
        >>> import numpy as np
        >>> q_1 = np.array([[1], [np.pi/2], [np.pi/2], [np.pi/2]])
        >>> q_2 = np.array([[1], [np.pi/2], [np.pi/2], [np.pi/2]])
        >>> q_12 = quatmult(q_1, q_2)
        >>> print(q_12)
        [[...]
         [...]
         [...]
         [...]]

    Description:
        Implements the Hamilton product for quaternion multiplication using
        matrix representation. Input quaternions must be in scalar-first
        format (w, x, y, z).

    Required Python packages:
        - numpy
        - warnings

    Subfunctions:
        None

    Required data files:
        None

    Notes:
        - Input quaternions are assumed to be unit quaternions
        - Quaternions must be provided as column vectors
        - Uses Hamilton product convention

    See Also:
        - https://en.wikipedia.org/wiki/Quaternion#Hamilton_product

    Author: Ian Adelman
    Email: IanAdelman@outlook.com
    Created: 2022
    Revised: 2025-02-01
    Version: 2.0.0

    Version Notes:
        2.0.0 (2025-02-01): Converted from MATLAB to Python, added
                            normalization and warning
        1.0.0 (2023-03-18): Initial MATLAB version
    """
    
    # Construct quaternion multiplication matrix
    Q = np.array([
        [qA[0,0], -qA[1,0], -qA[2,0], -qA[3,0]],
        [qA[1,0],  qA[0,0], -qA[3,0],  qA[2,0]],
        [qA[2,0],  qA[3,0],  qA[0,0], -qA[1,0]],
        [qA[3,0], -qA[2,0],  qA[1,0],  qA[0,0]]
    ])
    
    # Perform matrix multiplication
    qAB = Q @ qB
    
    # Normalize output quaternion (handles numerical drift)
    if not np.isclose(np.linalg.norm(qAB), 1.0, atol=1e-6):
        warnings.warn(
            "Significant normalization required - check input quaternions")

    
    # Normalize output quaternion
    qAB /= np.linalg.norm(qAB)
    
    return qAB
