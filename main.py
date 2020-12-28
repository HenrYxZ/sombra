import getopt
import numpy as np
import os
from PIL import Image
import sys
import time
# Local Modules
from animation import Animation
from camera import Camera, LensParams
from constants import MAX_QUALITY
from env_map import EnvironmentMap
from light import AreaLight, DirectionalLight, PointLight, SpotLight
import log
from material import Material
import material
from normal_map import NormalMap
from object import Cube, Plane, Sphere, Tetrahedron, Triangle
from render import render_aa, render_dof, render, render_mp, render_aa_mp
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
V_SAMPLES = 3
H_SAMPLES = 3
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
    v_view = np.array([0, 0, 1], dtype=float)
    v_up = np.array([0, 1, 0], dtype=float)
    d = 26
    scale_x = 35
    scale_y = 24
    lens_params = LensParams()
    main_camera = Camera(
        main_camera_pos, v_view, v_up, d, scale_x, scale_y,  lens_params
    )
    return [main_camera]


def setup_lights():
    # Directional Light
    # directional_light = DirectionalLight(np.array([-1, -1, 1]))
    # Point Light
    # light_pos = np.array([0, 50, 0], dtype=float)
    # point_light = PointLight(light_pos)
    # Spot Light
    # nl = utils.normalize(np.array([0, -0.5, 1]))
    # theta = utils.degree2radians(30)
    # spot_light = SpotLight(light_pos, theta, nl)
    # Area Light
    area_light_pos = np.array([0, 100, 0.0])
    area_light_n0 = np.array([1.0, 0.0, 0.0])
    area_light_n1 = utils.normalize(np.array([0.0, 1.0, 0.0]))
    sx = 18
    sy = 18
    area_light = AreaLight(area_light_pos, sx, sy, area_light_n0, area_light_n1)
    return [area_light]


def setup_objects():
    # Plane Object
    plane_pos = np.array([0, -25, 0], dtype=float)
    plane_n0 = np.array([1, 0, 0], dtype=float)
    plane_mtl = Material(
        material.COLOR_GRAY, material.TYPE_TEXTURED, kr=0.4, roughness=0.06
        # material.COLOR_GRAY, material.TYPE_DIFFUSE
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
    sphere_shader = shaders.TYPE_DIFFUSE_COLORS
    sphere_r = 25.0
    sphere = Sphere(sphere_pos, sphere_mtl, sphere_shader, sphere_r)
    # # Mickey Sphere
    # sphere_pos = np.array([-30, -5, 75], dtype=float)
    # sphere_mtl = Material(
    #     material.COLOR_BLUE,
    #     material.TYPE_TEXTURED,
    #     specular=DEFAULT_KS
    # )
    # box = Box(sphere_pos, 40, 40, 40)
    # mickey_img_texture = ImageTexture(MICKEY_TEXTURE_FILENAME)
    # sphere_mtl.add_texture(SolidImageTexture(mickey_img_texture, box))
    # sphere_shader = shaders.TYPE_DIFFUSE_COLORS
    # sphere_r = 20.0
    # mickey = Sphere(sphere_pos, sphere_mtl, sphere_shader, sphere_r)
    # # Gray Sphere
    # sphere_pos = np.array([90, 15, 160], dtype=float)
    # sphere_mtl = Material(
    #     material.COLOR_GRAY,
    #     material.TYPE_DIFFUSE,
    #     specular=DEFAULT_KS,
    #     border=0.0,
    #     kr=0.7, roughness=0.15
    # )
    # sphere_shader = shaders.TYPE_DIFFUSE_COLORS
    # sphere_r = 40.0
    # gray_sphere = Sphere(sphere_pos, sphere_mtl, sphere_shader, sphere_r)
    # return [sphere, plane, mickey, gray_sphere]
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
    render_function = render if debug_mode else render_function
    animation = Animation(duration, screen_size, fps, scene, render_function)
    sphere = scene.objects[0]
    main_camera = scene.cameras[0]
    animation.create(sphere, main_camera)


def main(argv):
    debug_mode = False
    animation_mode = False
    multi_core = False
    # Depth of Field
    dof_mode = False
    try:
        opts, args = getopt.getopt(
            argv, "hdamf", ["help", "debug", "animation", "multi", "dof"]
        )
    except getopt.GetoptError:
        print(
            'usage: main.py [-d,-h,-a,-m,-f|--debug,--help,--animation, '
            '--multi, --dop]'
        )
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print(
                'usage: main.py [-d,-h,-a,-m,-f|--debug,--help,--animation, '
                '--multi, --dop]'
            )
            sys.exit()
        elif opt in ('-d', '--debug'):
            debug_mode = True
        elif opt in ('-a', '--animation'):
            animation_mode = True
        elif opt in ('-m', '--multi'):
            multi_core = True
        elif opt in ('-f', '--dof'):
            dof_mode = True
    start = time.time()
    print("Setting up...")
    scene = setup_scene()
    if multi_core:
        if debug_mode:
            render_function = render_mp
        else:
            render_function = render_aa_mp
    elif dof_mode:
        render_function = render_dof
    elif debug_mode:
        render_function = render
    else:
        render_function = render_aa
    render_msg = "Rendering at {}x{}".format(WIDTH, HEIGHT)
    if not debug_mode:
        render_msg += " with {}x{} AA".format(
            H_SAMPLES, V_SAMPLES
        )
        if dof_mode:
            render_msg += " using depth of field"
    if multi_core:
        render_msg += f" using {os.cpu_count()} cores"
    print(render_msg)
    # Raytrace one image
    # -------------------------------------------------------------------------
    if not animation_mode:
        log.start_of_raytracing()
        print("Raytracing...")
        if debug_mode:
            img_arr = render_function(scene, scene.cameras[0], HEIGHT, WIDTH)
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
