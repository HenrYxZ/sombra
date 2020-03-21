import numpy as np
from PIL import Image
import time
# Local Modules
from camera import Camera
from light import Light, POINT_LIGHT
from material import Material
import material
from object import Plane, Sphere
from render import render, render_no_aa
from scene import Scene
import utils

# Width and Height of the image window in pixels
WIDTH = 200
HEIGHT = 200
# Vertical and Horizontal Samples for Random Jitter Anti Aliasing
V_SAMPLES = 4
H_SAMPLES = 4
MAX_QUALITY = 95
OUTPUT_IMG_FILENAME = "output.jpg"


def setup_scene():
    main_camera_pos = np.array([0, 0, 0])
    vview = np.array([0, 0, 1])
    vup = np.array([0, 1, 0])
    main_camera = Camera(main_camera_pos, vview, vup)
    light_pos = np.array([0, 50, 50])
    light = Light(light_pos, POINT_LIGHT)
    plane_position = np.array([0, -25, 0])
    plane_material = Material(material.COLOR_GRAY, material.DIFFUSE)
    plane_normal = np.array([0, 1, 0])
    plane = Plane(plane_position, plane_material, plane_normal)
    sphere_position = np.array([0, 0, 100])
    sphere_material = Material(material.COLOR_BLUE, material.DIFFUSE)
    sphere_radius = 25
    sphere = Sphere(sphere_position, sphere_material, sphere_radius)
    objects = [sphere, plane]
    scene = Scene([main_camera], [light], objects)
    return scene


def main():
    start = time.time()
    print("Setting up...")
    scene = setup_scene()
    print("Raytracing...")
    img_arr = render(
        scene, scene.cameras[0], HEIGHT, WIDTH, V_SAMPLES, H_SAMPLES
    )
    img = Image.fromarray(img_arr)
    img.save(OUTPUT_IMG_FILENAME, quality=MAX_QUALITY)
    print("Rendered image saved in {}".format(OUTPUT_IMG_FILENAME))
    end = time.time()
    time_spent = utils.humanize_time(end - start)
    print("Total time spent: {}".format(time_spent))


if __name__ == '__main__':
    main()
