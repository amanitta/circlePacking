# Circle Packing
Reproducing the simplest version of the **circle packing** algorithm proposed in [this article](https://www.sciencedirect.com/science/article/pii/S0925772102000998)
by Collins and Stephenson.</br></br>
The **/src** folder contains the implementation of the algorithm written in C++ (the correspondent executables are located in **/bin**).</br></br>
In order to have a circle packing, we need to start with a **complex K**. In _cpack\_test.cc_ the structure of such complex is hard-coded in the program.</br>
With the help of _cpack.py_ we can visualize an animation showing the creation of the circle packing as the algorithm progresses.<br>
The program should be run like this:
```
./bin/cpack_test | python ./src/cpack.py
```
<p align="center">
<img src="https://github.com/amanitta/circlePacking/blob/master/cpack_01.gif"/>
</p>
It is possible to choose between fixed (default) and random boundary conditions using the options -f or -f in _cpack_test_.</br></br>

The other python script provides instead a way to create a complex with a certain number of boundary and interior points. The geometrical form of the complex is not important at all: the only thing which is relevant is knowing the neighbouring nodes to which each interior vertex is connected. The script thus places the boundary points equally spaced on a circle, while the interior points are chosen at random inside the circle itself. A Delaunay triangulation is exploited to link the vertices inside the circle. The output of the script consists of the list of neighbours for each internal vertex, sorted in clockwise order.</br>
The program should be run like this
```
python pointsForComplex.py BOUNDARY INTERIOR [SEED]
```
<p align="center">
  <img src="https://github.com/amanitta/circlePacking/blob/master/complex.jpg">
</p>

The output of the python script just mentioned can then be fed to _cpack_final_, which reads the structure of the complex created and runs the circle packing algorithm.</br>
_cpack_debug.py_ is extremely useful for debugging the program and understanding how the animation is created. It can also be used to show the final result of the run, as shown below.
```
 python ./src/pointsForComplex.py 9 8 30 | ./bin/cpack_final | python ./src/cpack_debug.py 
```
<p align="center">
  <img src="https://github.com/amanitta/circlePacking/blob/master/cpack_debug.jpg">
</p>

Just as before, we can then produce an animation showing the action of the packing algorithm, now with an input (the complex) that has not to be hard-coded anywhere.
```
python ./src/pointsForComplex.py 20 25 987 | ./bin/cpack_final | python ./src/cpack.py 
```
Complex             |  Circle Packing
:-------------------------:|:-------------------------:
<img src="https://github.com/amanitta/circlePacking/blob/master/complex_final.jpg" width=500 height=400/> | <img src="https://github.com/amanitta/circlePacking/blob/master/cpack_final.gif" width=500 height=400/>




