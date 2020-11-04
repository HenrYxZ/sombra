import numpy as np

# Local Modules
from constants import MAX_COLOR_VALUE
from light import SpotLight
from ray import Ray, reflect_ray
from raytrace import compute_color, compute_shadow
import utils


DEFAULT_MAX_DEPTH = 5
rng = np.random.default_rng()
MIN_REFLECTIVE = 0.4


def pathtrace(ray, scene, depth=DEFAULT_MAX_DEPTH, current_level=0, weight=1):
    """
    Generates a path for a given ray
    Args:
        ray:
        scene:
        depth:
        current_level:
        weight:
    Returns:
        ndarray: The color for the path
    """
    # 1. Shoot ray and compute color at hit point
    # Get closest intersection point
    t_min = np.inf
    # The closest object hit by the ray
    obj_h = None
    for obj in scene.objects:
        t = ray.intersect(obj)
        if 0 < t < t_min:
            t_min = t
            obj_h = obj
    # There is a hit with an object
    if obj_h:
        ph = ray.at(t_min)
        eye = -ray.nr
        color = compute_color(ph, eye, obj_h, scene.lights)
        # Objects to check for occlusion
        objects_to_check = [obj for obj in scene.objects]
        objects_to_check.remove(obj_h)
        shadow = compute_shadow(ph, objects_to_check, scene.lights)
        surface_color = (
            color.astype(float) * (shadow.astype(float) / MAX_COLOR_VALUE)
        ).round()
        # Update weight multiplying reflectivity
        kr = max(obj_h.material.kr, MIN_REFLECTIVE)
        weight *= kr
        # 2. Calculate probability of stopping using Russian Roulette
        random_number = rng.random()
        if random_number < 1 - weight:
            # Stop
            return surface_color
        # Continue
        diffuse = obj_h.material.kr == 0
        reflected_ray = reflect_ray(
            obj_h.normal_at(ph), eye, ph, obj_h.material.roughness, diffuse
        )
        final_color = (1 - kr) * surface_color + kr * pathtrace(
            reflected_ray, scene, depth, current_level + 1, weight
        )
        return final_color
    # No hit
    elif scene.env_map:
        # Use unit director vector of ray for the Env Map
        color = scene.env_map.get_color(ray.nr)
        return color
    else:
        return np.zeros(3)
