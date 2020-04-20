import numpy as np

TYPE_DIFFUSE = "diffuse"
TYPE_TEXTURED = "textured"
# Color values are not in uint8 so just make sure to clip everything to uint8
# when rendering the final image
COLOR_BLUE = np.array([10, 10, 230], dtype=float)
COLOR_GRAY = np.array([135, 135, 135], dtype=float)


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

    """
    def __init__(
        self,
        diffuse=COLOR_GRAY,
        material_type=TYPE_DIFFUSE,
        specular=1.0,
        border=1.0,
        kr=0.0
    ):
        self.diffuse = diffuse
        self.material_type = material_type
        self.specular = specular
        self.border = border
        self.kr = kr
        self.texture = None

    def add_texture(self, texture):
        self.texture = texture
