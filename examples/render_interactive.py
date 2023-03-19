"""
Example that uses the pyglet module to display the image as it renders
"""
import numpy as np
from progress.bar import Bar
import pyglet
from PIL import Image
import pyglet.window.key as key

# Local Modules
from camera import Camera
from constants import RGB_CHANNELS, MAX_QUALITY
from material import Material, TYPE_TEXTURED
from object import Plane
from raytrace import raytrace
from render import create_ray_aa
from scene import Scene
from texture import ImageTexture
import shaders
import utils

from main import setup_scene

WIDTH = 288
HEIGHT = 192
H_SAMPLES = 3
V_SAMPLES = 3


screen = np.zeros(
    [HEIGHT, WIDTH, RGB_CHANNELS], dtype=np.uint8
)
IMG_FORMAT = 'RGB'
pitch = WIDTH * RGB_CHANNELS
image_data = pyglet.image.ImageData(
    WIDTH, HEIGHT, IMG_FORMAT, screen.tobytes(), pitch
)
window = pyglet.window.Window(WIDTH, HEIGHT, caption="Sombra")


def set_camera():
    camera_pos = np.array([0.0, 0.2, 0.0])
    v_view = utils.normalize(np.array([-1.0, 0.0, 2.0]))
    v_up = np.array([0.0, 1.0, 0.0])
    # d, scale_x and scale_y are camera parameters that define the view window
    # in world space
    return Camera(camera_pos, v_view, v_up, d=0.26, scale_x=0.4, scale_y=0.3)


def set_scene():
    pos = np.array([0.0, 0.0, 0])
    mat = Material(material_type=TYPE_TEXTURED)
    texture = ImageTexture("./textures/checkers.png")
    mat.add_texture(texture)
    # Normal of the plane
    n = np.array([0.0, 1.0, 0.0])
    # n0 vector of the plane (vector lying in the plane)
    n0 = np.array([1.0, 0.0, 0.0])
    # Scale for the texture in x and y
    sx = 4
    sy = 4
    plane = Plane(pos, mat, shaders.TYPE_FLAT, n, n0, sx, sy)
    cameras = [set_camera()]
    return Scene(cameras, [], [plane])


# scene = set_scene()
# camera = set_camera()
scene = setup_scene()
camera = scene.get_main_camera()
camera.position = np.array([-15, 0, -5])
camera.set_view_coord()

pause = True


def render(_):
    global j
    if pause:
        return
    if j == HEIGHT:
        bar.finish()
        pyglet.clock.unschedule(render)
        # Save image in file
        img = Image.fromarray(screen)
        img_filename = "examples_out/interactive.jpg"
        img.save(img_filename, quality=MAX_QUALITY)
        print(f"Image saved in {img_filename}")
        return
    for i in range(WIDTH):
        color = np.array([0, 0, 0], dtype=float)
        for n in range(V_SAMPLES):
            for m in range(H_SAMPLES):
                pixel_pos = (j, i, n, m)
                ray = create_ray_aa(
                    camera, HEIGHT, WIDTH, V_SAMPLES, H_SAMPLES, pixel_pos
                )
                color += raytrace(ray, scene) / float(total_samples)
        bar.next()
        screen[j][i] = color.round().astype(np.uint8)
    j += 1
    draw()


def draw():
    window.clear()
    # Bytes data of numpy array and flipped upside down
    data = np.flipud(screen).tobytes()
    image_data.set_data(IMG_FORMAT, pitch, data)
    image_data.blit(0, 0)


@window.event
def on_key_press(symbol, _):
    global pause
    if symbol == key.SPACE:
        pause = not pause


if __name__ == '__main__':
    print("Press SPACE to start")
    total_samples = H_SAMPLES * V_SAMPLES
    # This is for showing progress %
    iterations = HEIGHT * WIDTH
    bar = Bar(
        'Raytracing',
        max=iterations,
        suffix='%(percent)d%% [%(elapsed_td)s / %(eta_td)s]',
        check_tty=False
    )
    j = 0
    pyglet.clock.schedule(render)
    pyglet.app.run()
