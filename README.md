# Sombra

Sombra is simple Raytracer written in pure Python. It's main purpose is to help
understand how raytracing works with a clean code. If you are looking for an
efficient Raytracer you should probably use something like C++. The equations
used are taken from the Image Synthesis class at Texas A&M University taught by
professor Ergun Akleman. 

The main program creates a raytraced image of a scene with simple objects like
spheres and planes. It's using a resolution of 288x192px by default and random
jitter anti-aliasing with 4 samples per axis.

![showcase image](showcase.jpg)

## Usage

- Install all dependencies by running `python -m pip install -r requirements.txt`
- Run `python -u main.py` or `python -u main.py -d` to use _debug mode_ which
will not use Anti-Aliasing (-u is for displaying print messages in the console)
- The output image will be stored in the project folder
- (Optional Parameters)
  - `python -u main.py -h` or `python -u main.py --help` will display the available commands
  - `python -u main.py -d` or `python -u main.py --debug` for image without anti-aliasing (would be much faster)
  - `python -u main.py -m` or `python -u main.py --multi` will use multi-threading
  - `python -u main.py -a` or `python -u main.py --animation` will create an 8 seconds animation
  - `python -u main.py -f` or `python -u main.py --dof` will use Depth of Field to simulate camera focus

## Features

- Sphere, Plane and Triangle objects
- Diffuse, Specular and Border shaders
- Area, Directional, Point and Spot lights
- Change Field of View of camera by changing d (distance) and scale x and y
parameters of the projection view window
- Anti-Aliasing using Random Jitter
- Reflection by setting Ks value to materials
- Image textures
- Normal Maps
- Environment Sphere Map
- Animation by running a physics simulation of a moving sphere
- Multi-Threading

## Documentation

You can see the documentation in the [wiki](https://github.com/HenrYxZ/sombra/wiki/Documentation)

## Testing

To run the tests use unittest in this way `python -m unittest -v tests`.
This will run every test in the "_tests_" module, if you add new tests make sure to
import them into the "_\_\_init\_\_.py_" file of the "_tests_" folder.

## Dependencies

You will need to install
- Python

And external Python modules
- numpy
- pillow
- progress

You can install the required python modules by running:
`python -m pip install -r requirements.txt`
or installing them individually:
`python -m pip install numpy pillow progress`

Developed by Jesús Henríquez
