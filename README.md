# Gravitational Lens



## Getting started

The objectif of this Numerical Physics Project is to simulate a Gravitational Lens. To do that I will first make a simple 
2d simulation by defelcting the rays with a angle of deflection proportionnal to the gravitational potential. After this
simple simulation I will make a 3d simultaion whit the Ray-Tracing principale.


## Description

It's impossible to create an optic lens which captures the rays like a black hole. Because it's means that the speed of the light in the 
lense will be equal to zero, or the refraction index is equal to c/v, so for v=0 it's infinite. 
That's why to simulate a black hole with a event horizon a need to add an condition like, if the rayon is less closer than the 
Schwartzchild radius of the center of the black hope, the pixel is balck.

The first file named objet_gravitation contains every classes and functions used for the simulation and the file exe_gravitation
contened the executable code that creates the image with the different scenes. To change the scene you just have to
assign the varable "objects" with the list "galaxies", for the first scene, and "black_hole" for the second one. 
The computing can take, on my computer, about 2 or 3 minutes for both scenes.


## Roadmap
Next step -> optimization of the code


## Project status
In progress.
