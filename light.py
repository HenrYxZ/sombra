POINT_LIGHT = "point"
DIRECTIONAL_LIGHT = "directional"


class Light:
    """
    Light for a Scene
    """

    def __init__(self, position, type):
        self.position = position
        self.type = type
