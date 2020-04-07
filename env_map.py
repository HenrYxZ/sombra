import numpy as np


def env_map(n):
    x, y, z = n
    phi = np.arccos(z)
    theta = np.arccos((y / np.sin(phi)).round(4))
    u = theta / (2 * np.pi)
    v = phi / np.pi
    if x < 0:
        u = 1 - u
    return u, v