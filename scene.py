class Scene:
    """
    Scene for raytracer that manages the objects and cameras.
    """

    def __init__(self, cameras, lights, objects, env_map=None):
        self.cameras = cameras
        self.lights = lights
        self.objects = objects
        self.env_map = env_map
