# simple-raytracer

Simple Raytracer written in pure Python. It's main purpose is to help
understand how raytracing works with a clean code. If you are looking for an
efficient raytracer you should probably use something like C++. The equations
used are from the Image Synthesis class at Texas A&M University taught by
professor Ergun Akleman. 

It creates a raytraced image of a scene with simple objects like spheres and
planes. It's using a resolution of 280x192px by default and random jitter
anti-aliasing with 4 samples per axis.

![showcase image](showcase.jpg)

## Usage

- Install all dependencies by running `python -m pip install -r requirements.txt`
- Run `python -u main.py` or `python -u main.py -d` to use _debug mode_ which
will not use Anti-Aliasing (-u is for displaying print messages in the console)
- The output image will be stored in the project folder

## Features

- Sphere, Plane and Triangle objects
- Diffuse, Specular and Border shaders
- Directional, Point and Spot lights
- Change Field of View of camera by changing d (distance) and scale x and y
parameters
- Anti-Aliasing using Random Jitter
- Reflection by setting Ks value to materials
- Image textures
- Normal Maps
- Environment Sphere Map
- Animation by running a physics simulation of a moving sphere

## Testing

To run the tests use unittest in this way `python -m unittest -v tests`.
This will run every test in the "_tests_" module, if you add new tests make sure to
import them into the "_\_\_init\_\_.py_" file of the "_tests_" folder.

## Dependencies

You will need to install
- Python (python 2.7 and 3 are supported)

And external Python modules
- numpy
- pillow
- progress

You can install python modules, for example, by running:
`python -m pip install numpy pillow progress`
or running the requirements.txt:
`python -m pip install -r requirements.txt`

Developed by Jesús Henríquez
