import numpy as np

DIFFUSE = "diffuse"
# Color values are not in uint8 so just make sure to clip everything to uint8
# when rendering the final image
COLOR_BLUE = np.array([10, 10, 230], dtype=float)
COLOR_GRAY = np.array([135, 135, 135], dtype=float)


class Material:
    def __init__(self, diffuse=COLOR_GRAY, type=DIFFUSE, specular=1, border=1):
        self.diffuse = diffuse
        self.type = type
        self.specular = specular
        self.border = border
