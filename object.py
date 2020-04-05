import numpy as np
# Local modules
import utils


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
        pass

    def uvmap(self, p):
        """
        Map point p into texture coordinates u, v for this object.
        """
        pass


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
        n(numpy.array): The unit normal for this plane
        p1(numpy.array): Another point inside this plane
    """

    def __init__(self, position, material, shader_type, n, p1, sx=1, sy=1):
        Object.__init__(self, position, material, shader_type)
        # Making sure n is normalized
        self.n = utils.normalize(n)
        self.p1 = p1
        self.sx = sx
        self.sy = sy
        self.n0 = utils.normalize(p1 - position)
        self.n1 = np.cross(self.n0, n)

    def normal_at(self, p):
        # This doesn't validate that p is in the surface
        return self.n

    def uvmap(self, p):
        """
        Map this point into texture coordinates u, v for this Plane.

        Args:
            p(numpy.array): Point inside this Plane that will be transformed
                into texture coordinates (u, v)

        Returns:
            numpy.array: Point (u, v) in texture coordinates
        """
        dif_vector = p - self.position
        u = np.dot(dif_vector, self.n0) / self.sx
        v = np.dot(dif_vector, self.n1) / self.sy
        texture_coord = np.array([u, v])
        return texture_coord
