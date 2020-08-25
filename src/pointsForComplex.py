import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay
from collections import defaultdict
from itertools import permutations
import collections
from clockwiseOrder import clockw_ad
import time
import sys

def get_neighbours(triang, complex_points):
    _neighbors = defaultdict(set)  # set because I don't want repetitions
    for simplex in triang.vertices:
        for i, j in permutations(simplex, 2):
            _neighbors[i].add(j)

    points = [tuple(p) for p in triang.points]

    _coords_dict = {}
    for k, v in _neighbors.items():
        # also sorting the array elements in clockwise order here
        _coords_dict[points[k]] = sorted([points[i] for i in v], key=lambda x: clockw_ad(points[k], x))

    # going back to the indices
    complex_points = complex_points.T
    _index_dict = {}
    for k, v in _coords_dict.items():
        # print("key: ", k[0], k[1])
        ind_k = list(np.where((complex_points[0] == k[0]) & (complex_points[1] == k[1])))[0][0]
        # print("key index: ", ind_k)
        _index_dict[ind_k] = []
        for el in v:
            # print("value: ", el[0], el[1])
            ind_v = list(np.where((complex_points[0] == el[0]) & (complex_points[1] == el[1])))[0][0]
            # print("value index: ", ind_v)
            _index_dict[ind_k].append(ind_v)

        # print(_index_dict)

    # add -1 at the end of each element in the dict (for C++ code)
    for i in range(len(_index_dict)):
        _index_dict[i].append(-1)

    dict_list = list(map(list, sorted(_index_dict.items())))
    neigh_list = [x[1] for x in dict_list]
    return neigh_list

if __name__ == "__main__":
    BOUNDARY, INTERIOR = int(sys.argv[1]), int(sys.argv[2])
    if len(sys.argv) == 4:
        SEED = int(sys.argv[3])
        np.random.seed(SEED)

    # boundary chosen as a circle
    fig = plt.figure()
    ax = fig.gca()
    ax.axis('equal')
    R = 1
    bd = .2 # border between boundary and internal points
    x = np.linspace(-np.pi, np.pi - 2 * np.pi / BOUNDARY, BOUNDARY)
    boundary_points = np.array([[R * np.cos(a), R * np.sin(a)] for a in x])
    x_bound, y_bound = boundary_points.T
    internal_points = list()
    N = 0
    while N < INTERIOR:
        xi = np.random.uniform(-R, R)
        yi = np.random.uniform(-R, R)
        if xi ** 2 + yi ** 2 < (R - bd):
            internal_points.append([xi, yi])
            N += 1
    internal_points = np.array(internal_points)
    x_int, y_int = internal_points.T
    plt.scatter(x_bound, y_bound, s=25, color='r') # boundary points
    plt.scatter(x_int, y_int, s=5, color='b') # internal points
    # plt.show()
    complex_points = np.vstack((boundary_points, internal_points))
    # print("complex points: ", complex_points)
    # print("complex points.T: ", complex_points.T)

    dela = Delaunay
    triang = dela(complex_points)

    plt.triplot(complex_points[:, 0], complex_points[:, 1], triang.simplices.copy())
    for i, val in enumerate(complex_points):
        ax.annotate(i, (complex_points[i, 0], complex_points[i, 1]), size='10')

    neighbours = get_neighbours(triang, complex_points)[BOUNDARY:]

    print(BOUNDARY, INTERIOR)

    for i in range(INTERIOR):
        for j in range(len(neighbours[i])):
            print(neighbours[i][j], end=' ')
        print()

    plt.show()
    plt.savefig('../complex.jpg')
