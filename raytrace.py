import numpy as np
# Local Modules
from constants import MAX_COLOR_VALUE, RGB_CHANNELS
import material
import shaders
from texture import ImageTexture
import utils

DARK_VALUE = np.array([15, 15, 15], dtype=float) / MAX_COLOR_VALUE
LIGHT_VALUE = np.array([240, 240, 240], dtype=float) / MAX_COLOR_VALUE


def get_dark_and_light(ph, obj):
    if obj.material.material_type == material.TYPE_DIFFUSE:
        dark = DARK_VALUE * obj.material.diffuse
        light = LIGHT_VALUE * obj.material.diffuse
    else:
        if isinstance(obj.material.texture, ImageTexture):
            u, v = obj.uvmap(ph)
            texture_color = obj.material.texture.get_color(u, v)
        else:
            # Case for solid image texture
            texture_color = obj.material.texture.get_color(ph)
        dark = DARK_VALUE * texture_color
        light = LIGHT_VALUE * texture_color
    return dark, light


def use_shader_type(
        shader_type, nh, l, dark, light, eye, ks, thickness, diffuse
):
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
        np.array: The color for this ray in numpy uint8 of 3 channels
    """
    if obj.shader_type == shaders.TYPE_DIFFUSE_NO_LIGHT:
        return obj.material.diffuse
    final_color = np.zeros(RGB_CHANNELS)
    for light in lights:
        l = light.get_l(ph)
        nh = obj.normal_at(ph)
        if nh is None:
            return np.zeros(3)
        dark, light = get_dark_and_light(ph, obj)
        ks = obj.material.specular
        thickness = obj.material.border
        diffuse = obj.material.diffuse
        # Choose the corresponding shader
        color = use_shader_type(
            obj.shader_type, nh, l, dark, light, eye, ks, thickness, diffuse
        )
        final_color += color
    # Ensure the colors are between 0 and 255
    final_color /= len(lights)
    final_color = np.clip(final_color, 0, MAX_COLOR_VALUE)
    return final_color.astype(np.uint8)


def compute_shadow(ph, objects, lights):
    """
    Get the shadow component for this hit point.

    Args:
        ph(numpy.array): 3D point of hit between ray and object
        objects([Object]): The objects to check for shadow computation
        lights([Light]): List of the lights in the scene

    Returns:
        np.array: The shadow for this ray in numpy uint8 of 3 channels
    """
    final_shadow = np.zeros(RGB_CHANNELS)
    for light in lights:
        l = light.get_l(ph)
        dist_l = light.get_dist(ph)
        shadow = shaders.hard_shadow(ph, objects, l, dist_l)
        final_shadow += shadow
    final_shadow /= len(lights)
    final_shadow = np.clip(final_shadow, 0, MAX_COLOR_VALUE)
    return final_shadow.astype(np.uint8)


def raytrace(ray, camera_pos, scene):
    """
    Trace the ray to the closest intersection point with an object and get the
    color at that point.

    Args:
        ray(Ray): The ray to be traced
        camera_pos(numpy.array): 3D position of the camera
        scene(Scene): This object contains things like objects, lights, etc

    Returns:
        np.array: The color for this ray in numpy uint8 of 3 channels
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
        eye = utils.normalize(camera_pos - ph)
        color = compute_color(ph, eye, obj_h, lights)
        # Objects to check for occlusion
        objects_to_check = [obj for obj in objects]
        objects_to_check.remove(obj_h)
        shadow = compute_shadow(ph, objects_to_check, lights)
        final_color = (
            color.astype(float) * (shadow.astype(float) / MAX_COLOR_VALUE)
        ).round()
        return final_color.astype(np.uint8)
    # No hit
    elif env_map:
        # Use unit director vector of ray for the Env Map
        color = env_map.get_color(ray.nr)
        return color.astype(np.uint8)
    else:
        return np.zeros(3, dtype=np.uint8)
