import math
import numpy as np
# Local modules
import utils


MAX_DISTANCE_LIGHT = np.inf


class Light:
    """
    Light for a Scene.

    Attributes:
        position(numpy.array): 3D position of the light
    """

    def __init__(self, position):
        self.position = position

    def get_dist(self, ph):
        """
        Get distance from the light to the point ph.

        Args:
            ph(numpy.array): 3D point of hit between ray and object

        Returns:
            float: distance from the light to the point ph
        """
        dist = np.linalg.norm(self.position - ph)
        return dist

    def get_l(self, ph):
        """
        Get unit vector l that points to the light from hit point ph.

        Args:
            ph(numpy.array): 3D point of hit between ray and object

        Returns:
            numpy.array: unit vector pointing to the light
        """
        l = np.array([0, 1, 0], dtype=float)
        return l


class DirectionalLight(Light):
    """
    Directional Light for a scene.
    """

    def get_dist(self, ph):
        """
        Get distance from the light to the point ph.

        Args:
            ph(numpy.array): 3D point of hit between ray and object

        Returns:
            float: distance from the light to the point ph
        """
        return MAX_DISTANCE_LIGHT

    def get_l(self, ph):
        """
        Get unit vector l that points to the light from hit point ph.

        Args:
            ph(numpy.array): 3D point of hit between ray and object

        Returns:
            numpy.array: unit vector pointing to the light
        """
        l = utils.normalize(-1 * self.position)
        return l


class PointLight(Light):
    """
    Point Light for a scene.
    """

    def get_l(self, ph):
        """
        Get unit vector l that points to the light from hit point ph.

        Args:
            ph(numpy.array): 3D point of hit between ray and object

        Returns:
            numpy.array: unit vector pointing to the light
        """
        l = utils.normalize(self.position - ph)
        return l


class SpotLight(Light):
    """
    Spot Light for a Scene.

    Attributes:
        position(numpy.array): 3D position of the light
        theta(float): The angle for directional light in radians
        nl(numpy.array): Unit vector in the direction of the spot light
        cos_theta(float): Value for cos(theta), used for calculations
    """

    def __init__(self, position, theta=0, nl=None):
        Light.__init__(self, position)
        self.theta = theta
        self.nl = nl
        self.cos_theta = math.cos(theta)

    def get_l(self, ph):
        """
        Get unit vector l that points to the light from hit point ph.

        Args:
            ph(numpy.array): 3D point of hit between ray and object

        Returns:
            numpy.array: unit vector pointing to the light, 0 if outside cone
        """
        l = utils.normalize(self.position - ph)
        # This light won't illuminate if the point is outside the cone
        if np.dot(-1 * l, self.nl) < self.cos_theta:
            l = np.zeros(3)
        return l
