import numpy as np
from PIL import Image
import sys, getopt
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
    main_camera_pos = np.array([0, 0, 0], dtype=float)
    vview = np.array([0, 0, 1], dtype=float)
    vup = np.array([0, 1, 0], dtype=float)
    main_camera = Camera(main_camera_pos, vview, vup)
    light_pos = np.array([0, 50, 50], dtype=float)
    light = Light(light_pos, POINT_LIGHT)
    plane_position = np.array([0, -25, 0], dtype=float)
    plane_material = Material(material.COLOR_GRAY, material.DIFFUSE)
    plane_normal = np.array([0, 1, 0], dtype=float)
    plane = Plane(plane_position, plane_material, plane_normal)
    sphere_position = np.array([0, 0, 100], dtype=float)
    sphere_material = Material(material.COLOR_BLUE, material.DIFFUSE)
    sphere_radius = 25.0
    sphere = Sphere(sphere_position, sphere_material, sphere_radius)
    objects = [sphere, plane]
    scene = Scene([main_camera], [light], objects)
    return scene


def main(argv):
    debug_mode = False
    try:
        opts, args = getopt.getopt(argv, "hd", ["help", "debug"])
    except getopt.GetoptError:
        print 'usage: main.py [-d,-h|--debug,--help]'
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print 'usage: main.py [-d,-h|--debug,--help]'
            sys.exit()
        elif opt in ('-d', '--debug'):
            debug_mode = True
    start = time.time()
    print("Setting up...")
    scene = setup_scene()
    print("Raytracing...")
    if debug_mode:
        img_arr = render_no_aa(scene, scene.cameras[0], HEIGHT, WIDTH)
    else:
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
    main(sys.argv[1:])
