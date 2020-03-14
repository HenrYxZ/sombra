import numpy as np
from random import random
# Local Modules
from camera import Camera
from light import Light, POINT_LIGHT
from object import Sphere
from scene import Scene
import utils

# Width and Height of the image window in pixels
WIDTH = 200
HEIGHT = 200
# Vertical and Horizontal Samples for Random Jitter Anti Aliasing
V_SAMPLES = 4
H_SAMPLES = 4


def setup_scene():
    main_camera_pos = np.array([0, 0, -1])
    # quizas esto tenga que ser negativo
    vview = np.array([0, 0, 1])
    vup = np.array([0, 1, 0])
    main_camera = Camera(main_camera_pos, vview, vup)
    light_pos = utils.Position(0, 1.2, 0.5)
    light = Light(light_pos, POINT_LIGHT)
    sphere_position = utils.Position(0, 0.25, 1)
    sphere_radius = 0.25
    sphere = Sphere(sphere_position, sphere_radius)
    scene = Scene([main_camera], [light], [sphere])
    return scene


def raytrace(scene, camera):
    if not scene or not scene.objects or not camera:
        print("Cannot generate an image")
        return
    for j in range(HEIGHT):
        for i in range(WIDTH):
            for n in range(V_SAMPLES):
                for m in range(H_SAMPLES):
                    x = i + (m / H_SAMPLES) + (random() / H_SAMPLES)
                    y = j + (n / V_SAMPLES) + (random() / V_SAMPLES)
                    # Get x projected in view coords
                    xp = (x / WIDTH) * camera.scale_x
                    # Get y projected in view coords
                    yp = (y / HEIGHT) * camera.scale_y
                    pp = camera.p00 + xp * camera.n0 + yp * camera.n1
                    # TODO: now raytrace from this point


def main():
    print("Setting up...")
    scene = setup_scene()
    print("Raytracing...")
    raytrace(scene, scene.cameras[0])


if __name__ == '__main__':
    main()
