POINT_LIGHT = "point"
DIRECTIONAL_LIGHT = "directional"


class Light(object):
    """
    Light for a Scene
    """

    def __init__(self, position, type):
        self.position = position
        self.type = type
