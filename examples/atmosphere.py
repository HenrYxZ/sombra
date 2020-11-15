"""
Example that generates an image of the a sky using atmosphere
"""
import numpy as np
from PIL import Image

# Local Modules
from camera import Camera
from constants import MAX_QUALITY
from scene import Scene
from sky import SkyDome
from render import render, render_mp
import utils

SCREEN_WIDTH = 300
SCREEN_HEIGHT = 200
OUTPUT_DIR = "examples_out"
OUTPUT_IMG_FILENAME = f"{OUTPUT_DIR}/6_atmosphere.jpg"


def set_camera():
    camera_pos = np.array([0.0, 1.74, 0.0])
    v_view = np.array([0.0, 0.0, 1.0])
    v_up = np.array([0.0, 1.0, 0.0])
    return Camera(camera_pos, v_view, v_up, d=2.5, scale_x=3, scale_y=2)


def set_scene():
    sky_dome = SkyDome()
    cameras = [set_camera()]
    return Scene(cameras, [], [], None, sky_dome)


def main():
    print("Running atmosphere example")
    timer = utils.Timer()
    timer.start()
    scene = set_scene()
    main_camera = scene.get_main_camera()
    screen = render_mp(scene, main_camera, SCREEN_HEIGHT, SCREEN_WIDTH)
    img_output = Image.fromarray(screen)
    img_output.save(OUTPUT_IMG_FILENAME, quality=MAX_QUALITY)
    timer.stop()
    print(f"Image saved in {OUTPUT_IMG_FILENAME}")
    print(f"Total time spent {timer}")


if __name__ == '__main__':
    main()
