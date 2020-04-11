import numpy as np
from texture import ImageTexture


def uvmap(n):
    # Custom n0, n1, n2 axis definition
    n0 = np.array([1, 0, 0])
    n1 = np.array([0, 1, 0])
    n2 = np.array([0, 0, 1])
    x = np.dot(n0, n)
    y = np.dot(n1, n)
    z = np.dot(n2, n)
    # phi = np.arccos(z)
    # theta = np.arccos((y / np.sin(phi)).round(4))
    # u = theta / (2 * np.pi)
    # v = phi / np.pi
    # if x < 0:
    #     u = 1 - u
    u = 0.5 + np.arctan2(z, x) / (2 * np.pi)
    v = 0.5 - np.arcsin(y) / np.pi
    v = 1 - v
    return u, v


class EnvironmentMap:

    def __init__(self, img_filename):
        self.img_texture = ImageTexture(img_filename)

    def get_color(self, n):
        u, v = uvmap(n)
        return self.img_texture.get_color(u, v)
