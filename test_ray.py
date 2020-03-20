import numpy as np
import unittest
# Local Modules
from ray import Ray
from object import Plane, Sphere


class RayTestCase(unittest.TestCase):
    def setUp(self):
        pr = np.array([0, 0, 1])
        nr = np.array([0, 0, 1])
        self.ray = Ray(pr, nr)

    def test_intersect_sphere(self):
        # case there is intersection
        sphere_position = np.array([0, 0, 4])
        material = None
        radius = 1
        sphere = Sphere(sphere_position, material, radius)
        t = self.ray.intersect(sphere)
        self.assertEqual(t, 2)
        # cases object is behind
        sphere_position = np.array([0, 0, -4])
        material = None
        radius = 2
        sphere = Sphere(sphere_position, material, radius)
        t = self.ray.intersect(sphere)
        self.assertEqual(t, -1)
        sphere_position = np.array([3, 24, -1])
        material = None
        radius = 0.4
        sphere = Sphere(sphere_position, material, radius)
        t = self.ray.intersect(sphere)
        self.assertEqual(t, -1)
        # case is not in the ray line
        sphere_position = np.array([-3.3, 12.6, 5.2])
        material = None
        radius = 0.4
        sphere = Sphere(sphere_position, material, radius)
        t = self.ray.intersect(sphere)
        self.assertEqual(t, -1)

    def test_intersect_plane(self):
        # Case there is intersection
        p0 = np.array([0, 0, 3])
        n = np.array([0, 0, -1])
        material = None
        plane = Plane(p0, material, n)
        t = self.ray.intersect(plane)
        self.assertEqual(t, 2)
        # Case there is not because it's parallel to the ray
        p0 = np.array([0, -1, 0])
        n = np.array([0, 1, 0])
        plane = Plane(p0, material, n)
        t = self.ray.intersect(plane)
        self.assertEqual(t, -1)
        # Case there is not because it is behind
        p0 = np.array([0, 0, -1])
        n = np.array([0, 0, 1])
        plane = Plane(p0, material, n)
        t = self.ray.intersect(plane)
        self.assertEqual(t, -1)


    def test_at(self):
        self.assertTrue(np.array_equal(self.ray.at(2), np.array([0, 0, 3])))

if __name__ == '__main__':
    unittest.main()
