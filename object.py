class Object:
    """
    Represent a generic object inside the scene that has a specific position,
    material and intersect function.

    Attributes:
        position(numpy.array): A 3D point that represents the position
        material(Material): The material to be rendered for this object
        shader_type(string): The type of shader to use for this object
    """

    def __init__(self, position, material, shader_type):
        self.position = position
        self.material = material
        self.shader_type = shader_type

    def normal_at(self, p):
        """
        Get the normal at point p.
        """
        return None


class Sphere(Object):
    """
    Represent a Sphere object to be used in a scene.

    Attributes:
        position(numpy.array): A 3D point inside the plane
        material(Material): The material to be rendered for this object
        radius(float): The radius of this sphere
    """

    def __init__(self, position, material, shader_type, radius):
        Object.__init__(self, position, material, shader_type)
        self.radius = radius

    def normal_at(self, p):
        # This doesn't validate that p is in the surface
        return (p - self.position) / float(self.radius)


class Plane(Object):
    """
    Represent a Plane object to be used in a scene.

    Attributes:
        position(numpy.array): A 3D point inside the plane
        material(Material): The material to be rendered for this object
        n(numpy.array): The normal for this plane
    """

    def __init__(self, position, material, shader_type, n):
       Object.__init__(self, position, material, shader_type)
       self.n = n

    def normal_at(self, p):
        # This doesn't validate that p is in the surface
        return self.n
