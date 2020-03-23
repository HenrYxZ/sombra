import numpy as np
# Local Modules
from constants import MAX_COLOR_VALUE, RGB_CHANNELS
import shaders
import utils
from light import DIRECTIONAL_LIGHT, POINT_LIGHT, SPOT_LIGHT

DARK_COLOR = np.array([15, 15, 15], dtype=float) / MAX_COLOR_VALUE
LIGHT_COLOR = np.array([240, 240, 240], dtype=float) / MAX_COLOR_VALUE


def compute_color(ph, eye, obj, lights):
    """
    Compute the color for the given object at the given point.

    Args:
        ph(numpy.array): 3D point of hit between ray and object
        eye(numpy.array): Unit vector in the direction of the viewer
        obj(Object): The object that was hit
        lights([Light]): List of the lights in the scene

    Returns:
        np.array: The color for this ray in numpy uint8 of 3 channels
    """
    final_color = np.zeros(RGB_CHANNELS)
    for light in lights:
        if light.type == POINT_LIGHT:
            l = utils.normalize(light.position - ph)
        elif light.type == DIRECTIONAL_LIGHT:
            l = utils.normalize(light.position)
        elif light.type == SPOT_LIGHT:
            l = utils.normalize(light.position - ph)
            # This light won't illuminate if the point is outside the cone
            if np.dot(l, light.nl) < light.cos_theta:
                continue
        else:
            # Default unit vector looking to light up in the y direction
            l = np.array([0, 1, 0], dtype=float)
        nh = obj.normal_at(ph)
        if nh is None:
            return np.zeros(3)
        dark = DARK_COLOR * obj.material.diffuse
        light = LIGHT_COLOR * obj.material.diffuse
        # Choose the corresponding one
        if obj.shader_type == shaders.TYPE_DIFFUSE_LIGHT:
            color = shaders.diffuse_light(nh, l)
        elif obj.shader_type == shaders.TYPE_DIFFUSE_COLORS:
            color = shaders.diffuse_colors(nh, l, dark, light)
        elif obj.shader_type == shaders.TYPE_DIFF_SPECULAR:
            color = shaders.diffuse_with_specular(nh, l, eye, dark, light)
        elif obj.shader_type == shaders.TYPE_DIFF_SPEC_BORDER:
            color = shaders.diffuse_specular_border(nh, l, eye, dark, light)
        else:
            color = np.zeros(RGB_CHANNELS)
        final_color += color
    # Ensure the colors are between 0 and 255
    final_color = np.clip(final_color, 0, MAX_COLOR_VALUE)
    return final_color.astype(np.uint8)


def raytrace(ray, camera_pos, objects, lights):
    """
    Trace the ray to the closest intersection point with an object and get the
    color at that point.

    Args:
        ray(Ray): The ray to be traced
        camera_pos(numpy.array): 3D position of the camera
        objects([Object]): Objects that are going to be checked for hit
        lights([Light]): Lights that will lid the object at hit point

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
        eye = utils.normalize(camera_pos - ph)
        color = compute_color(ph, eye, obj_h, lights)
        return color
    # No hit
    else:
        return np.array([0, 0, 0], dtype=np.uint8)
