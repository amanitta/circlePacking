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

The other python script provides instead a way to create a complex with a certain number of boundary and interior points. The geometrical form of the complex is not important at all: the only thing which is relevant is knowing the neighbouring nodes to which each interior vertex is connected. The script thus places the boundary points equally spaced on a circle, while the interior points are chosen at random inside the circle itself. To program should thus be run like this
```
python pointsForComplex.py BOUNDARY INTERIOR [SEED]
```
<p align="center">
  <img src="https://github.com/amanitta/circlePacking/blob/master/complex.jpg">
</p>

  
