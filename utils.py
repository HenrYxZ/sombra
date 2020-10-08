import numpy as np
import time

# Local imports
from material import Material
import material


MTL_DIFFUSE_BLUE = Material(material.COLOR_BLUE, material.TYPE_DIFFUSE)


def normalize(arr):
    """
    Normalize a vector using numpy.

    Args:
        arr(darray): Input vector

    Returns:
        darray: Normalized input vector
    """
    norm = np.linalg.norm(arr)
    if norm == 0:
        return arr
    return arr / norm


def humanize_time(secs):
    """
    Extracted from http://testingreflections.com/node/6534
    """
    mins, secs = divmod(secs, 60)
    hours, mins = divmod(mins, 60)
    return '%02d:%02d:%02f' % (hours, mins, secs)


def degree2radians(degrees):
    return (degrees / float(360)) * 2 * np.pi


def random_unit_vector():
    # 3D random vector
    v = np.random.random_sample(3)
    v_unit = normalize(v)
    return v_unit


class Timer:
    def __init__(self):
        self.start_time = 0
        self.end_time = 0
        self.elapsed_time = 0

    def start(self):
        self.start_time = time.time()

    def stop(self):
        self.end_time = time.time()
        self.elapsed_time = self.end_time - self.start_time

    def __str__(self):
        return humanize_time(self.elapsed_time)

# class Position(object):
#     """Position in 3D space"""
#
#     def __init__(self, x=0, y=0, z=0):
#         self.x = x
#         self.y = y
#         self.z = z
#         self.data = np.array([x, y, z])
