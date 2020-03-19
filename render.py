import numpy as np
from random import random

# Local Modules
import constants
import utils
from ray import Ray
from raytrace import raytrace

PERCENTAGE_STEP = 5
RGB_CHANNELS = 3


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
    iterations = HEIGHT * WIDTH * V_SAMPLES * H_SAMPLES
    step_size = np.ceil((iterations * PERCENTAGE_STEP) / 100).astype('int')
    counter = 0
    for j in range(HEIGHT):
        for i in range(WIDTH):
            color = np.array([0, 0, 0], dtype=np.uint8)
            for n in range(V_SAMPLES):
                for m in range(H_SAMPLES):
                    x = i + (float(m) / H_SAMPLES) + (random() / H_SAMPLES)
                    y = (
                        HEIGHT - 1 - j
                        + (float(n) / V_SAMPLES)
                        +(random() / V_SAMPLES)
                    )
                    # Get x projected in view coord
                    xp = (x / WIDTH) * camera.scale_x
                    # Get y projected in view coord
                    yp = (y / HEIGHT) * camera.scale_y
                    pp = camera.p00 + xp * camera.n0 + yp * camera.n1
                    npe = utils.normalize(pp - camera.position)
                    ray = Ray(pp, npe)
                    total_samples = H_SAMPLES * V_SAMPLES
                    color += (
                        raytrace(ray, scene.objects, scene.lights)
                        / total_samples
                    )
                    counter += 1
                    if counter % step_size == 0:
                        percent_done = int((counter / float(iterations)) * 100)
                        print("{}% done".format(percent_done))
            output[j][i] = color
    return output