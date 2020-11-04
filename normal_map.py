import numpy as np
# Local Modules
from constants import MAX_COLOR_VALUE
from texture import ImageTexture, SolidImageTexture
import utils


class NormalMap:
    def __init__(self, texture, obj):
        self.texture = texture
        self.obj = obj

    def get_normal(self, p):
        if isinstance(self.texture, ImageTexture):
            u, v = self.obj.uvmap(p)
            color = self.texture.get_color(u, v)
        else:
            color = self.texture.get_color(p)
        r, g, b = color[:3]
        # x and y will be from [-1 to 1] and z from [0 to 1]
        x = 2 * (r / np.float(MAX_COLOR_VALUE)) - 1
        y = 2 * (g / np.float(MAX_COLOR_VALUE)) - 1
        z = (b / float(MAX_COLOR_VALUE))
        normal_vector = np.array([x, y, z])
        normal_vector = utils.normalize(normal_vector)
        local_diff = normal_vector - np.array([0, 0, 1])
        final_normal = self.obj.physical_normal_at(p) + local_diff
        return final_normal
