import numpy as np
# Local modules
from constants import DEFAULT_N0, DEFAULT_N1, DEFAULT_N2, NO_INTERSECTION
from normal_map import NormalMap
import utils


class Object:
    """
    Represent a generic object inside the scene that has a specific position,
    material and intersect function.

    Attributes:
        position(numpy.array): A 3D point that represents the position
        material(Material): The material to be rendered for this object
        shader_type(string): The type of shader to use for this object
        ID(int): The index inside the scene
        normal_map(NormalMap): An object that allows you to get normals mapping
            points of the object to a texture
    """

    def __init__(self, position, material, shader_type):
        self.position = position
        self.material = material
        self.shader_type = shader_type
        self.ID = None
        self.normal_map = None

    def set_id(self, idx):
        self.ID = idx

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

    def add_normal_map(self, texture):
        self.normal_map = NormalMap(texture, self)


class Sphere(Object):
    """
    Represent a Sphere object to be used in a scene.

    Attributes:
        position(numpy.array): A 3D point inside the plane
        material(Material): The material to be rendered for this object
        shader_type(string): The type of shader to use for this object
        radius(float): The radius of this sphere
        rotation(numpy.array) Rotation in x, y and z (in grads?).
    """

    def __init__(
            self, position, material, shader_type, radius, rotation=np.zeros(3)
    ):
        Object.__init__(self, position, material, shader_type)
        self.radius = radius
        self.rotation = rotation

    def __str__(self):
        return "r: {}, pc: {}, rot: {}".format(
            self.radius, self.position, self.rotation
        )

    def normal_at(self, p):
        # This doesn't validate that p is in the surface
        if self.normal_map:
            return self.normal_map.get_normal(p)
        return (p - self.position) / float(self.radius)

    def physical_normal_at(self, p):
        return (p - self.position) / float(self.radius)

    def rotate_x(self, v):
        theta = self.rotation[0]
        rot_mat = np.array([
            [1, 0, 0],
            [0, np.cos(theta), -np.sin(theta)],
            [0, np.sin(theta), np.cos(theta)]
        ])
        rotated_v = np.dot(rot_mat, v)
        return rotated_v

    def rotate_y(self, v):
        theta = self.rotation[1]
        rot_mat = np.array([
            [np.cos(theta), 0, np.sin(theta)],
            [0, 1, 0],
            [-np.sin(theta), 0, np.cos(theta)]
        ])
        rotated_v = np.dot(rot_mat, v)
        return rotated_v

    def rotate_z(self, v):
        theta = self.rotation[2]
        rot_mat = np.array([
            [np.cos(theta), -np.sin(theta), 0],
            [np.sin(theta), np.cos(theta), 0],
            [0, 0, 1]
        ])
        rotated_v = np.dot(rot_mat, v)
        return rotated_v

    def get_orientation(self):
        """
        Get the perpendicular unit vectors n0, n1, n2 that define the
        orientation of this object
        """
        # Only work with rotation around x by now
        n0 = DEFAULT_N0
        n1 = DEFAULT_N1
        if self.rotation[2] != 0.0:
            n0 = self.rotate_z(n0)
            n1 = self.rotate_z(n1)
        return n0, n1, DEFAULT_N2

    def uvmap(self, p):
        """
        Map this point into texture coordinates u, v.

        Args:
            p(numpy.array): Point inside this object that will be transformed
                into texture coordinates (u, v)

        Returns:
            tuple: Point (u, v) in texture coordinates
        """
        # local_v is the unit vector that goes in the direction from the center
        # of the sphere to the position p
        local_v = (p - self.position) / self.radius
        n0, n1, n2 = self.get_orientation()
        x = np.dot(n0, local_v)
        y = np.dot(n1, local_v)
        z = np.dot(n2, local_v)
        # phi = np.arccos(z)
        # v = phi / np.pi
        # theta = np.arccos((y / np.sin(phi)).round(4))
        # if x < 0:
        #     theta = 2 * np.pi - theta
        # u = theta / (2 * np.pi)
        u = 0.5 + np.arctan2(z, x) / (2 * np.pi)
        v = 0.5 - np.arcsin(y) / np.pi
        v = 1 - v
        return u, v

    def intersect_sphere_np(self, pr, nr):
        pc = self.position
        dif = pr - pc
        b = np.dot(nr, dif)
        c = np.dot(dif, dif) - self.radius ** 2
        discriminant = b ** 2 - c
        t = -1 * b - np.sqrt(discriminant)
        return np.where(b > 0 or discriminant < 0, NO_INTERSECTION, t)


