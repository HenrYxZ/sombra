import numpy as np


MAX_COLOR_VALUE = 255.0
RGB_CHANNELS = 3
DEFAULT_N0 = np.array([1, 0, 0], dtype=float)
DEFAULT_N1 = np.array([0, 1, 0], dtype=float)
DEFAULT_N2 = np.array([0, 0, 1], dtype=float)
MAX_QUALITY = 95
NO_INTERSECTION = -1
# 6 is wavelength index for red, 3 for green and 2 for blue
RGB_INDEX = [6, 3, 2]
COLOR_MATCHING = [
    [400, 0.0143, 0.0004, 0.0679],
    [445, 0.3481, 0.0298, 1.7826],
    [475, 0.1421, 0.1126, 1.0419],
    [510, 0.0093, 0.5030, 0.1582],
    [570, 0.7621, 0.9520, 0.0021],
    [590, 1.0263, 0.7570, 0.0011],
    [650, 0.2835, 0.1070, 0.0000]
]
# XYZ to sRGB color space
XYZ_TO_RGB = np.array([
    [3.2404542, -1.5371385, -0.4985314],
    [-0.9692660, 1.8760108, 0.0415560],
    [0.0556434, -0.2040259, 1.0572252]
])
SUNLIGHT = np.array([750, 1234, 1419, 1395, 1338, 1344, 1289])
RAINBOW_WAVELENGHTS = np.array([400, 445, 475, 510, 570, 590, 650])
