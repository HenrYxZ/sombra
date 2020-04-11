import numpy as np
from progress.bar import Bar
from random import random

# Local Modules
import utils
from ray import Ray
from raytrace import raytrace

PERCENTAGE_STEP = 1
RGB_CHANNELS = 3


def render_no_aa(scene, camera, HEIGHT=100, WIDTH=100):
    """
    Render the image for the given scene an camera using raytracing.

    Args:
        scene(Scene): The scene that contains objects, cameras and lights.
        camera(Camera): The camera that is rendering this image.

    Returns:
        numpy.array: The pixels with the raytraced colors.
    """
    output = np.zeros((HEIGHT, WIDTH, RGB_CHANNELS), dtype=np.uint8)
    if not scene or not scene.objects or not camera or camera.inside(
            scene.objects
    ):
        print("Cannot generate an image")
        return output
    # This is for showing progress %
    iterations = HEIGHT * WIDTH
    step_size = np.ceil((iterations * PERCENTAGE_STEP) / 100).astype('int')
    counter = 0
    bar = Bar('Raytracing', max=100 / PERCENTAGE_STEP)
    # This is needed to use it in Git Bash
    bar.check_tty = False
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
            output[j][i] = raytrace(ray, camera.position, scene)
            counter += 1
            if counter % step_size == 0:
                bar.next()
    bar.finish()
    return output


def render(scene, camera, HEIGHT=100, WIDTH=100, V_SAMPLES=4, H_SAMPLES=4):
    """
    Render the image for the given scene an camera using raytracing.

    Args:
        scene(Scene): The scene that contains objects, cameras and lights.
        camera(Camera): The camera that is rendering this image.

    Returns:
        numpy.array: The pixels with the raytraced colors.
    """
    output = np.zeros((HEIGHT, WIDTH, RGB_CHANNELS), dtype=np.uint8)
    if not scene or not scene.objects or not camera or camera.inside(
        scene.objects
    ):
        print("Cannot generate an image")
        return output
    # This is for showing progress %
    iterations = HEIGHT * WIDTH * V_SAMPLES * H_SAMPLES
    step_size = np.ceil((iterations * PERCENTAGE_STEP) / 100).astype('int')
    counter = 0
    bar = Bar('Raytracing', max=100/PERCENTAGE_STEP)
    # This is needed to use it in Git Bash
    bar.check_tty = False
    for j in range(HEIGHT):
        for i in range(WIDTH):
            color = np.array([0, 0, 0], dtype=float)
            for n in range(V_SAMPLES):
                for m in range(H_SAMPLES):
                    x = i + (float(m) / H_SAMPLES) + (random() / H_SAMPLES)
                    y = (
                        HEIGHT - 1 - j
                        + (float(n) / V_SAMPLES)
                        + (random() / V_SAMPLES)
                    )
                    # Get x projected in view coord
                    xp = (x / float(WIDTH)) * camera.scale_x
                    # Get y projected in view coord
                    yp = (y / float(HEIGHT)) * camera.scale_y
                    pp = camera.p00 + xp * camera.n0 + yp * camera.n1
                    npe = utils.normalize(pp - camera.position)
                    ray = Ray(pp, npe)
                    total_samples = H_SAMPLES * V_SAMPLES
                    color += (
                        raytrace(ray, camera.position, scene)
                        / float(total_samples)
                    )
                    counter += 1
                    if counter % step_size == 0:
                        bar.next()
            output[j][i] = np.round(color)
    bar.finish()
    return output
