import numpy as np
# Local Modules
from factories.constants import DEFAULT_POSITION, DEFAULT_RADIUS
from ray import Ray
import utils

LARGE_DISTANCE = 9999999


def create_intersecting():
    pr = np.array([DEFAULT_POSITION[0], DEFAULT_POSITION[1], 0])
    nr = np.array([0, 0, 1])
    return Ray(pr, nr)


def create_intersecting2():
    pr = np.array([DEFAULT_POSITION[0], DEFAULT_POSITION[1], 0])
    y = DEFAULT_POSITION[1] - DEFAULT_RADIUS
    nr = utils.normalize(
        np.array([
            DEFAULT_POSITION[0], y, DEFAULT_POSITION[2]
        ])
    )
    return Ray(pr, nr)


def create_non_intersecting():
    pr = np.array([DEFAULT_POSITION[0], DEFAULT_POSITION[1], 0])
    nr = utils.normalize(np.array([0, LARGE_DISTANCE, 1]))
    return Ray(pr, nr)


def create_inside():
    pr = DEFAULT_POSITION
    nr = np.array([0, 0, 1])
    return Ray(pr, nr)
