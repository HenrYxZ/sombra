import numpy as np
import utils
# Local Modules
from object import Sphere


class Camera:
    """
    Camera object
    """

    def __init__(
        self, position, vview, vup, d=0.035, scale_x=1, scale_y=1
    ):
        self.position = position
        self.vview = vview
        self.vup = vup
        self.d = d
        self.scale_x = scale_x
        self.scale_y = scale_y
        self.calculate_view_coords()

    def calculate_view_coords(self):
        """
        This are the unit vectors that form the view coordinates of the camera.
        Including the starting point of the view window on world coordinates.
        This information allows for projecting a point in the camera window
        into the world coordinates.
        """
        self.n0 = utils.normalize(np.cross(self.vview, self.vup))
        self.n1 = utils.normalize(np.cross(self.n0, self.vview))
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
                if np.dot(dif, dif) < (obj.radius ** 2):
                    return True
        return False
