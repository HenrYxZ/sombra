import numpy as np
from PIL import Image


class Texture:
    """
    Represent a texture for the material of an object.
    """
    def __init__(self):
        pass

    def get_color(self, *args):
        """
        Return the color for a point in texture coordinates
        """
        pass


class ImageTexture(Texture):
    """
    Represent a texture that uses an image.

    Attributes:
        img_filename(str): Path to the image file
        img(numpy.array): Image for this texture as a numpy array
    """
    def __init__(self, img_filename):
        Texture.__init__(self)
        self.img_filename = img_filename
        img_obj = Image.open(img_filename)
        self.img = np.asarray(img_obj)
        self.h, self.w, _ = self.img.shape

    def get_color(self, u, v):
        """
        Get the color for one point (u, v) inside the texture, it doesn't have
        to be between 0 and 1, this will use tiling.

        Args:
            u(float): horizontal coordinate of the point
            v(float): vertical coordinate of the point

        Returns:
            numpy.array: RGB color for this point, interpolating the 4 closest
                pixels
        """
        # Use tiling
        if u < 0 or u > 1:
            u = u - np.floor(u)
            if u < 0:
                u = 1 - u
        if v < 0 or v > 1:
            v = v - np.floor(v)
            if v < 0:
                v = 1 - v
        x = u * self.w
        y = v * self.h
        # Flip y value to go from bottom to top
        y = self.h - y
        # Interpolate values of pixel neighborhood of x and y
        I = int(np.round(x))
        J = int(np.round(y))
        # But not in the borders
        if I == 0 or J == 0 or I == self.w or J == self.h:
            if I == self.w:
                I -= 1
            if J == self.h:
                J -= 1
            return self.img[J][I]
        # t and s are interpolation parameters that go from 0 to 1
        t = x - I + 0.5
        s = y - J + 0.5
        # Ensure this only gives RGB and not A
        color = (
                self.img[J - 1][I - 1] * (1 - t) * (1 - s)
                + self.img[J - 1][I] * t * (1 - s)
                + self.img[J][I - 1] * (1 - t) * s
                + self.img[J][I] * t * s
        )[:3]
        return color


class Box:
    def __init__(self, p0, s0, s1, s2, n0, n1, n2):
        self.p0 = p0
        self.s0 = s0
        self.s1 = s1
        self.s2 = s2
        self.n0 = n0
        self.n1 = n1
        self.n2 = n2


class SolidImageTexture(Texture):
    """
    Represents a texture defined by a solid box.

    Attributes:
        img_texture(ImageTexture): The object that stores the image and can get
            the texture for a given (u, v)
        box(Box): The spatial representation of this solid texture
    """
    def __init__(self, img_texture, box):
        Texture.__init__(self)
        self.img_texture = img_texture
        self.box = box

    def get_color(self, p):
        """
        Get the color for a solid image texture that repeats the same image
        along the n2 axis.

        Args:
            p(numpy.array): 3D point in world coordinates

        Returns:
            numpy.array: RGB value calculated using the texture
        """
        u = np.dot(self.box.n0, p - self.box.p0) / self.box.s0
        v = np.dot(self.box.n1, p - self.box.p0) / self.box.s1
        color = self.img_texture.get_color(u, v)
        return color
