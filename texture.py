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
            numpy.array: color for this point, interpolating the 4 closest
                pixels
        """
        # Use tiling
        u = u - np.floor(u)
        if u < 0:
            u = 1 - u
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
            return self.img[I][J]
        # t and s are interpolation parameters that go from 0 to 1
        t = x - I + 0.5
        s = y - J + 0.5
        color = (
            self.img[J - 1][I - 1] * (1 - t) * (1 - s)
            + self.img[J - 1][I] * t * (1 - s)
            + self.img[J][I - 1] * (1 - t) * s
            + self.img[J][I] * t * s
        )
        return color
