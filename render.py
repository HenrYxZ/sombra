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

def raytrace_unordered_wrapper(args):
    ray, i, j, w, scene = args
    color = raytrace(ray, scene)
    weighted_color = color * w
    return (weighted_color, i, j)

def avg(colors, samples):
    total_sum = np.zeros(3)
    for color in colors:
        total_sum += color
    return total_sum / samples


def create_rays(camera, height, width):
    rays = []
    for j in range(height):
        for i in range(width):
            x = i
            y = height - 1 - j
            # Get x projected in view coord
            xp = (x / float(width)) * camera.scale_x
            # Get y projected in view coord
            yp = (y / float(height)) * camera.scale_y
            pp = camera.p00 + xp * camera.n0 + yp * camera.n1
            npe = utils.normalize(pp - camera.position)
            ray = Ray(pp, npe)
            rays.append(ray)
    return rays


def create_rays_aa(camera, HEIGHT=100, WIDTH=100, V_SAMPLES=4, H_SAMPLES=4):
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


def create_rays_aa_with_pos(
    camera, HEIGHT=100, WIDTH=100, V_SAMPLES=4, H_SAMPLES=4
):
    rays = []
    # weight for each ray
    w = 1 / (V_SAMPLES * H_SAMPLES)
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
                    rays.append([ray, i, j, w])
    return rays


