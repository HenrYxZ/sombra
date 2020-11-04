import numpy as np
from PIL import Image
# Local Modules
from constants import DEFAULT_N0, DEFAULT_N1, DEFAULT_N2, RGB_CHANNELS, \
    MAX_COLOR_VALUE


DEFAULT_MAP_WIDTH = 1024
DEFAULT_MAP_HEIGHT = 1024


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
        i = int(np.round(x))
        j = int(np.round(y))
        # But not in the borders
        if i == 0 or j == 0 or i == self.w or j == self.h:
            if i == self.w:
                i -= 1
            if j == self.h:
                j -= 1
            return self.img[j][i]
        # t and s are interpolation parameters that go from 0 to 1
        t = x - i + 0.5
        s = y - j + 0.5
        # Ensure this only gives RGB and not A
        color = (
            self.img[j - 1][i - 1] * (1 - t) * (1 - s)
            + self.img[j - 1][i] * t * (1 - s)
            + self.img[j][i - 1] * (1 - t) * s
            + self.img[j][i] * t * s
        )[:3]
        return color

    def prepare_for_sphere(self):
        im_arr = self.img
        new_arr = np.tile(im_arr, 2)
        self.img = new_arr
        self.h, self.w, _ = self.img.shape


class Box:
    def __init__(
        self, center, s0, s1, s2, n0=DEFAULT_N0, n1=DEFAULT_N1, n2=DEFAULT_N2
    ):
        self.center = center
        self.s0 = s0
        self.s1 = s1
        self.s2 = s2
        self.n0 = n0
        self.n1 = n1
        self.n2 = n2
        self.min_vertex = center - (s0 / 2) * n0 - (s1 / 2) * n1 - (s2 / 2) * n2


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

        u = np.dot(self.box.n0, p - self.box.min_vertex) / self.box.s0
        v = np.dot(self.box.n1, p - self.box.min_vertex) / self.box.s1
        color = self.img_texture.get_color(u, v)
        return color


class IlluminationTexture(Texture):
    """
    Represent a texture that uses a color grid to store illumination
    information.

    Attributes:
        width(int): The width of the grid
        height(int): The height of the grid
        data(ndarray): The grid with the data
    """
    def __init__(self, width=DEFAULT_MAP_WIDTH, height=DEFAULT_MAP_HEIGHT):
        Texture.__init__(self)
        self.width = width
        self.height = height
        self.data = np.zeros((height, width, RGB_CHANNELS), np.uint8)

    def load(self, filename):
        img = Image.open(filename)
        self.data = np.asarray(img)

    def add_color(self, u, v, color, blerp=True):
        x = u * self.width
        y = v * self.height
        # Flip y value to go from bottom to top
        y = self.height - y
        # nearest neighbor pixel
        i = int(round(x))
        j = int(round(y))
        if i == self.width:
            i -= 1
        if j == self.height:
            j -= 1
        # Clip color to 0-255
        color = np.clip(color, 0, MAX_COLOR_VALUE)
        if i == 0 or j == 0 or i == self.width or j == self.height or not blerp:
            if i == self.width:
                i -= 1
            if j == self.height:
                j -= 1
            self.data[j][i] = color.astype(np.uint8)
        # t and s are interpolation parameters that go from 0 to 1
        t = x - i + 0.5
        s = y - j + 0.5
        # Bilinear interpolation
        self.data[j - 1][i - 1] += np.round((1 - t) * (1 - s) * color).astype(
            np.uint8
        )
        self.data[j - 1][i] += np.round(t * (1 - s) * color).astype(
            np.uint8
        )
        self.data[j][i - 1] += np.round((1 - t) * s * color).astype(
            np.uint8
        )
        self.data[j][i] += np.round(t * s * color).astype(
            np.uint8
        )

    def get_color(self, u, v):
        x = u * self.width
        y = v * self.height
        # Flip y value to go from bottom to top
        y = self.height - y
        # nearest neighbor pixel
        i = int(round(x))
        j = int(round(y))
        return self.data[j][i]

    def get_interpolated_color(self, u, v):
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
        if u < 0 or u > 1:
            u = u - np.floor(u)
            if u < 0:
                u = 1 - u
        if v < 0 or v > 1:
            v = v - np.floor(v)
            if v < 0:
                v = 1 - v
        # Don't use tiling
        # if u < 0 or u > 1:
            # raise ValueError(f"u={u} should be between 0 and 1")
        # if v < 0 or v > 1:
            # raise ValueError(f"v={v} should be between 0 and 1")
        x = u * self.width
        y = v * self.height
        # Flip y value to go from bottom to top
        y = self.height - y
        # Interpolate values of pixel neighborhood of x and y
        i = int(np.round(x))
        j = int(np.round(y))
        # But not in the borders
        if i == 0 or j == 0 or i == self.width or j == self.height:
            if i == self.width:
                i -= 1
            if j == self.height:
                j -= 1
            return self.data[j][i]
        # t and s are interpolation parameters that go from 0 to 1
        t = x - i + 0.5
        s = y - j + 0.5
        # Bilinear interpolation
        color = (
            self.data[j - 1][i - 1] * (1 - t) * (1 - s)
            + self.data[j - 1][i] * t * (1 - s)
            + self.data[j][i - 1] * (1 - t) * s
            + self.data[j][i] * t * s
        )[:3]   # Ensure this only gives RGB and not A
        return color
