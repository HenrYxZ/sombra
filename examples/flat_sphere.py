"""
Example that generates an image of a sphere with a flat color (no lighting).
"""
import numpy as np
from PIL import Image

# Local Modules
from camera import Camera
from constants import RGB_CHANNELS, MAX_QUALITY
from material import Material, COLOR_BLUE
from object import Sphere
from scene import Scene
import shaders

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 300
OUTPUT_IMG_FILENAME = "1_flat_sphere.jpg"


def set_camera():
    camera_pos = np.array([0.0, 0.25, 0.0])
    v_view = np.array([0.0, 0.0, 1.0])
    v_up = np.array([0.0, 1.0, 0.0])
    return Camera(camera_pos, v_view, v_up, d=0.26, scale_x=0.4, scale_y=0.3)


def set_scene():
    pos = np.array([0.0, 0.25, 0.6])
    mat = Material(COLOR_BLUE)
    radius = 0.25
    sphere = Sphere(pos, mat, shaders.TYPE_FLAT, radius)
    cameras = [set_camera()]
    return Scene(cameras, [], [sphere])


def main():
    scene = set_scene()
    main_camera = scene.get_main_camera()
    screen = np.zeros([SCREEN_HEIGHT, SCREEN_WIDTH, RGB_CHANNELS])
    img_output = Image.fromarray(screen)
    img_output.save(OUTPUT_IMG_FILENAME, quality=MAX_QUALITY)


if __name__ == '__main__':
    main()
