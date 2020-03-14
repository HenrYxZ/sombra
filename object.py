class Object(object):
    """
    Represent a generic object inside the scene that has a specific position
    and intersect function
    """

    def __init__(self, arg):
        super(Object, self).__init__()
        self.arg = arg
