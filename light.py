import math

POINT_LIGHT = "point"
DIRECTIONAL_LIGHT = "directional"
SPOT_LIGHT = "spot"


class Light:
    """
    Light for a Scene.

    Attributes:
        position(numpy.array): 3D position of the light
        type(str): The type of this light
        theta(float): The angle for directional light in radians
        nl(numpy.array): Unit vector in the direction of the spot light
    """

    def __init__(self, position, type, theta=0, nl=None):
        self.position = position
        self.type = type
        self.theta = theta
        self.nl = nl
        self.cos_theta = math.cos(theta)