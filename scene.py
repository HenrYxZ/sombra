class Scene:
    """
    Scene for raytracer that manages the objects and cameras.
    """

    def __init__(
            self, cameras, lights, objects, env_map=None, main_camera_idx=0
    ):
        self.cameras = cameras
        self.lights = lights
        self.objects = objects
        self.env_map = env_map
        self.main_camera_idx = main_camera_idx

    def get_main_camera(self):
        return self.cameras[self.main_camera_idx]
