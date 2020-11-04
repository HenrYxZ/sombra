"""
Example that generates an image of a sphere with a flat color (no lighting).
"""
import numpy as np
from PIL import Image
import os.path

# Local Modules
from camera import Camera
from constants import RGB_CHANNELS, MAX_QUALITY
from light import DirectionalLight
from material import Material, COLOR_BLUE
from object import Sphere
from render import render
from scene import Scene
import shaders
import utils

SCREEN_WIDTH = 300
SCREEN_HEIGHT = 200
EXAMPLES_OUT_DIR = "../examples_out"
OUTPUT_IMG_FILENAME = f"{EXAMPLES_OUT_DIR}/4_six_spheres.jpg"


def set_camera():
    camera_pos = np.array([0.0, 0.0, 0.0])
    v_view = np.array([0.0, 0.0, 1.0])
    v_up = np.array([0.0, 1.0, 0.0])
    return Camera(camera_pos, v_view, v_up, d=0.26, scale_x=0.6, scale_y=0.4)


def set_scene():
    z = 1
    y = [-0.3, 0.3]
    x = [-0.6, 0, 0.6]
    L = np.array([30, -100, 25])
    mat = Material(COLOR_BLUE)
    radius = 0.15
    positions = []
    for j in range(len(y)):
        for i in range(len(x)):
            positions.append(np.array([x[i], y[j], z]))
    spheres = [
        Sphere(p, mat, shaders.TYPE_DIFF_SPECULAR, radius) for p in positions
    ]
    cameras = [set_camera()]
    light = DirectionalLight(L)
    return Scene(cameras, [light], spheres)


def main():
    scene = set_scene()
    main_camera = scene.get_main_camera()
    # ------------------------------------------------------------------------
    # Rendering
    timer = utils.Timer()
    timer.start()
    screen = render(scene, main_camera, SCREEN_HEIGHT, SCREEN_WIDTH)
    timer.stop()
    # ------------------------------------------------------------------------
    print(f"Total time spent rendering: {timer}")
    img_output = Image.fromarray(screen)
    if not os.path.exists(EXAMPLES_OUT_DIR):
        os.mkdir(EXAMPLES_OUT_DIR)
    img_output.save(OUTPUT_IMG_FILENAME, quality=MAX_QUALITY)
    print(f"Output image created in: {OUTPUT_IMG_FILENAME}")


if __name__ == '__main__':
    main()
