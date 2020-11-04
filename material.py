import numpy as np

TYPE_DIFFUSE = "diffuse"
TYPE_TEXTURED = "textured"
# Color values are not in uint8 so just make sure to clip everything to uint8
# when rendering the final image
COLOR_DARK_GRAY = np.array([64, 64, 64])
COLOR_GRAY = np.array([135, 135, 135])
COLOR_LIGHT_GRAY = np.array([211, 211, 211])
COLOR_GREEN = np.array([65, 230, 65])
COLOR_RED = np.array([230, 80, 80])
COLOR_BLUE = np.array([70, 70, 230])


class Material:
    """
    This class represents the material that an object will have.

    Attributes:
        diffuse(numpy.array): RGB color for the diffuse component
        material_type(str): the type of material like diffuse, textured, etc
        specular(float): parameter for how specular is this material (use
            values between 0 and 1)
        border(float): parameter for how thick the border is in this material
            (use values between 0 and 1)
        kr(float): parameter for how much the surface reflects (between 0 - 1)
        ior(float): parameter for index of refraction (between 0 - 1)
        roughness(float): parameter for how smooth is the surface of reflection
        illumination_map(IlluminationTexture): an illumination map object for
            backwards raytracing
    """
    def __init__(
        self,
        diffuse=COLOR_GRAY,
        material_type=TYPE_DIFFUSE,
        specular=1.0,
        border=1.0,
        kr=0.0,
        ior=1.0,
        roughness=0.0
    ):
        self.diffuse = diffuse
        self.material_type = material_type
        self.specular = specular
        self.border = border
        self.kr = kr
        self.ior = ior
        self.texture = None
        self.roughness = roughness
        self.illumination_map = None

    def add_texture(self, texture):
        self.texture = texture

    def add_illumination_map(self, texture):
        self.illumination_map = texture
