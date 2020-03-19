class Object:
    """
    Represent a generic object inside the scene that has a specific position
    and intersect function
    """

    def __init__(self, position, material):
        self.position = position
        self.material = material


class Sphere(Object):
    """
    Represent a Sphere object to be used in a scene.
    """

    def __init__(self, position, material, radius):
        Object.__init__(self, position, material)
        self.radius = radius
