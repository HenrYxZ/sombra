import numpy as np
import utils
# Local Modules
from object import Plane, Sphere


class Camera:
    """
    Camera object
    """

    def __init__(
        self, position, vview, vup, d=26, scale_x=35, scale_y=24
        # self, position, vview, vup, d=1.6, scale_x=4, scale_y=3
    ):
        self.position = position
        self.vview = vview
        self.vup = vup
        self.d = float(d)
        self.scale_x = float(scale_x)
        self.scale_y = float(scale_y)
        self.set_view_coord()

    def set_view_coord(self):
        """
        This are the unit vectors that form the view coordinates of the camera.
        Including the starting point of the view window on world coordinates.
        This information allows for projecting a point in the camera window
        into the world coordinates.
        """
        self.n0 = utils.normalize(np.cross(self.vup, self.vview))
        self.n1 = utils.normalize(np.cross(self.vview, self.n0))
        self.n2 = utils.normalize(self.vview)
        # Point in the center of the screen of the camera window
        pc = self.position + self.d * self.n2
        self.p00 = (
            pc - (self.scale_x / 2) * self.n0 - (self.scale_y / 2) * self.n1
        )

    def spin(self, degrees):
        pass

    def pan(self, degrees):
        pass

    def tilt(self, degrees):
        pass

    def inside(self, objects):
        """
        Returns true if the camera position is inside any of the objects.
        """
        for obj in objects:
            if isinstance(obj, Sphere):
                dif = self.position - obj.position
                return np.dot(dif, dif) < (obj.radius ** 2)
            if isinstance(obj, Plane):
                return np.dot(self.position - obj.position, obj.n) == 0
        return False
