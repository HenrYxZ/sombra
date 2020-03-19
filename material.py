import numpy as np

DIFFUSE = "diffuse"
# Color values are not in uint8 so just make sure to clip everything to uint8
# when rendering the final image
COLOR_BLUE = np.array([10, 10, 230])
COLOR_GRAY = np.array([135, 135, 135])


class Material:
    def __init__(self, diffuse, type):
        self.diffuse = diffuse
        self.type = type