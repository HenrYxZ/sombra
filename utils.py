import numpy as np
import time

# Local imports
import constants
from material import Material
import material


MTL_DIFFUSE_BLUE = Material(material.COLOR_BLUE, material.TYPE_DIFFUSE)


def normalize(arr):
    """
    Normalize a vector using numpy.

    Args:
        arr(ndarray): Input vector

    Returns:
        ndarray: Normalized input vector
    """
    norm = np.linalg.norm(arr)
    if norm == 0:
        return arr
    return arr / norm


def distance(p1, p2):
    """
    Get the distance between points p1 and p2
    Args:
        p1(ndarray): Point 1
        p2(ndarray): Point 2
    Returns:
         float: Distance
    """
    dist = np.linalg.norm(p1 - p2)
    return dist


def humanize_time(secs):
    """
    Extracted from http://testingreflections.com/node/6534
    """
    mins, secs = divmod(secs, 60)
    hours, mins = divmod(mins, 60)
    return '%02d:%02d:%02d' % (hours, mins, secs)


def degree2radians(degrees):
    return (degrees / float(360)) * 2 * np.pi


def random_unit_vector():
    # 3D random vector
    v = np.random.random_sample(3)
    v_unit = normalize(v)
    return v_unit


def rotate_x(v, theta):
    rot_mat = np.array([
        [1, 0, 0],
        [0, np.cos(theta), -np.sin(theta)],
        [0, np.sin(theta), np.cos(theta)]
    ])
    rotated_v = np.dot(rot_mat, v)
    return rotated_v


def blerp(img_arr, x, y):
    # Interpolate values of pixel neighborhood of x and y
    i = int(np.round(x))
    j = int(np.round(y))
    # But not in the borders
    height, width, _ = img_arr.shape
    if i == 0 or j == 0 or i == width or j == height:
        if i == width:
            i -= 1
        if j == height:
            j -= 1
        return img_arr[j][i]
    # t and s are interpolation parameters that go from 0 to 1
    t = x - i + 0.5
    s = y - j + 0.5
    # Bilinear interpolation
    color = (
        img_arr[j - 1][i - 1] * (1 - t) * (1 - s)
        + img_arr[j - 1][i] * t * (1 - s)
        + img_arr[j][i - 1] * (1 - t) * s
        + img_arr[j][i] * t * s
    )
    return color


def color_matching(color):
    xyz = np.zeros(3)
    # Exception for color in RGB
    if len(color) == 3:
        new_color_matching = np.array([
            constants.COLOR_MATCHING[constants.RGB_INDEX[0]],
            constants.COLOR_MATCHING[constants.RGB_INDEX[1]],
            constants.COLOR_MATCHING[constants.RGB_INDEX[2]]
        ])
        for i in range(len(color)):
            intensity = color[i]
            xyz[0] += intensity * new_color_matching[i][1]
            xyz[1] += intensity * new_color_matching[i][2]
            xyz[2] += intensity * new_color_matching[i][3]
    else:
        for i in range(len(color)):
            intensity = color[i]
            xyz[0] += intensity * constants.COLOR_MATCHING[i][1]
            xyz[1] += intensity * constants.COLOR_MATCHING[i][2]
            xyz[2] += intensity * constants.COLOR_MATCHING[i][3]
    return xyz


def xyz_to_rgb(color):
    rgb_color = np.matmul(constants.XYZ_TO_RGB, color)
    rgb_color = np.clip(rgb_color, 0, 1)
    return rgb_color


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
