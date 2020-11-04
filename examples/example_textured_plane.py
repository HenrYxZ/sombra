"""
Example that generates an image of a plane with a texture and no lighting.
"""
import numpy as np
from PIL import Image
import os.path

# Local Modules
from camera import Camera
from constants import MAX_QUALITY
from material import Material, TYPE_TEXTURED
from object import Plane
from render import render
from scene import Scene
from texture import ImageTexture
import shaders
import utils

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 300
EXAMPLES_OUT_DIR = "../examples_out"
OUTPUT_IMG_FILENAME = "{}/3_textured_plane.jpg".format(EXAMPLES_OUT_DIR)


def set_camera():
    camera_pos = np.array([0.0, 0.2, 0.0])
    v_view = utils.normalize(np.array([-1.0, 0.0, 2.0]))
    v_up = np.array([0.0, 1.0, 0.0])
    # d, scale_x and scale_y are camera parameters that define the view window
    # in world space
    return Camera(camera_pos, v_view, v_up, d=0.26, scale_x=0.4, scale_y=0.3)


def set_scene():
    pos = np.array([0.0, 0.0, 0])
    mat = Material(material_type=TYPE_TEXTURED)
    texture = ImageTexture("../textures/checkers.png")
    mat.add_texture(texture)
    # Normal of the plane
    n = np.array([0.0, 1.0, 0.0])
    # n0 vector of the plane (vector lying in the plane)
    n0 = np.array([1.0, 0.0, 0.0])
    # Scale for the texture in x and y
    sx = 4
    sy = 4
    plane = Plane(pos, mat, shaders.TYPE_FLAT, n, n0, sx, sy)
    cameras = [set_camera()]
    return Scene(cameras, [], [plane])


def main():
    scene = set_scene()
    main_camera = scene.get_main_camera()
    screen = render(scene, main_camera, SCREEN_HEIGHT, SCREEN_WIDTH)
    img_output = Image.fromarray(screen)
    if not os.path.exists(EXAMPLES_OUT_DIR):
        os.mkdir(EXAMPLES_OUT_DIR)
    img_output.save(OUTPUT_IMG_FILENAME, quality=MAX_QUALITY)
    print(f"Output image created in : {OUTPUT_IMG_FILENAME}")


if __name__ == '__main__':
    main()
