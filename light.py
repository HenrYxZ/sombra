import math


class Light:
    """
    Light for a Scene.

    Attributes:
        position(numpy.array): 3D position of the light
    """

    def __init__(self, position):
        self.position = position


class DirectionalLight(Light):
    """
    Directional Light for a scene.

    Attributes:
        position(numpy.array): 3D direction of the light
    """
    pass


class PointLight(Light):
    """
    Point Light for a scene.

    Attributes:
        position(numpy.array): 3D position of the light
    """
    pass


class SpotLight:
    """
    Spot Light for a Scene.

    Attributes:
        position(numpy.array): 3D position of the light
        theta(float): The angle for directional light in radians
        nl(numpy.array): Unit vector in the direction of the spot light
        cos_theta(float): Value for cos(theta), used for calculations
    """

    def __init__(self, position, theta=0, nl=None):
        self.position = position
        self.theta = theta
        self.nl = nl
        self.cos_theta = math.cos(theta)
