"""
Example that generates an image of a sphere and two planes with a flat color
(no lighting).
"""
import numpy as np
from PIL import Image

# Local Modules
from camera import Camera
from constants import RGB_CHANNELS
from material import Material, COLOR_BLUE, COLOR_GREEN
from object import Plane, Sphere
from scene import Scene
import shaders

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
NO_INTERSECTION = -1


def set_camera():
    camera_pos = np.zeros(3)
    v_view = np.array([0.0, 0.0, 1.0])
    v_up = np.array([0.0, 1.0, 0.0])
    return Camera(camera_pos, v_view, v_up)


def set_scene():
    n0 = np.array([1.0, 0.0, 0.0])
    n = np.array([0.0, 1.0, 0.0])
    pos = np.array([0.0, 0.0, 1.0])
    mat = Material()
    plane_1 = Plane(pos, mat, shaders.TYPE_FLAT, n, n0)
    n0 = np.array([1.0, 0.0, 0.0])
    n = np.array([0.0, 0.0, -1.0])
    pos = np.array([0.0, 0.0, 1.0])
    mat = Material(COLOR_GREEN)
    plane_2 = Plane(pos, mat, shaders.TYPE_FLAT, n, n0)
    pos = np.array([0.0, 0.25, 0.6])
    mat = Material(COLOR_BLUE)
    radius = 0.25
    sphere = Sphere(pos, mat, shaders.TYPE_FLAT, radius)
    cameras = [set_camera()]
    return Scene(cameras, [], [plane_1, plane_2, sphere])


def intersect_sphere_np(sphere, pr, nr):
    pc = sphere.position
    dif = pr - pc
    b = np.dot(nr, dif)
    c = np.dot(dif, dif) - sphere.radius ** 2
    discriminant = b ** 2 - c
    t = -1 * b - np.sqrt(discriminant)
    return np.where(b > 0 or discriminant < 0, NO_INTERSECTION, t)


def main():
    screen = np.zeros(
        [SCREEN_HEIGHT, SCREEN_WIDTH, RGB_CHANNELS], dtype=np.uint8
    )
    scene = set_scene()


if __name__ == '__main__':
    main()
