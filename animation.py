from copy import deepcopy
import imageio
import numpy as np
import os
from PIL import Image

# Local Modules
from simulation import SphereBody, Simulation, State, SystemState


ANIM_OUT_DIR = "animation_out"
ANIM_VID_FILENAME = ANIM_OUT_DIR + "/animation.mp4"
MAX_QUALITY = 95
V0 = np.array([35, 0, 0], dtype=float)


class Transform:
    def __init__(self, translate=None, rotate=None, scale=None):
        self.translate = translate
        self.rotate = rotate
        self.scale = scale


class KeyFrame:
    def __init__(self, obj, frame_number, transform=None):
        self.obj = obj
        self.frame_number = frame_number
        if transform is None:
            self.transform = Transform()
        else:
            self.transform = transform

    def add_translate(self, translate):
        self.transform.translate = translate

    def add_rotate(self, rotate):
        self.transform.rotate = rotate

    def add_scale(self, scale):
        self.transform.scale = scale


def initialize_simulation(sphere):
    t = 0
    initial_state = SystemState(t)
    rigid_bodies = [SphereBody(sphere)]
    v = V0
    vx, vy, vz = v[0], v[1], v[2]
    wz = -1 * ((vx + vy) / sphere.radius)
    wx = (vz + vy) / sphere.radius
    wy = 0
    w = np.array([wx, wy, wz])
    body_initial_state = State(sphere.position, sphere.rotation, v, w)
    initial_state.add(body_initial_state)
    return initial_state, rigid_bodies


def create_keyframes_from_states(system_states, rigid_bodies):
    """
    Returns a list on which each element is a list of keyframes for the
    same frame number.
    """
    keyframes = []
    for i in range(len(system_states)):
        system_state = system_states[i]
        current_keyframes = []
        for j in range(len(system_state.bodies_state)):
            state = system_state.bodies_state[j]
            transform = Transform(state.pos, state.rot, state.scale)
            obj = rigid_bodies[j].obj
            keyframe = KeyFrame(obj, i, transform)
            current_keyframes.append(keyframe)
        keyframes.append(current_keyframes)
    return keyframes


class Animation:
    """
    This has the necessary parameters and functions for creating an
    animation. To do that it first has to run a simulation for a scene, then
    create a series of keyframes from the simulation data, then turn the
    keyframes into a series of scenes, and render each of them into images. It
    will create a new scene for each frame.
    """
    def __init__(self, duration, screen_size, fps, scene, render):
        self.duration = duration
        self.screen_size = screen_size
        self.fps = fps
        self.scene = scene
        # This is the render function to use
        self.render = render

    def create_scene_from_keyframes(self, keyframes):
        """
        Create a scene from the given keyframes that belong to the same frame
        number.
        """
        new_scene = deepcopy(self.scene)
        for keyframe in keyframes:
            new_obj = new_scene.objects[keyframe.obj.ID]
            new_obj.position = keyframe.transform.translate
            new_obj.rotation = keyframe.transform.rotate
            # scale is also possible
        return new_scene

    def create(self, sphere, camera):
        print("Creating animation...")
        time_step = 1.0 / self.fps
        initial_state, rigid_bodies = initialize_simulation(sphere)
        simulation = Simulation(
            initial_state, rigid_bodies, self.duration, time_step
        )
        f = -1 * (V0 / self.duration)
        print("Running simulation...")
        system_states = simulation.run(f)
        keyframes = create_keyframes_from_states(
            system_states, rigid_bodies
        )
        # Write video
        writer = imageio.get_writer(ANIM_VID_FILENAME, fps=self.fps)
        for i in range(len(keyframes)):
            # Create a new scene using the keyframe and render that scene
            current_keyframes = keyframes[i]
            new_scene = self.create_scene_from_keyframes(current_keyframes)
            w, h = self.screen_size
            print("Rendering frame={}/{}...".format(i, len(keyframes) - 1))
            img_arr = self.render(new_scene, camera, h, w)
            # Append rendered image into video
            writer.append_data(img_arr)
            # Write rendered image into image file
            img = Image.fromarray(img_arr)
            if not os.path.exists(ANIM_OUT_DIR):
                os.mkdir(ANIM_OUT_DIR)
            output_img_filename = "{}/{}.jpg".format(ANIM_OUT_DIR, i)
            img.save(output_img_filename, quality=MAX_QUALITY)
            print("Rendered image saved in {}".format(output_img_filename))
        writer.close()
        print("Animation video rendered in {}".format(ANIM_VID_FILENAME))
