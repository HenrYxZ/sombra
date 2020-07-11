import multiprocessing as mp
import numpy as np
from progress.bar import Bar
from random import random

# Local Modules
import utils
from ray import Ray
from raytrace import raytrace

PERCENTAGE_STEP = 1
RGB_CHANNELS = 3


def raytrace_mp_wrapper(args):
    return raytrace(*args)


def avg(colors, samples):
    total_sum = np.zeros(3)
    for color in colors:
        total_sum += color
    return total_sum / samples


def create_rays(camera, HEIGHT=100, WIDTH=100, V_SAMPLES=4, H_SAMPLES=4):
    rays = []
    for j in range(HEIGHT):
        for i in range(WIDTH):
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
                    rays.append(ray)
    return rays


def render_no_aa(scene, camera, HEIGHT=100, WIDTH=100):
    """
    Render the image for the given scene and camera using raytracing.

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
            color = raytrace(ray, scene)
            output[j][i] = color.round().astype(np.uint8)
            counter += 1
            if counter % step_size == 0:
                bar.next()
    bar.finish()
    return output


def render(scene, camera, HEIGHT=100, WIDTH=100, V_SAMPLES=4, H_SAMPLES=4):
    """
    Render the image for the given scene and camera using raytracing.

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
                    color += raytrace(ray, scene) / float(total_samples)
                    counter += 1
                    if counter % step_size == 0:
                        bar.next()
            output[j][i] = color.round().astype(np.uint8)
    bar.finish()
    return output

def render_mp(scene, camera, HEIGHT=100, WIDTH=100, V_SAMPLES=4, H_SAMPLES=4):
    """
    Render the image for the given scene and camera using raytracing in multi-
    processors.

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
    print("Creating rays...")
    rays = create_rays(camera, HEIGHT, WIDTH, V_SAMPLES, H_SAMPLES)
    pool = mp.Pool(mp.cpu_count())
    print("Shooting rays...")
    ray_colors = pool.map(
        raytrace_mp_wrapper, [(ray, scene) for ray in rays]
    )
    print(ray_colors[:8])
    pool.close()
    print("Arranging pixels...")
    samples = H_SAMPLES * V_SAMPLES
    # using list comprehension
    pixel_colors = [
        avg(ray_colors[i:i+samples], samples)
        for i in range(0, len(ray_colors), samples)
    ]
    n = WIDTH * HEIGHT
    pixels_2d = [pixel_colors[i:i + WIDTH] for i in range(0, n, WIDTH)]
    output = np.asarray(pixels_2d).round().astype(np.uint8)
    return output
