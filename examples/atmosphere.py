"""
Example that generates an image of the a sky using atmosphere
"""
import numpy as np
from PIL import Image
from progress.bar import Bar

# Local Modules
from camera import Camera
from constants import MAX_QUALITY, RGB_CHANNELS
from light import DirectionalLight
from material import Material
from object import Sphere
from ray import Ray
from raytrace import raytrace
from render import render, render_mp
from scene import Scene
import shaders
from sky import SkyDome
import utils

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
OUTPUT_DIR = "examples_out"
OUTPUT_IMG_FILENAME = f"{OUTPUT_DIR}/6_atmosphere.jpg"


def process_buffer(buffer):
    max_num = np.max(buffer)
    buffer = buffer / max_num
    output = (np.round(buffer) * MAX_QUALITY).astype(np.uint8)
    return output


def render_sky(scene, camera, HEIGHT=100, WIDTH=100):
    """
    Render the image for the given scene and camera using raytracing.

    Args:
        scene(Scene): The scene that contains objects, cameras and lights.
        camera(Camera): The camera that is rendering this image.

    Returns:
        numpy.array: The pixels with the raytraced colors.
    """
    # This is for showing progress %
    iterations = HEIGHT * WIDTH
    step_size = np.ceil(iterations / 100).astype('int')
    counter = 0
    bar = Bar('Raytracing', max=100)
    # This is needed to use it in Git Bash
    bar.check_tty = False
    buffer = np.zeros([HEIGHT, WIDTH, RGB_CHANNELS])
    for j in range(HEIGHT):
        for i in range(WIDTH):
            x = i
            y = HEIGHT - 1 - j
            # Get x projected in view coord
            xp = (x / float(WIDTH)) * camera.scale_x
            # Get y projected in view coord
            yp = (y / float(HEIGHT)) * camera.scale_y
            pp = camera.p00 + xp * camera.n0 + yp * camera.n1
            npe = utils.normalize(pp - camera.position)
            ray = Ray(pp, npe)
            color = scene.sky_dome.light_at_ray(ray)
            buffer[j][i] = color
            counter += 1
            if counter % step_size == 0:
                bar.next()
    bar.finish()
    output = process_buffer(buffer)
    return output


def set_camera():
    camera_pos = np.array([0.0, 1.74, 0.0])
    v_view = np.array([0.0, 0.0, 1.0])
    v_up = np.array([0.0, 1.0, 0.0])
    return Camera(camera_pos, v_view, v_up, d=2.5, scale_x=3, scale_y=2)


def set_scene():
    sky_dome = SkyDome()
    cameras = [set_camera()]
    r = sky_dome.radius
    position = np.array([0, -r, 0])
    sphere = Sphere(position, Material(), shaders.TYPE_DIFFUSE_COLORS, r)
    objects = [sphere]
    light = DirectionalLight(-sky_dome.sun_direction)
    lights = [light]
    return Scene(cameras, lights, objects, None, sky_dome)


def main():
    print("Running atmosphere example")
    timer = utils.Timer()
    timer.start()
    scene = set_scene()
    main_camera = scene.get_main_camera()
    screen = render_mp(
        scene, main_camera, SCREEN_HEIGHT, SCREEN_WIDTH
    )
    img_output = Image.fromarray(screen)
    img_output.save(OUTPUT_IMG_FILENAME, quality=MAX_QUALITY)
    timer.stop()
    print(f"Image saved in {OUTPUT_IMG_FILENAME}")
    print(f"Total time spent {timer}")


if __name__ == '__main__':
    main()
