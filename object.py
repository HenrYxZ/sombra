OBJ_TYPE_SPHERE = "sphere"


class Object(object):
    """
    Represent a generic object inside the scene that has a specific position
    and intersect function
    """

    def __init__(self, position):
        super(Object, self).__init__()
        self.position = position


class Sphere(Object):
    """
    Represent a Sphere object to be used in a scene.
    """

    def __init__(self, position, radius):
        super(Sphere, self).__init__(position)
        self.radius = radius
        self.type = OBJ_TYPE_SPHERE
