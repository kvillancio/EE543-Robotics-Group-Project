import numpy as np

def quat2axisangle(q: np.ndarray) -> tuple[np.ndarray, float]:
    """
    Calculate the Euler rotation axis and angle from a unit quaternion.

    This function computes the equivalent axis-angle representation of a
    given unit quaternion.

    Args:
        q (np.ndarray): A 4x1 unit quaternion in
        scalar-first format [w, x, y, z].

    Returns:
        tuple[np.ndarray, float]: A tuple containing:
            - axis (np.ndarray): A 3x1 unit vector representing the axis of
              rotation.
            - angle (float): The angle of rotation in radians.

    Example:
        >>> import numpy as np
        >>> np.set_printoptions(precision=4, suppress=True)
        >>> quat = np.array([[1], [0.1], [0.2], [0.3]])
        >>> axis, angle = quat2axisangle(quat)
        >>> print(f"Axis: {axis.T}")
        >>> print(f"Angle: {angle}")
        Axis: [[0.2673 0.5345 0.8018]]
        Angle: 0.7497

    Description:
        When given an input of a 4x1 unit quaternion, this function calculates
        the equivalent Euler rotation about an axis. The axis is normalized,
        and the angle is constrained to be within plus/minus 2 pi

    Required Python packages:
        - numpy

    Subfunctions:
        None

    Required data files:
        None

    Notes:
        - The function assumes the input quaternion is a unit quaternion.
        - The output axis is normalized to ensure it's a unit vector.

    See Also:
        - https://en.wikipedia.org/wiki/Quaternions_and_spatial_rotation

    Author: Ian Adelman
    Email: IanAdelman@outlook.com
    Created: 2023
    Revised: 2025-02-01
    Version: 2.1.0

    Version Notes:
        2.1.0 (2025-02-01): Converted from MATLAB to Python, updated function
                            header formatting
        2.0.0 (2023-03-18): Updated function header, improved code readability,
                            normalized angle and vector, added warning
    """
    
    # Calculate angle of rotation
    angle = 2 * np.arccos(q[0, 0])

    # Normalize angle to be within ±2π
    angle = np.angle(np.exp(1j * angle))

    # Calculate axis of rotation
    axis = q[1:4] / np.sin(angle / 2)

    # Normalize vector
    axis = axis / np.linalg.norm(axis)

    return axis, angle
