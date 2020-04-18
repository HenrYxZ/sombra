import unittest
import numpy as np
# Local modules
from object import Triangle
from vertex import Vertex
import shaders
import utils


class TriangleTestCase(unittest.TestCase):
    def setUp(self):
        self.v0 = Vertex(np.array([-1.0, 0.0, 0.0]))
        self.v1 = Vertex(np.array([1.0, 0.0, 0.0]))
        self.v2 = Vertex(np.array([0.0, 1.0, 0.0]))
        self.triangle = Triangle(
            utils.MTL_DIFFUSE_BLUE,
            shaders.TYPE_DIFFUSE_COLORS,
            self.v0,
            self.v1,
            self.v2
        )

    def test_barycentric_coordinates(self):
        s, t = self.triangle.get_barycentric_coord(self.v0.position)
        self.assertEqual(s, 0)
        self.assertEqual(t, 0)
        s, t = self.triangle.get_barycentric_coord(self.v1.position)
        self.assertEqual(s, 1)
        self.assertEqual(t, 0)
        s, t = self.triangle.get_barycentric_coord(self.v2.position)
        self.assertEqual(s, 0)
        self.assertEqual(t, 1)
        ph = self.v1.position * 0.7 + self.v2.position * 0.3
        s, t = self.triangle.get_barycentric_coord(ph)
        self.assertAlmostEqual(s, 0.7)
        self.assertAlmostEqual(t, 0.3)


if __name__ == '__main__':
    unittest.main()
