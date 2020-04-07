import numpy as np


def env_map(n):
    # Custom n0, n1, n2 axis definition
    n0 = np.array([0, 0, 1])
    n1 = np.array([1, 0, 0])
    n2 = np.array([0, -1, 0])
    x = np.dot(n0, n)
    y = np.dot(n1, n)
    z = np.dot(n2, n)
    phi = np.arccos(z)
    theta = np.arccos((y / np.sin(phi)).round(4))
    u = theta / (2 * np.pi)
    v = phi / np.pi
    if x < 0:
        u = 1 - u
    return u, v