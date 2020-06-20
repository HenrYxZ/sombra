import numpy as np
import warnings
# Local Modules
from constants import MAX_COLOR_VALUE, RGB_CHANNELS
import material
from ray import Ray
import shaders
from texture import ImageTexture
import utils

DARK_VALUE = np.array([15, 15, 15], dtype=float) / MAX_COLOR_VALUE
LIGHT_VALUE = np.array([240, 240, 240], dtype=float) / MAX_COLOR_VALUE
# Constant of specular reflection
KR = 0.3
MIN_KR = 0.05
# Allow two reflection/refraction recursions
DEFAULT_RAYTRACER_DEPTH = 2


def get_dark_and_light(ph, obj):
    if obj.material.material_type == material.TYPE_DIFFUSE:
        color = obj.material.diffuse
    else:
        if isinstance(obj.material.texture, ImageTexture):
            u, v = obj.uvmap(ph)
            color = obj.material.texture.get_color(u, v)
        else:
            # Case for solid image texture
            color = obj.material.texture.get_color(ph)
    dark = DARK_VALUE * color
    light = LIGHT_VALUE * color
    return dark, light


def use_shader_type(shader_type, nh, l, eye, mtl, dark, light):
    ks = mtl.specular
    thickness = mtl.border
    if shader_type == shaders.TYPE_DIFFUSE_LIGHT:
        color = shaders.diffuse_light(nh, l)
    elif shader_type == shaders.TYPE_DIFFUSE_COLORS:
        color = shaders.diffuse_colors(nh, l, dark, light)
    elif shader_type == shaders.TYPE_DIFF_SPECULAR:
        color = shaders.diffuse_with_specular(
            nh, l, eye, dark, light, ks
        )
    elif shader_type == shaders.TYPE_DIFF_SPEC_BORDER:
        color = shaders.diffuse_specular_border(
            nh, l, eye, dark, light, ks, thickness
        )
    else:
        color = np.zeros(RGB_CHANNELS)
    return color


def compute_color(ph, eye, obj, lights):
    """
    Compute the color for the given object at the given point.

    Args:
        ph(numpy.array): 3D point of hit between ray and object
        eye(numpy.array): Unit vector in the direction of the viewer
        obj(Object): The object that was hit
        lights([Light]): List of the lights in the scene

    Returns:
        np.array: The color for this ray in numpy array of 3 channels
    """
    if obj.shader_type == shaders.TYPE_DIFFUSE_NO_LIGHT:
        return obj.material.diffuse
    # Control colors for barycentric shading
    dark_color, light_color = get_dark_and_light(ph, obj)
    nh = obj.normal_at(ph)
    if nh is None:
        warnings.warn("Normal is 0 for obj: {} at ph: {}".format(obj, ph))
        return np.zeros(3)
    final_color = np.zeros(RGB_CHANNELS)
    for light in lights:
        l = light.get_l(ph)
        # Choose the corresponding shader
        color = use_shader_type(
            obj.shader_type, nh, l, eye, obj.material, dark_color, light_color
        )
        final_color += color
    # Ensure the colors are between 0 and 255
    final_color /= len(lights)
    final_color = np.clip(final_color, 0, MAX_COLOR_VALUE)
    return final_color


def compute_shadow(ph, objects, lights):
    """
    Get the shadow component for this hit point.

    Args:
        ph(numpy.array): 3D point of hit between ray and object
        objects([Object]): The objects to check for shadow computation
        lights([Light]): List of the lights in the scene

    Returns:
        np.array: The shadow for this ray in numpy array of 3 channels
    """
    final_shadow = np.zeros(RGB_CHANNELS)
    for light in lights:
        l = light.get_l(ph)
        dist_l = light.get_dist(ph)
        shadow = shaders.hard_shadow(ph, objects, l, dist_l)
        final_shadow += shadow
    final_shadow /= len(lights)
    final_shadow = np.clip(final_shadow, 0, MAX_COLOR_VALUE)
    return final_shadow


def raytrace(ray, scene, depth=DEFAULT_RAYTRACER_DEPTH, kr=1):
    """
    Trace the ray to the closest intersection point with an object and get the
    color at that point.

    Args:
        ray(Ray): The ray to be traced
        scene(Scene): This object contains things like objects, lights, etc
        depth(int): How many sub iterations of raytrace will accept
        kr(float): How much this raytrace will reflect (used for recursion)

    Returns:
        np.array: The color for this ray in numpy array of 3 channels
    """
    # Get closest intersection point
    tmin = np.inf
    # The closest object hit by the ray
    obj_h = None
    objects = scene.objects
    lights = scene.lights
    env_map = scene.env_map
    for obj in objects:
        t = ray.intersect(obj)
        if 0 < t < tmin:
            tmin = t
            obj_h = obj
    # There is a hit with an object
    if obj_h:
        ph = ray.at(tmin)
        eye = utils.normalize(ray.pr - ph)
        color = compute_color(ph, eye, obj_h, lights)
        # Objects to check for occlusion
        objects_to_check = [obj for obj in objects]
        objects_to_check.remove(obj_h)
        shadow = compute_shadow(ph, objects_to_check, lights)
        final_color = (
            color.astype(float) * (shadow.astype(float) / MAX_COLOR_VALUE)
        ).round()
        # Reflections
        if obj_h.material.kr > 0 and depth > 0 and kr > MIN_KR:
            n = obj_h.normal_at(ph)
            C = np.dot(n, eye)
            r = -1 * eye + 2 * C * n
            # Adding roughness
            if obj_h.material.roughness > 0:
                # Random vector with 3 values between [-1, 1]
                random_vector = 2 * np.random.random_sample(3) - 1
                r = utils.normalize(
                    r + obj_h.material.roughness**2 * random_vector
                )
            reflected_ray = Ray(ph, utils.normalize(r))
            new_kr = kr * obj_h.material.kr
            reflection_color = raytrace(
                reflected_ray, scene, depth - 1, new_kr
            )
            final_color = final_color * (1 - new_kr) + reflection_color * new_kr
        return final_color
    # No hit
    elif env_map:
        # Use unit director vector of ray for the Env Map
        color = env_map.get_color(ray.nr)
        return color
    else:
        return np.zeros(3)
