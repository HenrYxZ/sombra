import numpy as np


def diffuse(n, l, material):
    """
    Shader calculation for a normal and a light vector.
    Args:
        n(numpy.array): Unit normal vector
        l(numpy.array): Unit vector in the direction to the light
    Returns:
        numpy.array: The calculated color (grayscale 0-255)
    """
    diffuse_coef = np.dot(n, l)
    color = np.maximum(0, diffuse_coef) * material
    return color
