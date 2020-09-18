import numpy as np
# Local Modules
from factories.constants import DEFAULT_POSITION, DEFAULT_RADIUS
from material import Material
from object import Sphere

DEFAULT_MATERIAL = Material()
MOCK_SHADER_TYPE = "mock_shader_type"


def create_sphere():
    return Sphere(
        DEFAULT_POSITION, DEFAULT_MATERIAL, MOCK_SHADER_TYPE, DEFAULT_RADIUS
    )


def create_sphere_behind():
    position = np.array([0, 0, -4])
    return Sphere(position, DEFAULT_MATERIAL, MOCK_SHADER_TYPE, DEFAULT_RADIUS)
