import numpy as np
from PIL import Image
from random import random
import time
# Local Modules
from camera import Camera
from light import Light, POINT_LIGHT
from object import Sphere, OBJ_TYPE_SPHERE
from ray import Ray
import shaders
from scene import Scene
import utils

# Width and Height of the image window in pixels
WIDTH = 200
HEIGHT = 200
# Vertical and Horizontal Samples for Random Jitter Anti Aliasing
V_SAMPLES = 4
H_SAMPLES = 4
PERCENTAGE_STEP = 5
MAX_QUALITY = 95
RGB_CHANNELS = 3
OUTPUT_IMG_FILENAME = "output.jpg"


def setup_scene():
    main_camera_pos = np.array([0, 0, -1])
    # quizas esto tenga que ser negativo
    vview = np.array([0, 0, 1])
    vup = np.array([0, 1, 0])
    main_camera = Camera(main_camera_pos, vview, vup)
    light_pos = np.array([0, 1.2, 0.5])
    light = Light(light_pos, POINT_LIGHT)
    sphere_position = np.array([0, 0.25, 1])
    sphere_radius = 0.25
    sphere = Sphere(sphere_position, sphere_radius)
    scene = Scene([main_camera], [light], [sphere])
    return scene


def inside(camera, objects):
    """
    Returns true if the camera position is inside any of the objects.
    """
    for obj in objects:
        if obj.type == OBJ_TYPE_SPHERE:
            dif = camera.position - obj.position
            if np.dot(dif, dif) < (obj.radius ** 2):
                return True
    return False


def compute_color(ph, obj, lights):
    """
    Compute the color for the given object at the given point.

    Returns:
        np.array: The color for this ray in numpy uint8 of 3 channels
    """
    if obj.type == OBJ_TYPE_SPHERE:
        nh = utils.normalize(ph - obj.position)
        material = np.array([10, 10, 230], dtype=np.uint8)
        final_color = np.array([0, 0, 0])
        for light in lights:
            if light.type == POINT_LIGHT:
                l = utils.normalize(light.position - ph)
                color = shaders.diffuse(nh, l, material)
            final_color += color
        final_color = np.clip(final_color, 0, 255).astype(np.uint8)
        return final_color
    else:
        return np.array([0, 0, 0], dtype=np.uint8)


def raytrace(ray, objects, lights):
    """
    Use the given ray to calculate colors.

    Returns:
        np.array: The color for this ray in numpy uint8 of 3 channels
    """
    color = np.array([0, 0, 0], dtype=np.uint8)
    # Get closest intersection point
    tmin = np.inf
    # The closest object hitted by the ray
    obj_h = None
    for obj in objects:
        t = ray.intersect(obj)
        print(t)
        if t > 0 and t < tmin:
            tmin = t
            obj_h = obj
    if obj_h:
        ph = ray.at(tmin)
        total_num_samples = H_SAMPLES * V_SAMPLES
        color += (
            compute_color(ph, obj_h, lights)
            / total_num_samples
        )
    return color


def render(scene, camera):
    """
    Render the image for the given scene an camera using raytracing.

    Args:
        scene(Scene): The scene that contains objects, cameras and lights.
        camera(Camera): The camera that is rendering this image.

    Returns:
        numpy.array: The pixels with the raytraced colors.
    """
    output = np.zeros((HEIGHT, WIDTH, RGB_CHANNELS), dtype=np.uint8)
    if not scene or not scene.objects or not camera or inside(
        camera, scene.objects
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
                    x = i + (m / H_SAMPLES) + (random() / H_SAMPLES)
                    y = j + (n / V_SAMPLES) + (random() / V_SAMPLES)
                    # Get x projected in view coords
                    xp = (x / WIDTH) * camera.scale_x
                    # Get y projected in view coords
                    yp = (y / HEIGHT) * camera.scale_y
                    pp = camera.p00 + xp * camera.n0 + yp * camera.n1
                    npe = pp - camera.position
                    ray = Ray(pp, npe)
                    color += raytrace(ray, scene.objects, scene.lights)
                    counter += 1
                    if counter % step_size == 0:
                        percent_done = int((counter / float(iterations)) * 100)
                        print("{}% done".format(percent_done))
            output[j][i] = color
    return output


def main():
    start = time.time()
    print("Setting up...")
    scene = setup_scene()
    print("Raytracing...")
    img_arr = render(scene, scene.cameras[0])
    img = Image.fromarray(img_arr)
    img.save(OUTPUT_IMG_FILENAME, quality=MAX_QUALITY)
    print("Rendered image saved in {}".format(OUTPUT_IMG_FILENAME))
    end = time.time()
    time_spent = utils.humanize_time(end - start)
    print("Total time spent: {}".format(time_spent))


if __name__ == '__main__':
    main()
