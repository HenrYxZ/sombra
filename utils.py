import numpy as np


def normalize(v):
    """
    Normalize a vector using numpy.

    Args:
        v(array): Input vector

    Returns:
        array: Normalized input vector
    """
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm


def degree2radians(degrees):
    return (degrees / 360) * 2 * np.pi


# class Position(object):
#     """Position in 3D space"""
#
#     def __init__(self, x=0, y=0, z=0):
#         self.x = x
#         self.y = y
#         self.z = z
#         self.data = np.array([x, y, z])
