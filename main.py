import getopt
import numpy as np
from PIL import Image
import sys
import time
# Local Modules
from animation import Animation
from camera import Camera
from env_map import EnvironmentMap
from light import DirectionalLight, PointLight, SpotLight
import log
from material import Material
import material
from normal_map import NormalMap
from object import Cube, Plane, Sphere, Tetrahedron, Triangle
from render import render, render_no_aa, render_mp
from scene import Scene
import shaders
from texture import ImageTexture, SolidImageTexture, Box
import utils
from vertex import Vertex

# Width and Height of the image window in pixels
WIDTH = 288
HEIGHT = 192
# WIDTH = 1280
# HEIGHT = 720
# Vertical and Horizontal Samples for Random Jitter Anti Aliasing
V_SAMPLES = 4
H_SAMPLES = 4
MAX_QUALITY = 95
DEFAULT_KS = 0.8
DEFAULT_THICKNESS = 0.7
CHECKERS_TEXTURE_FILENAME = "textures/checkers.png"
COIN_TEXTURE_FILENAME = "textures/ten pence heads normal.png"
EARTH_TEXTURE_FILENAME = "textures/earth.jpg"
EARTH_HD_TEXTURE_FILENAME = "textures/hd_earth.jpg"
GARAGE_TEXTURE_FILENAME = "textures/garage_1k.jpg"
HALL_TEXTURE_FILENAME = "textures/music_hall_01.jpg"
MICKEY_TEXTURE_FILENAME = "textures/mickey.jpg"
MOON_TEXTURE_FILENAME = "textures/024-night-time-lighting-moonsky-03.jpg"
NORMAL_TEXTURE_FILENAME = "textures/normal.jpg"
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
    plane_mtl = Material(
        material.COLOR_GRAY, material.TYPE_TEXTURED, kr=0.4, roughness=0.05
    )
    plane_shader = shaders.TYPE_DIFFUSE_COLORS
    plane_normal = np.array([0, 1, 0], dtype=float)
    plane_texture = ImageTexture(CHECKERS_TEXTURE_FILENAME)
    plane_mtl.add_texture(plane_texture)
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
    sphere_pos = np.array([-50, 0, 100], dtype=float)
    sphere_mtl = Material(
        material.COLOR_BLUE,
        material.TYPE_TEXTURED,
        specular=DEFAULT_KS
    )
    sphere_mtl.add_texture(ImageTexture(EARTH_HD_TEXTURE_FILENAME))
    sphere_shader = shaders.TYPE_DIFF_SPECULAR
    sphere_r = 25.0
    sphere = Sphere(sphere_pos, sphere_mtl, sphere_shader, sphere_r)
    return [sphere, plane]


def set_objects_id(objects):
    for i in range(len(objects)):
        objects[i].set_id(i)


def setup_scene():
    cameras = setup_cameras()
    lights = setup_lights()
    objects = setup_objects()
    set_objects_id(objects)
    env_map = EnvironmentMap(HALL_TEXTURE_FILENAME)
    scene = Scene(cameras, lights, objects, env_map)
    # scene = Scene(cameras, lights, objects)
    return scene


def animate(debug_mode, render_function, duration, screen_size, fps, scene):
    # duration in seconds
    render_function = render_no_aa if debug_mode else render_function
    animation = Animation(duration, screen_size, fps, scene, render_function)
    sphere = scene.objects[0]
    main_camera = scene.cameras[0]
    animation.create(sphere, main_camera)


def main(argv):
    debug_mode = False
    animation_mode = False
    multi_core = False
    try:
        opts, args = getopt.getopt(
            argv, "hdam", ["help", "debug", "animation", "multi"]
        )
    except getopt.GetoptError:
        print('usage: main.py [-d,-h,-a, m|--debug,--help,--animation, --multi]')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print('usage: main.py [-d,-h|--debug,--help]')
            sys.exit()
        elif opt in ('-d', '--debug'):
            debug_mode = True
        elif opt in ('-a', '--animation'):
            animation_mode = True
        elif opt in ('-m', '--multi'):
            multi_core = True
    start = time.time()
    print("Setting up...")
    scene = setup_scene()
    render_function = render_mp if multi_core else render
    render_msg = "Rendering at {}x{}".format(WIDTH, HEIGHT)
    if not debug_mode:
        render_msg += " with {}x{} AA".format(
            H_SAMPLES, V_SAMPLES
        )
        if multi_core:
            render_msg += " using multi-core"
    print(render_msg)
    # Raytrace one image
    # -------------------------------------------------------------------------
    if not animation_mode:
        log.start_of_raytracing()
        print("Raytracing...")
        if debug_mode:
            img_arr = render_no_aa(scene, scene.cameras[0], HEIGHT, WIDTH)
        else:
            img_arr = render_function(
                scene, scene.cameras[0], HEIGHT, WIDTH, V_SAMPLES, H_SAMPLES
            )
        img = Image.fromarray(img_arr)
        img.save(OUTPUT_IMG_FILENAME, quality=MAX_QUALITY)
        print("Rendered image saved in {}".format(OUTPUT_IMG_FILENAME))
        log.end_of_raytracing()
    # Create an animation
    # --------------------------------------------------------------------------
    else:
        duration = 4 if debug_mode else float(input("Enter duration="))
        screen_size = (WIDTH, HEIGHT)
        fps = 2 if debug_mode else int(input("Enter fps="))
        log.start_of_animation()
        animate(debug_mode, render_function, duration, screen_size, fps, scene)
        log.end_of_animation()
    # --------------------------------------------------------------------------
    end = time.time()
    time_spent = utils.humanize_time(end - start)
    print("Total time spent: {}".format(time_spent))


if __name__ == '__main__':
    main(sys.argv[1:])
