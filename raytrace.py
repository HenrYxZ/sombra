import numpy as np
# Local Modules
import shaders
import utils
from constants import MAX_COLOR_VALUE
from light import POINT_LIGHT, DIRECTIONAL_LIGHT
from object import Plane, Sphere


def compute_color(ph, obj, lights):
    """
    Compute the color for the given object at the given point.

    Returns:
        np.array: The color for this ray in numpy uint8 of 3 channels
    """
    final_color = np.array([0, 0, 0], dtype=float)
    for light in lights:
        if light.type == POINT_LIGHT:
            l = utils.normalize(light.position - ph)
        elif light.type == DIRECTIONAL_LIGHT:
            l = utils.normalize(light.position)
        else:
            # Default unit vector looking to light up in the y direction
            l = np.array([0, 1, 0], dtype=float)
        nh = obj.normal_at(ph)
        if nh is None:
            return np.array([0, 0, 0], dtype=float)
        color = shaders.diffuse(nh, l, obj.material.diffuse)
        final_color += color
    # Ensure the colors are between 0 and 255
    final_color = np.clip(final_color, 0, MAX_COLOR_VALUE)
    return final_color.astype(np.uint8)


def raytrace(ray, objects, lights):
    """
    Use the given ray to calculate colors.

    Returns:
        np.array: The color for this ray in numpy uint8 of 3 channels
    """
    # Get closest intersection point
    tmin = np.inf
    # The closest object hit by the ray
    obj_h = None
    for obj in objects:
        t = ray.intersect(obj)
        if 0 < t < tmin:
            tmin = t
            obj_h = obj
    # There is a hit with an object
    if obj_h:
        ph = ray.at(tmin)
        color = compute_color(ph, obj_h, lights)
        return color
    # No hit
    else:
        return np.array([0, 0, 0], dtype=np.uint8)