import math
import numpy as np
# Local modules
from constants import DEFAULT_N0, DEFAULT_N1
import utils


MAX_DISTANCE_LIGHT = np.inf
# Default horizontal and vertical number of samples for area lights
AREA_LIGHT_M = 6
AREA_LIGHT_N = 6
#


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


class AreaLight(Light):
    """
    Area Light for a Scene.

    Attributes:
        position(numpy.array): Center of the area light
        s0(float): width of area light in world coordinates
        s1(float): height of area light in world coordinates
        n0(numpy.array): Unit vector for horizontal direction
        n1(numpy.array): Unit vector for vertical direction
        p00(numpy.array): Origin point for area light
    """

    def __init__(self, position, s0, s1, n0=DEFAULT_N0, n1=DEFAULT_N1):
        Light.__init__(self, position)
        self.s0 = s0
        self.s1 = s1
        self.n0 = n0
        self.n1 = n1
        self.p00 = position - (float(s0) / 2) * n0 - (float(s1) / 2) * n1

    def get_l(self, ph):
        """
        Get unit vector l that points to a random sample inside the area from
            hit point ph.

        Args:
            ph(numpy.array): 3D point of hit between ray and object

        Returns:
            numpy.array: unit vector pointing to random sample
        """
        r0, r1 = np.random.random_sample(2)
        x = r0 * self.s0
        y = r1 * self.s1
        p = self.p00 + x * self.n0 + y * self.n1
        l = utils.normalize(p - ph)
        return l

    def get_samples(self, m=AREA_LIGHT_M, n=AREA_LIGHT_N):
        """
        Get sample points from the area light dividing the area m horizontally
        and n vertically and using random jitter.

        Args:
            m(int): Number of horizontal samples to use
            n(int): Number of vertical samples to use

        Returns:
            list of numpy.array: sample positions in world space
        """
        samples = []
        for i in range(m):
            for j in range(n):
                r0, r1 = np.random.random_sample(2)
                x = ((i + r0) / m) * self.s0
                y = ((j + r1) / n) * self.s1
                p = self.p00 + x * self.n0 + y * self.n1
                samples.append(p)
        return samples
