class Scene(object):
    """
    Scene for raytracer that manages the objects and cameras.
    """

    def __init__(self, cameras, lights, objects):
        self.cameras = cameras
        self.lights = lights
        self.objects = objects
