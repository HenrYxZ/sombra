"""
Example that generates an image of a path-traced scene.
"""
import numpy as np
from PIL import Image
import os.path

# Local Modules
from camera import Camera
from constants import MAX_QUALITY, DEFAULT_N0, DEFAULT_N1, DEFAULT_N2
from light import PointLight
from light_raytracing import backward_raytracing
from material import Material
from object import Plane, Sphere
from pathtracer import pathtrace
from render import render_aa_t
from scene import Scene
import shaders
from texture import Box, IlluminationTexture, ImageTexture, SolidImageTexture
import utils
import material

SCREEN_WIDTH = 300
SCREEN_HEIGHT = 200
OUT_DIR = "../examples_out"
OUTPUT_IMG_FILENAME = f"{OUT_DIR}/5_pathtracing.jpg"
NORMAL_MAP_FILENAME = "textures/4483-normal.jpg"
debug = False
MICKEY_FILENAME = "textures/mickey.jpg"


def create_cube(objects):
    sx = 2
    sy = 2
    shader_type = shaders.TYPE_LIGHT_MAP
    positions = [
        np.array([-1, 1, 1]),
        np.array([1, 1, 1]),
        np.array([0, 1, 0]),
        np.array([0, 1, 2]),
        np.array([0, 0, 1]),
        np.array([0, 2, 1]),
    ]
    n0, n1, n2 = DEFAULT_N0, DEFAULT_N1, DEFAULT_N2
    ns = [n0, -n0, n2, -n2, n1, -n1]
    n0s = [n1, n1, n0, n0, n0, n0]
    colors = [
        material.COLOR_GREEN, material.COLOR_RED, material.COLOR_WHITE,
        material.COLOR_WHITE, material.COLOR_WHITE, material.COLOR_WHITE
    ]
    for i in range(6):
        mtl = Material(colors[i])
        illumination_map = IlluminationTexture()
        mtl.add_illumination_map(illumination_map)
        plane = Plane(positions[i], mtl, shader_type, ns[i], n0s[i], sx, sy)
        objects.append(plane)


def set_camera():
    camera_pos = np.array([0.0, 0.6, -0.5])
    v_view = np.array([0.0, 0.0, 1.0])
    v_up = np.array([0.0, 1.0, 0.0])
    camera = Camera(camera_pos, v_view, v_up, d=0.8, scale_x=1.2, scale_y=0.8)
    # camera.tilt(30)
    return camera


def set_light():
    # light_pos = np.array([-1, 1, 1])
    # light_theta = utils.degree2radians(30)
    # light_direction = utils.normalize(np.array([1, -1, 0]))
    # light = SpotLight(light_pos, light_theta, light_direction)
    # light_pos = np.array([0.0, 1.0, 0.01])
    light_pos = np.array([0, 1.7, 1])
    light_direction = -DEFAULT_N1
    light = PointLight(light_pos)
    light.nl = light_direction
    return light


def set_scene():
    cameras = [set_camera()]
    light = set_light()
    # Objects
    objects = []
    # Metallic sphere
    mtl = Material(kr=0.7, specular=0.8)
    shader_type = shaders.TYPE_DIFF_SPECULAR
    radius = 0.2
    pos = np.array([0.6, radius, 1])
    sphere = Sphere(pos, mtl, shader_type, radius)
    # normal_map = ImageTexture(NORMAL_MAP_FILENAME)
    # normal_map.prepare_for_sphere()
    # sphere.add_normal_map(normal_map)
    objects.append(sphere)
    # Mickey sphere
    radius = 0.4
    pos = np.array([-0.4, radius, 1.5])
    mtl = Material(
        material_type=material.TYPE_TEXTURED, specular=0.5, roughness=0.3
    )
    shader_type = shaders.TYPE_DIFF_SPECULAR
    texture = ImageTexture(MICKEY_FILENAME)
    box_size = 1.8 * radius
    box = Box(pos, box_size, box_size, box_size)
    mtl.add_texture(SolidImageTexture(texture, box))
    sphere = Sphere(pos, mtl, shader_type, radius)
    objects.append(sphere)
    create_cube(objects)

    return Scene(cameras, [light], objects)


def main():
    if not os.path.exists(OUT_DIR):
        os.mkdir(OUT_DIR)
    total_timer = utils.Timer()
    total_timer.start()
    scene = set_scene()
    main_camera = scene.get_main_camera()
    # ------------------------------------------------------------------------
    # Illuminate
    # timer = utils.Timer()
    # timer.start()
    # LIGHT_SCREEN_WIDTH = 1024
    # LIGHT_SCREEN_HEIGHT = 1024
    # # n0 = np.array([0, 0, -1])
    # # n1 = utils.normalize(np.array([1, 1, 0]))
    # n0 = DEFAULT_N0
    # n1 = DEFAULT_N2
    # backward_raytracing(
    #    scene, scene.lights[0], LIGHT_SCREEN_WIDTH, LIGHT_SCREEN_HEIGHT, n0, n1
    # )
    # timer.stop()
    # print(f"Total time spent illuminating: {timer}")
    # for i in range(len(scene.objects)):
    #     obj = scene.objects[i]
    #     if obj.material.illumination_map:
    #         map = obj.material.illumination_map.data
    #         img_output = Image.fromarray(map)
    #         filename = f"{OUT_DIR}/5_illumination_map_{i}.jpg"
    #         img_output.save(filename, quality=MAX_QUALITY)
    # Load saved illumination maps
    # for i in range(2, 8):
    #     filename = f"5_illumination_map_{i}.jpg"
    #     scene.objects[i].material.illumination_map.load(filename)
    # ------------------------------------------------------------------------
    # Rendering
    if debug:
        V_SAMPLES = 1
        H_SAMPLES = 1
    else:
        V_SAMPLES = 5
        H_SAMPLES = 5
    timer = utils.Timer()
    timer.start()
    print("Running pathtracer")
    screen = render_aa_t(
        scene, main_camera, pathtrace, SCREEN_HEIGHT, SCREEN_WIDTH, V_SAMPLES,
        H_SAMPLES
    )
    # screen = render_aa_t(
    #     scene, main_camera, raytrace, SCREEN_HEIGHT, SCREEN_WIDTH, V_SAMPLES,
    #     H_SAMPLES
    # )
    # screen = render_mp(scene, main_camera, SCREEN_HEIGHT, SCREEN_WIDTH)
    timer.stop()
    # ------------------------------------------------------------------------
    print(f"Total time spent rendering: {timer}")
    img_output = Image.fromarray(screen)
    img_output.save(OUTPUT_IMG_FILENAME, quality=MAX_QUALITY)
    print(f"Output image created in: {OUTPUT_IMG_FILENAME}")
    total_timer.stop()
    print(f"Total time in the program: {total_timer}")


if __name__ == '__main__':
    main()
