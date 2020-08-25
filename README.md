# Circle Packing
Reproducing the simplest version of the **circle packing** algorithm proposed in [this article](https://www.sciencedirect.com/science/article/pii/S0925772102000998)
by Collins and Stephenson.</br>
The **/src** folder contains the implementation of the algorithm written in C++ (the correspondent executables are located in **/bin**).</br>
In order to have a circle packing, we need to start with a **complex K**. In _cpack\_test_ the structure of such complex is hard-coded in the program.</br>
With the help of _cpack.py_ we can visualize an animation showing the creation of the circle packing as the algorithm progresses.<br>
The program should be run like this:
```
./bin/cpack_test | python ./src/cpack.py
```
