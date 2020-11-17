# Assignment 4 Atmospheric Light Scattering

## Introduction

I implemented a script that generates an image of a sky using atmospheric light scattering, using Ray casting with Python and some utilities libraries.
(Pillow for image creation, numpy for numeric arrays).
To run the program install the requirements:

`$ python -m pip install -r requirements.txt`

Then run:

`$ python run_example.py atmosphere`

## How it works

Atmospheric Light Scattering with rays works by shooting the rays like normal raytracing but intersecting with the atmosphere.
If the point of intersection is B and camera is A, we sample points along the segment between A and B. Each point has some density (the density increases near the
surface of the planet and decreases going higher) which models the amounts of particles at that altitude. Particles like Nitrogen or other gases in the atmosphere,
scatter the light that comes from the sun to the camera. That can be modeled with the Rayleigh Scattering equation.

For each sample along A to B, another segment is created from the sample point P to the direction where the sun comes from and the intersection of the atmosphere,
call that point C. That segment is also sampled to calculate the light coming from the sun that is scattered along. With that information one can calculate the
light for the point P.

For getting the total light at a point there is the optical depth that is the integration of density along the segment. We do that by making the sum of samples and
multiplying the segment that each sample has, just like one would sample the integral of a function by adding multiple columns that fall bellow the function.

I did by looking at the information in Chapter 16 of GPU Gems 2 - [link](https://developer.nvidia.com/gpugems/gpugems2/part-ii-shading-lighting-and-shadows/chapter-16-accurate-atmospheric-scattering)

And this video tutorial, but the code here didn't gave me good results - [link](https://www.youtube.com/watch?v=DxfEbulyFcY)

## Equations

- **Phase Function**: Determines a factor of light going to the direction of the camera
- **Out Scatter Equation**: How much light is scattered along the segment (wavelenght dependent)
- **In Scatter Equation**: How much light comes in along the segment (wavelenght dependent)

## The Code

The script is in *examples/atmosphere.py*. I defined a class SkyDome in *sky.py* that has all the logic for calculating light at a ray.
All the equations are defined in that class.

## Results

I'm rendering a 600x400 image in about 1min 30secs in a 8-core processor using multithread.
This is using 10 samples for sun rays and 10 for view rays. My results were not good, I think it is an issue with color. I get values that don't go, from 0 to 1.
And I clip them, but there I don't know exactly how to interpret them. There is also the problem of what should I use as the Illumination coming from the sun.
I tried using (1, 1, 1) and [1289, 1395, 1234] which is actual luminance from NASA for wavelengths R, G, B.

This is my result assuming RGB color:

![atmosphere colorful](examples_out/6_atmosphere_colorful.jpg)

This is my result transforming the color from I to XYZ with Color Matching and then from XYZ to sRGB with matrix:

![atmosphere](examples_out/6_atmosphere.jpg)


Jesús Henríquez
