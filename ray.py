import numpy as np
# Local modules
from object import OBJ_TYPE_SPHERE


class Ray:
    """
    Ray object that is used for raytracing. It has an intersect function to get
    the intersection of the ray and a given object.

    Attr:
        pr: Origin point of the Ray
        nr: Director vector for the ray.
    """

    def __init__(self, pr, nr):
        self.pr = pr
        self.nr = nr

    def at(self, t):
        """
        Get the point in the ray at position t
        """
        return self.pr + t * self.nr

    def intersect(self, obj):
        """
        Find t of intersection, -1 value means no intersection.
        """
        if obj.type == OBJ_TYPE_SPHERE:
            # Sphere center point
            pc = obj.position
            dif = self.pr - pc
            b = np.dot(self.nr, dif)
            c = np.dot(dif, dif) - obj.radius ** 2
            discriminant = b ** 2 - c
            if b > 0 or discriminant < 0:
                return -1
            t = -1 * b - np.sqrt(discriminant)
            return t
        else:
            return -1