def render(scene, camera, HEIGHT=100, WIDTH=100):
    """
    Render the image for the given scene and camera using raytracing.

    Args:
        scene(Scene): The scene that contains objects, cameras and lights.
        camera(Camera): The camera that is rendering this image.

    Returns:
        numpy.array: The pixels with the raytraced colors.
    """
    output = np.zeros((HEIGHT, WIDTH, RGB_CHANNELS), dtype=np.uint8)
    if not scene or scene.is_empty() or not camera or camera.inside(
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


def render_aa(scene, camera, HEIGHT=100, WIDTH=100, V_SAMPLES=4, H_SAMPLES=4):
    """
    Render the image for the given scene and camera using raytracing.

    Args:
        scene(Scene): The scene that contains objects, cameras and lights.
        camera(Camera): The camera that is rendering this image.

    Returns:
        numpy.array: The pixels with the raytraced colors.
    """
    output = np.zeros((HEIGHT, WIDTH, RGB_CHANNELS), dtype=np.uint8)
    if not scene or scene.is_empty() or not camera or camera.inside(
        scene.objects
    ):
        print("Cannot generate an image")
        return output
    total_samples = H_SAMPLES * V_SAMPLES
    # This is for showing progress %
    iterations = HEIGHT * WIDTH * total_samples
    step_size = np.ceil((iterations * PERCENTAGE_STEP) / 100).astype('int')
    counter = 0
    bar = Bar('Raytracing', max=100 / PERCENTAGE_STEP)
    # This is needed to use it in Git Bash
    bar.check_tty = False
    for j in range(HEIGHT):
        for i in range(WIDTH):
            color = np.array([0, 0, 0], dtype=float)
            for n in range(V_SAMPLES):
                for m in range(H_SAMPLES):
                    r0, r1 = np.random.random_sample(2)
                    # Floats x, y inside the image plane grid
                    x = i + ((float(m) + r0) / H_SAMPLES)
                    y = HEIGHT - 1 - j + ((float(n) + r1) / V_SAMPLES)
                    # Get x projected in view coord
                    xp = (x / float(WIDTH)) * camera.scale_x
                    # Get y projected in view coord
                    yp = (y / float(HEIGHT)) * camera.scale_y
                    pp = camera.p00 + xp * camera.n0 + yp * camera.n1
                    npe = utils.normalize(pp - camera.position)
                    ray = Ray(pp, npe)

                    color += raytrace(ray, scene) / float(total_samples)
                    counter += 1
                    if counter % step_size == 0:
                        bar.next()
            output[j][i] = color.round().astype(np.uint8)
    bar.finish()
    return output


def render_mp(scene, camera, height, width):
    """
    Render the image for the given scene and camera using raytracing in multi-
    processors.
    Args:
        scene(Scene): The scene that contains objects, cameras and lights.
        camera(Camera): The camera that is rendering this image.
    Returns:
        numpy.array: The pixels with the raytraced colors.
    """
    output = np.zeros((height, width, RGB_CHANNELS), dtype=np.uint8)
    if not scene or scene.is_empty() or not camera or camera.inside(
        scene.objects
    ):
        print("Cannot generate an image")
        return output
    print("Creating rays...")
    rays = create_rays(camera, height, width)
    pool = mp.Pool(mp.cpu_count())
    print("Shooting rays...")
    ray_colors = pool.map(
        raytrace_mp_wrapper, [(ray, scene) for ray in rays]
    )
    pool.close()
    print("Arranging pixels...")
    for j in range(height):
        for i in range(width):
            output[j][i] = ray_colors[i + j * width]
    return output


def render_aa_mp(
        scene, camera, HEIGHT=100, WIDTH=100, V_SAMPLES=4, H_SAMPLES=4
):
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
    if not scene or scene.is_empty() or not camera or camera.inside(
        scene.objects
    ):
        print("Cannot generate an image")
        return output
    print("Creating rays...")
    rays = create_rays_aa(camera, HEIGHT, WIDTH, V_SAMPLES, H_SAMPLES)
    pool = mp.Pool(mp.cpu_count())
    print("Shooting rays...")
    ray_colors = pool.map(
        raytrace_mp_wrapper, [(ray, scene) for ray in rays]
    )
    pool.close()
    print("Arranging pixels...")
    samples = H_SAMPLES * V_SAMPLES
    # using list comprehension
    pixel_colors = [
        avg(ray_colors[i:i + samples], samples)
        for i in range(0, len(ray_colors), samples)
    ]
    n = WIDTH * HEIGHT
    pixels_2d = [pixel_colors[i:i + WIDTH] for i in range(0, n, WIDTH)]
    output = np.asarray(pixels_2d).round().astype(np.uint8)
    return output


def render_aa_mp_unordered(
    scene, camera, HEIGHT=100, WIDTH=100, V_SAMPLES=4, H_SAMPLES=4
):
    """
    Render the image for the given scene and camera using raytracing in multi-
    processors unordered with random-jittering anti-aliasing.

    Args:
        scene(Scene): The scene that contains objects, cameras and lights.
        camera(Camera): The camera that is rendering this image.

    Returns:
        numpy.array: The pixels with the raytraced colors.
    """
    output = np.zeros([HEIGHT, WIDTH, RGB_CHANNELS], dtype=np.uint8)
    n = HEIGHT * WIDTH * V_SAMPLES * H_SAMPLES
    if not scene or scene.is_empty() or not camera or camera.inside(
        scene.objects
    ):
        print("Cannot generate an image")
        return output
    print("Creating rays...")
    rays_with_pos = create_rays_aa_with_pos(
        camera, HEIGHT, WIDTH, V_SAMPLES, H_SAMPLES
    )
    threads_count = mp.cpu_count()
    pool = mp.Pool(threads_count)
    print("Shooting rays...")
    ray_colors = pool.imap_unordered(
        raytrace_unordered_wrapper, [
            (ray, i, j, w, scene) for ray, i, j, w in rays_with_pos
        ], chunksize=n//threads_count
    )
    pool.close()
    # Put the colors in a float buffer first, then pass to uint8
    buffer = np.zeros([HEIGHT, WIDTH, RGB_CHANNELS])
    for color, i, j in ray_colors:
        buffer[j][i] += color
    print("Arranging pixels...")
    for j in range(HEIGHT):
        for i in range(WIDTH):
            output[j][i] = buffer[j][i].round()
    return output


def render_dof(scene, camera, HEIGHT=100, WIDTH=100, V_SAMPLES=6, H_SAMPLES=6):
    """
    Render the image for the given scene and camera using raytracing with
    depth of field.

    Args:
        scene(Scene): The scene that contains objects, cameras and lights.
        camera(Camera): The camera that is rendering this image.

    Returns:
        numpy.array: The pixels with the raytraced colors.
    """
    output = np.zeros((HEIGHT, WIDTH, RGB_CHANNELS), dtype=np.uint8)
    if not scene or scene.is_empty() or not camera or camera.inside(
            scene.objects
    ):
        print("Cannot generate an image")
        return output
    total_samples = H_SAMPLES * V_SAMPLES
    # This is for showing progress %
    iterations = HEIGHT * WIDTH * total_samples
    step_size = np.ceil((iterations * PERCENTAGE_STEP) / 100).astype('int')
    counter = 0
    bar = Bar('Raytracing', max=100 / PERCENTAGE_STEP)
    # This is needed to use it in Git Bash
    bar.check_tty = False
    for j in range(HEIGHT):
        for i in range(WIDTH):
            color = np.array([0, 0, 0], dtype=float)
            lens_sample_offsets = []
            n0 = camera.n0
            n1 = camera.n1
            for n in range(V_SAMPLES):
                for m in range(H_SAMPLES):
                    r0, r1 = np.random.random_sample(2)
                    ap_sx = camera.lens_params.ap_sx
                    ap_sy = camera.lens_params.ap_sy
                    x_offset = ((r0 - 0.5) * m) / H_SAMPLES * ap_sx
                    y_offset = ((r1 - 0.5) * n) / V_SAMPLES * ap_sy
                    lens_sample_offsets.append((x_offset, y_offset))
            random_start = np.random.random_integers(0, total_samples - 1)
            for n in range(V_SAMPLES):
                for m in range(H_SAMPLES):
                    r0, r1 = np.random.random_sample(2)
                    x = i + ((float(m) + r0) / H_SAMPLES)
                    y = HEIGHT - 1 - j + ((float(n) + r1) / V_SAMPLES)
                    # Get x projected in view coord
                    xp = (x / float(WIDTH)) * camera.scale_x
                    # Get y projected in view coord
                    yp = (y / float(HEIGHT)) * camera.scale_y
                    pp = camera.p00 + xp * camera.n0 + yp * camera.n1
                    npe = utils.normalize(pp - camera.position)
                    sample_idx = n + m * H_SAMPLES - random_start
                    x_offset, y_offset = lens_sample_offsets[sample_idx]
                    ps = pp + x_offset * n0 + y_offset * n1
                    fp = pp + npe * camera.lens_params.f
                    director = utils.normalize(fp - ps)
                    ray = Ray(ps, director)

                    color += raytrace(ray, scene) / float(total_samples)
                    counter += 1
                    if counter % step_size == 0:
                        bar.next()
            output[j][i] = color.round().astype(np.uint8)
    bar.finish()
    return output


def render_aa_t(
        scene, camera, func, HEIGHT=100, WIDTH=100, V_SAMPLES=4,
        H_SAMPLES=4
):
    """
    Render the image for the given scene and camera using a template function.

    Args:
        scene(Scene): The scene that contains objects, cameras and lights.
        camera(Camera): The camera that is rendering this image.

    Returns:
        numpy.array: The pixels with the raytraced colors.
    """
    output = np.zeros((HEIGHT, WIDTH, RGB_CHANNELS), dtype=np.uint8)
    if not scene or scene.is_empty() or not camera or camera.inside(
        scene.objects
    ):
        print("Cannot generate an image")
        return output
    total_samples = H_SAMPLES * V_SAMPLES
    # This is for showing progress %
    iterations = HEIGHT * WIDTH
    step_size = np.ceil((iterations * PERCENTAGE_STEP) / 100).astype('int')
    counter = 0
    bar = Bar('Rendering', max=100 / PERCENTAGE_STEP)
    # This is needed to use it in Git Bash
    bar.check_tty = False
    for j in range(HEIGHT):
        for i in range(WIDTH):
            color = np.array([0, 0, 0], dtype=float)
            for n in range(V_SAMPLES):
                for m in range(H_SAMPLES):
                    r0, r1 = np.random.random_sample(2)
                    # Floats x, y inside the image plane grid
                    x = i + ((float(m) + r0) / H_SAMPLES)
                    y = HEIGHT - 1 - j + ((float(n) + r1) / V_SAMPLES)
                    # Get x projected in view coord
                    xp = (x / float(WIDTH)) * camera.scale_x
                    # Get y projected in view coord
                    yp = (y / float(HEIGHT)) * camera.scale_y
                    pp = camera.p00 + xp * camera.n0 + yp * camera.n1
                    npe = utils.normalize(pp - camera.position)
                    ray = Ray(pp, npe)

                    color += func(ray, scene) / float(total_samples)
            counter += 1
            if counter % step_size == 0:
                bar.next()
            output[j][i] = color.round().astype(np.uint8)
    bar.finish()
    return output
