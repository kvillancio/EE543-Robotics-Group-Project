# -*- coding: utf-8 -*-
import numpy as np

def vector_magnitude(vector: np.ndarray) -> float:
    """
    Calculate the magnitude (Euclidean norm) of a vector.

    This function computes the magnitude of an input vector using the
    Euclidean norm (L2 norm).

    Version: 1.1.0

    Args:
        vector (np.ndarray): n-dimensional numpy array of input vector.

    Returns:
        float: The magnitude (length) of the input vector.

    Example:
        >>> import numpy as np
        >>> v = np.array([3, 4])
        >>> magnitude = vector_magnitude(v)
        >>> print(f"The magnitude is: {magnitude:.4f}")
        The magnitude is: 5.0000

    Description:
        The function calculates the square root of the sum of the squares
        of all elements in the input vector.

    Required Python packages:
        - numpy

    Subfunctions:
        None

    Required data files:
        None

    Notes:
        - This function works for vectors of any dimension.
        - For very large vectors, consider using np.linalg.norm for better
          numerical stability.

    See Also:
        - https://en.wikipedia.org/wiki/Euclidean_vector#Length

    Author: Ian Adelman
    Email: IanAdelman@outlook.com
    Created: 2025-01-11
    Revised: 2025-01-12
    Version: 1.1.0

    Version Notes:
        1.1.0 (2025-01-11): Added comprehensive documentation, type hints, and
                            PEP 8 compliance, including header formatting with
                            help from perplexity
        1.0.0 (2025-01-11): Initial implementation
    """
    
    sum_of_squares = np.sum(vector**2)
    magnitude = np.sqrt(sum_of_squares)
    return magnitude
