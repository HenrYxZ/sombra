import getopt
import numpy as np
from PIL import Image
import sys
import time
# Local Modules
from camera import Camera
from env_map import EnvironmentMap
from light import DirectionalLight, PointLight, SpotLight
from material import Material
import material
from object import Plane, Sphere, Tetrahedron, Triangle
from render import render, render_no_aa
from scene import Scene
import shaders
from texture import ImageTexture, SolidImageTexture, Box
import utils
from vertex import Vertex

# Width and Height of the image window in pixels
WIDTH = 280
HEIGHT = 192
# Vertical and Horizontal Samples for Random Jitter Anti Aliasing
V_SAMPLES = 4
H_SAMPLES = 4
MAX_QUALITY = 95
DEFAULT_KS = 0.8
DEFAULT_THICKNESS = 0.7
EARTH_TEXTURE_FILENAME = "textures/earth.jpg"
CHECKERS_TEXTURE_FILENAME = "textures/checkers.png"
MICKEY_TEXTURE_FILENAME = "textures/mickey.jpg"
PARK_TEXTURE_FILENAME = "textures/autumn_park.jpg"
OUTPUT_IMG_FILENAME = "output.jpg"


def default_vertex(p, n):
    return Vertex(p, material.COLOR_BLUE, shaders.TYPE_DIFFUSE_COLORS, n)


def setup_cameras():
    main_camera_pos = np.array([0, 0, 0], dtype=float)
    vview = np.array([0, 0, 1], dtype=float)
    vup = np.array([0, 1, 0], dtype=float)
    main_camera = Camera(main_camera_pos, vview, vup)
    return [main_camera]


def setup_lights():
    # Directional Light
    # directional_light = DirectionalLight(np.array([-1, -1, 1]))
    # Point Light
    light_pos = np.array([0, 50, 50], dtype=float)
    point_light = PointLight(light_pos)
    # Spot Light
    # nl = utils.normalize(np.array([0, -0.5, 1]))
    # theta = utils.degree2radians(30)
    # spot_light = SpotLight(light_pos, theta, nl)
    return [point_light]


def setup_objects():
    # Plane Object
    plane_pos = np.array([0, -25, 0], dtype=float)
    plane_n0 = np.array([1, 0, 0], dtype=float)
    plane_mtl = Material(material.COLOR_GRAY, material.TYPE_DIFFUSE)
    plane_shader = shaders.TYPE_DIFFUSE_COLORS
    plane_normal = np.array([0, 1, 0], dtype=float)
    # plane_texture = ImageTexture(CHECKERS_TEXTURE_FILENAME)
    # plane_mtl.add_texture(plane_texture)
    plane_sx = 250
    plane_sy = 250
    plane = Plane(
        plane_pos,
        plane_mtl,
        plane_shader,
        plane_normal,
        plane_n0,
        plane_sx,
        plane_sy
    )
    # Sphere Object
    # sphere_pos = np.array([0, 0, 100], dtype=float)
    # sphere_mtl = Material(
    #     material.COLOR_BLUE,
    #     material.TYPE_TEXTURED,
    #     DEFAULT_KS,
    #     DEFAULT_THICKNESS
    # )
    # sphere_texture = ImageTexture(EARTH_TEXTURE_FILENAME)
    # sphere_mtl.add_texture(sphere_texture)
    # sphere_shader = shaders.TYPE_DIFF_SPECULAR
    # sphere_r = 25.0
    # sphere = Sphere(sphere_pos, sphere_mtl, sphere_shader, sphere_r)
    # El Mickey Shhiiino
    # mickey_pos = np.array([-50, 0, 100], dtype=float)
    # mickey_r = 20.0
    # mickey_mtl = Material(material.COLOR_BLUE, material.TYPE_TEXTURED)
    # mickey_img_texture = ImageTexture(MICKEY_TEXTURE_FILENAME)
    # mickey_p0 = mickey_pos - np.array([mickey_r, mickey_r, mickey_r])
    # mickey_s = mickey_r * 2
    # n0 = np.array([0, 0, 1])
    # n1 = np.array([0, 1, 0])
    # n2 = np.array([1, 0, 0])
    # mickey_box = Box(mickey_p0, mickey_s, mickey_s, mickey_s, n0, n1, n2)
    # mickey_texture = SolidImageTexture(mickey_img_texture, mickey_box)
    # mickey_mtl.add_texture(mickey_texture)
    # mickey_shader = shaders.TYPE_DIFF_SPECULAR
    # mickey = Sphere(mickey_pos, mickey_mtl, mickey_shader, mickey_r)
    # Triangle
    # n = np.array([0, 0, -1])
    # v0 = default_vertex(np.array([-30, -15, 55]), n)
    # v1 = default_vertex(np.array([30, -15, 55]), n)
    # v2 = default_vertex(np.array([0, 35, 55]), n)
    # triangle = Triangle(
    #     utils.MTL_DIFFUSE_BLUE, shaders.TYPE_DIFFUSE_COLORS, v0, v1, v2
    # )
    # Tetrahedron
    v0 = Vertex(np.array([-30, -10, 80], dtype=float))
    v1 = Vertex(np.array([0, 20, 80], dtype=float))
    v2 = Vertex(np.array([30, -10, 80], dtype=float))
    v3 = Vertex(np.array([0, 0, 60], dtype=float))
    tetrahedron = Tetrahedron(
        utils.MTL_DIFFUSE_BLUE, shaders.TYPE_DIFFUSE_COLORS, v0, v1, v2, v3
    )
    return [tetrahedron, plane]


def setup_scene():
    cameras = setup_cameras()
    lights = setup_lights()
    objects = setup_objects()
    # env_map = EnvironmentMap(PARK_TEXTURE_FILENAME)
    # scene = Scene(cameras, lights, objects, env_map)
    scene = Scene(cameras, lights, objects)
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