class HollowSphere(Sphere):
    def normal_at(self, p):
        # This doesn't validate that p is in the surface
        if self.normal_map:
            return self.normal_map.get_normal(p)
        return -super().physical_normal_at(p)

    def physical_normal_at(self, p):
        return -super().physical_normal_at(p)


class Plane(Object):
    """
    Represent a Plane object to be used in a scene.

    Attributes:
        position(numpy.array): A 3D point inside the plane
        material(Material): The material to be rendered for this object
        shader_type(string): The type of shader to use for this object
        n(numpy.array): The unit normal for this plane
        n0(numpy.array): One of the unit directors inside the plane
        sx(float): Scale in x of the plane
        sy(float): Scale in y of the plane
    """

    def __init__(self, position, material, shader_type, n, n0, sx=1, sy=1):
        Object.__init__(self, position, material, shader_type)
        # Making sure n is normalized
        self.n = utils.normalize(n)
        # Make sure n0 is normalized
        self.n0 = utils.normalize(n0)
        self.sx = sx
        self.sy = sy
        self.n1 = np.cross(self.n0, n)

    def normal_at(self, p):
        # This doesn't validate that p is in the surface
        return self.n

    def uvmap(self, p):
        """
        Map this point into texture coordinates u, v. Position will be in the
        center of the texture and not in the bottom left of the texture.

        Args:
            p(numpy.array): Point inside this object that will be transformed
                into texture coordinates (u, v)

        Returns:
            tuple: Point (u, v) in texture coordinates
        """
        # bottom left corner of the plane
        p00 = self.position - (self.sx * self.n0) / 2 - (self.sy * self.n1) / 2
        dif_vector = p - p00
        u = np.dot(dif_vector, self.n0) / self.sx
        v = np.dot(dif_vector, self.n1) / self.sy
        return u, v


class Triangle(Object):
    """
    Represents a single triangle object to be used inside a scene.

    Attributes:
        v0(Vertex): First of the vertices of this triangle
        v1(Vertex): Second of the vertices of this triangle
        v2(Vertex): Third of the vertices of this triangle
        area(float): The area of this triangle
        n(numpy.array): Geometrical normal calculated using the vertices
    """

    def __init__(self, material, shader_type, v0, v1, v2):
        # Set object position as the center of the triangle
        position = 0.34 * v0.position + 0.33 * v1.position + 0.33 * v2.position
        Object.__init__(self, position, material, shader_type)
        self.v0 = v0
        self.v1 = v1
        self.v2 = v2
        a_v = np.cross(v1.position - v0.position, v2.position - v1.position) / 2
        self.area = np.linalg.norm(a_v)
        self.n = a_v / self.area

    def __str__(self):
        return "v0: {}\nv1: {}\nv2: {}".format(
            self.v0.position, self.v1.position, self.v2.position
        )

    def get_barycentric_coord(self, ph):
        """
        Get the barycentric coordinates s and t for a point ph in world coord.

        Args:
            ph(numpy.array): 3D point in world coordinates

        Returns:
            (float, float): Barycentric coordinates s and t for point ph
        """
        a_v_1 = np.cross(ph - self.v0.position, self.v2.position - ph) / 2
        a_v_2 = np.cross(ph - self.v1.position, self.v0.position - ph) / 2
        s = np.dot(self.n, a_v_1) / self.area
        t = np.dot(self.n, a_v_2) / self.area
        return s, t

    def is_inside(self, p):
        """
        Checks if the point p is inside the triangle.

        Args:
            p(numpy.array): Point in world coordinates

        Returns:
            boolean: whether the point is inside
        """
        s, t = self.get_barycentric_coord(p)
        if 0 <= s <= 1 and 0 <= t <= 1 and s + t <= 1:
            return True
        else:
            return False

    def normal_at(self, p, s=None, t=None):
        if s is None or t is None:
            s, t = self.get_barycentric_coord(p)
        if (
            self.v0.n is not None
            and self.v1.n is not None
            and self.v2.n is not None
        ):
            return (1 - s - t) * self.v0.n + s * self.v1.n + t * self.v2.n
        else:
            return self.n

    def uvmap(self, p, s=None, t=None):
        if s is None or t is None:
            s, t = self.get_barycentric_coord(p)
        u = (1 - s - t) * self.v0.u + s * self.v1.u + t * self.v2.u
        v = (1 - s - t) * self.v0.v + s * self.v1.v + t * self.v2.v
        return u, v


