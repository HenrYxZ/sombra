import numpy as np
from progress.bar import Bar

# Local Modules
from constants import DEFAULT_N2
from light import SpotLight
from ray import Ray, reflect_ray
from texture import IlluminationTexture
import utils

PERCENTAGE_STEP = 1
KR_EPSILON = 0.2


def transport_light(ray, scene, light_intensity, depth=0):
    # Only use one bounce for now
    if depth == 2:
        return
    # Get closest intersection point
    t_min = np.inf
    # The closest object hit by the ray
    obj_h = None
    for obj in scene.objects:
        t = ray.intersect(obj)
        if 0 < t < t_min:
            t_min = t
            obj_h = obj
    if obj_h:
        ph = ray.at(t_min)
        # store the illumination
        n = obj_h.normal_at(ph)
        # the light unit vector is the opposite of the incoming ray
        l = ray.nr * -1
        illumination = light_intensity * np.dot(n, l)
        # Only add caustics for diffuse objects (kr=0)
        if (
            obj_h.material.illumination_map and depth > 0
            and obj_h.material.kr <= KR_EPSILON
        ):
            u, v = obj_h.uvmap(ph)
            illumination_map = obj_h.material.illumination_map
            illumination_map.add_color(u, v, illumination)
        # If this is a specular object, shoot again
        if obj_h.material.kr > 0:
            reflected_ray = reflect_ray(n, ray.nr, ph, obj_h.material.roughness)
            new_intensity = obj_h.material.kr * light_intensity
            transport_light(reflected_ray, scene, new_intensity, depth + 1)


def backward_raytracing(scene, light, width, height, n0, n1, d=2):
    """
    Shoot paths from the lights and store the new information in each object
    color texture
    """
    print("Illuminating with light raytracing...")
    sx = 2
    sy = 2
    iterations = height * width
    step_size = np.ceil((iterations * PERCENTAGE_STEP) / 100).astype('int')
    counter = 0
    # n1 = DEFAULT_N2
    # n0 = np.cross(light.nl, n1)
    p00 = light.position + d * light.nl - (sx / 2) * n0 - (sy / 2) * n1
    bar = Bar('Illuminating', max=100 / PERCENTAGE_STEP)
    # This is needed to use it in Git Bash
    bar.check_tty = False
    for j in range(height):
        for i in range(width):
            x = i
            y = height - 1 - j
            # Get x projected in view coord
            xp = (x / float(width)) * sx
            # Get y projected in view coord
            yp = (y / float(height)) * sy
            pp = p00 + xp * n0 + yp * n1
            npe = utils.normalize(pp - light.position)
            ray = Ray(light.position, npe)
            transport_light(ray, scene, light.color)
            counter += 1
            if counter % step_size == 0:
                bar.next()
    bar.finish()
