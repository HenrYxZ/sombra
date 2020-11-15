class Scene:
    """
    Scene for raytracer that manages the objects and cameras.

    Attributes:
        cameras(list): The cameras for this scene
        lights(list): Light objects for this scene
        objects(list): List of Objects for this scene
        env_map(EnvironmentMap): The Environment Map
        sky_dome(SkyDome): A Sky Dome that can recreate a sky with atmosphere
            dependant on sun direction
    """

    def __init__(
            self, cameras, lights, objects, env_map=None,
            sky_dome=None, main_camera_idx=0
    ):
        self.cameras = cameras
        self.lights = lights
        self.objects = objects
        self.env_map = env_map
        self.sky_dome = sky_dome
        self.main_camera_idx = main_camera_idx

    def get_main_camera(self):
        return self.cameras[self.main_camera_idx]

    def is_empty(self):
        return not (self.objects or self.env_map or self.sky_dome)