class Tetrahedron(Object):
    """
     Represents a tetrahedron object to be used inside a scene.

    Attributes:
        mtl(Material): The material for this object
        shd_type(str): The shader type for this object
        tr0(Triangle): First of the triangles of this tetrahedron
        tr1(Triangle): Second of the triangles of this tetrahedron
        tr2(Triangle): Third of the triangles of this tetrahedron
        tr3(Triangle): Fourth of the triangles of this tetrahedron
    """
    def __init__(self, mtl, shd_type, v0, v1, v2, v3):
        position = (
            0.25 * v0.position
            + 0.25 * v1.position
            + 0.25 * v2.position
            + 0.25 * v3.position
        )
        Object.__init__(self, position, mtl, shd_type)
        self.tr0 = Triangle(mtl, shd_type, v0, v1, v2)
        self.tr1 = Triangle(mtl, shd_type, v3, v2, v1)
        self.tr2 = Triangle(mtl, shd_type, v0, v2, v3)
        self.tr3 = Triangle(mtl, shd_type, v3, v1, v0)

    def __str__(self):
        return "tr0:\n{}\ntr1:\n{}\ntr2:\n{}\ntr3:\n{}".format(
            self.tr0, self.tr1, self.tr2, self.tr3
        )

    def normal_at(self, p):
        if self.tr0.is_inside(p):
            return self.tr0.n
        if self.tr1.is_inside(p):
            return self.tr1.n
        if self.tr2.is_inside(p):
            return self.tr2.n
        if self.tr3.is_inside(p):
            return self.tr3.n
        raise ValueError(
            "Point {} doesn't belong to Tetrahedron {}".format(
                p, self
            )
        )

    def get_triangles(self):
        return [self.tr0, self.tr1, self.tr2, self.tr3]


# THIS IS NOT WORKING
class Cube(Object):
    def __init__(
            self, mtl, shd_type, v1, side_length,
            n0=DEFAULT_N0, n1=DEFAULT_N1, n2=DEFAULT_N2
    ):
        position = v1 + (n0 + n1 + n2) * (side_length / 2)
        Object.__init__(self, position, mtl, shd_type)
        self.v1 = v1
        self.n0 = n0
        self.n1 = n1
        self.n2 = n2
        self.s = side_length
        self.define_vertices()
        self.define_triangles()

    def define_vertices(self):
        self.v2 = self.v1 + self.n2 * self.s
        self.v3 = self.v1 + self.n1 * self.s
        self.v4 = self.v1 + self.n1 * self.s + self.n2 * self.s
        self.v5 = self.v1 + self.n0 * self.s
        self.v6 = self.v1 + self.n0 * self.s + self.n2 * self.s
        self.v7 = self.v1 + self.n0 * self.s + self.n1 * self.s
        self.v8 = self.v7 + self.n2 * self.s

    def define_triangles(self):
        mtl = self.material
        shd_type = self.shader_type
        self.t1 = Triangle(mtl, shd_type, self.v1, self.v7, self.v5)
        self.t2 = Triangle(mtl, shd_type, self.v1, self.v3, self.v7)
        self.t3 = Triangle(mtl, shd_type, self.v1, self.v4, self.v3)
        self.t4 = Triangle(mtl, shd_type, self.v1, self.v2, self.v4)
        self.t5 = Triangle(mtl, shd_type, self.v3, self.v8, self.v7)
        self.t6 = Triangle(mtl, shd_type, self.v3, self.v4, self.v8)
        self.t7 = Triangle(mtl, shd_type, self.v5, self.v7, self.v8)
        self.t8 = Triangle(mtl, shd_type, self.v5, self.v8, self.v6)
        self.t9 = Triangle(mtl, shd_type, self.v1, self.v5, self.v6)
        self.t10 = Triangle(mtl, shd_type, self.v1, self.v6, self.v2)
        self.t11 = Triangle(mtl, shd_type, self.v2, self.v6, self.v8)
        self.t12 = Triangle(mtl, shd_type, self.v2, self.v8, self.v4)

    def __str__(self):
        return "Cube: v1={} s={} n0={} n1={} n2={}".format(
            self.v1, self.s, self.n0, self.n1, self.n2
        )

    def get_triangles(self):
        return [
            self.t1, self.t2, self.t3, self.t4, self.t5, self.t6, self.t7,
            self.t8, self.t9, self.t10, self.t11, self.t12
        ]

    def normal_at(self, p):
        triangles = self.get_triangles()
        for triangle in triangles:
            if triangle.is_inside(p):
                return triangle.n
        raise ValueError(
            "Point {} doesn't belong to Cube {}".format(
                p, self
            )
        )
