import unittest
# Local Modules
from factories import object_factory, ray_factory


class SphereTestCase(unittest.TestCase):
    def test_intersect(self):
        # Get rays
        r1 = ray_factory.create_intersecting()
        r2 = ray_factory.create_intersecting2()
        r3 = ray_factory.create_non_intersecting()
        rays = [r1, r2, r3]
        # TODO Put rays into an array
        pr = map(lambda r: r.pr, rays)
        nr = map(lambda r: r.nr, rays)
        sphere = object_factory.create_sphere()
        distances = sphere.intersect_sphere_np(pr, nr)
        # Intersect them to Sphere
        for i in range(len(rays)):
            self.assertEqual(rays[i].intersect(sphere), distances[i])


if __name__ == '__main__':
    unittest.main()
