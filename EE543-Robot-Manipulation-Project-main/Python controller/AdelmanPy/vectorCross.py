# -*- coding: utf-8 -*-
import numpy as np

def vector_cross(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """
    Calculate the cross product of two 3D vectors.

    This function computes the cross product of two 3D vectors using
    the right-hand rule. The result is a vector perpendicular to both
    input vectors.

    Version: 1.1.0

    Args:
        a (np.ndarray): A 3x1 vector.
        b (np.ndarray): A 3x1 vector.

    Returns:
        np.ndarray: A 3x1 vector representing the cross product of a and b.

    Raises:
        ValueError: If either input vector does not have exactly 3 elements.

    Example:
        >>> import numpy as np
        >>> a = np.array([1, 0, 0])
        >>> b = np.array([0, 1, 0])
        >>> result = vector_cross(a, b)
        >>> print(result)
        [0 0 1]

    Required Python packages:
        - numpy

    Subfunctions:
        None

    Required data files:
        None

    Notes:
        - The function assumes input vectors are numpy arrays.
        - The cross product is anti-commutative: a × b = -(b × a).

    See Also:
        - https://en.wikipedia.org/wiki/Cross_product

    Author: Ian Adelman
    Email: IanAdelman@outlook.com
    Created: 2025-01-10
    Revised: 2025-01-11
    Version: 1.1.0

    Version Notes:
        1.1.0 (2025-01-11): Added comprehensive documentation, type hints, 
                            and PEP 8 compliance including header formatting
                            with help from perplexity
        1.0.0 (2025-01-10): Initial implementation
        
    """
    # Vectors must both have 3 elements
    if (len(a) != 3) or (len(b) != 3):
        raise ValueError("Both vectors must have 3 elements")

    # Calculate cross product
    return np.array([
        a[1]*b[2] - a[2]*b[1],
        a[2]*b[0] - a[0]*b[2],
        a[0]*b[1] - a[1]*b[0]
    ])
