import numpy as np
import matplotlib.pyplot as plt
import sys
import matplotlib as mpl

if __name__ == "__main__":

    # for _ in range(1):
    # reading the first line of STDIN
    vertices = list(map(int, sys.stdin.readline().split()))
    INTERIOR, BOUNDARY = vertices[0], vertices[1]

    radii = [[] for i in range(BOUNDARY + INTERIOR)] # empty list of lists

    # reading values of boundary radii
    bound_rad = list(map(float, sys.stdin.readline().split()))

    neigh = list() # neighbouring vertices
    angles = [[] for i in range(BOUNDARY + INTERIOR)]
    partial = [[] for i in range(BOUNDARY + INTERIOR)] # partial angle sum

    # appending 'fake values' for boundary vertices
    for i in range(BOUNDARY):
        neigh.append([-1])
        angles[i].append([-1])
        partial[i].append([-1])

    for _ in range(INTERIOR):
        # reading next n = INTERIOR lines of STDIN
        neigh.append(list(map(int, sys.stdin.readline().split())))

    while True:
        try:
            for i in range(INTERIOR):
                radii[i + BOUNDARY].append(float(sys.stdin.readline()))
                angles[i + BOUNDARY].append(list(map(float, sys.stdin.readline().split())))
                partial[i + BOUNDARY].append(list(map(float, sys.stdin.readline().split())))
        except:
            print("Reached EOF")
            break

    for i in range(BOUNDARY):
        for rep in range(len(radii[BOUNDARY])):
            radii[i].append(bound_rad[i])
            # boundary conditions don't change, so I append all equal values

    fig, ax = plt.subplots()
    ax.axis('equal') # forces same n. of pixels along different axes
    ax.set_xlim(-20, 20)
    ax.set_ylim(-20, 20)

    ims = []

    for call in [len(radii[0]) - 1]: # loop on the iterations of the algorithm
        # ims.append([])
        # # titles
        # title = ax.text(10, 10, "", bbox={'facecolor': 'w', 'alpha': 0.5, 'pad': 5},
        #                 transform=ax.transAxes, ha="center", animated=True)
        # title.set_text("Iteration n. %d" % call)
        # ims[call].append(title)

        already_drawn = list()
        centers = [[0, 0] for i in range(BOUNDARY + INTERIOR)] # position of the centers of the internal vertices
        # intially all set as (0, 0)
        print("centers: ", centers)
        # centers[BOUNDARY].append([0, 0]) # the first circle is always centered at the origin

        # progressive shifts will need to be taken into account
        shifts0 = [0 for i in range(BOUNDARY + INTERIOR)] # initially set them all as 0

        shifts1 = [0 for i in range(BOUNDARY + INTERIOR)] # initially set them all as 0

        # defining color map (helpful in debugging)
        cmap = mpl.cm.Paired
        color = 0

        to_draw = [x for x in range(BOUNDARY, BOUNDARY + INTERIOR)] # list of the interior vertices
        # exluding the first one cause it will always be drawn as first
        vertices = list()
        vertex = BOUNDARY

        l = 0

        while len(vertices) < INTERIOR: # loop on the flowers
            print("vertex: ", vertex)
            l += 1
            prev = 0
            # finding the current center among the petals of one of the previous flowers, if it is not present, skip
            # to the next one
            flag = False

            # special case for the first circle to draw
            if (vertex == BOUNDARY) & (vertex not in vertices):
                vertices.append(vertex)
            else:
                for v in vertices:
                    if (vertex in neigh[v]) & (vertex not in vertices):
                        print("v: ", v,"neigh[v]: ", neigh[v])
                        vertices.append(vertex)
                        print("vertices: ", vertices)
                        flag = True  # the vertex was found among the neighbours
                        prev = v # storing the node which has the current vertex as a neighbour
                        my_circ = neigh[v].index(vertex)
                        break

                if not flag:
                    print("VERTEX NOT FOUND among the neighbours of the circles already constructed\n"
                          "or ALREADY PRINTED")
                    l = l % INTERIOR  # go to the next vertex to draw
                    # not the most efficient method...
                    vertex = to_draw[l]
                    continue

            # CENTRAL CIRCLE
            xc = centers[vertex][0] # second index always 0 for how I defined the centers.. wanted to keep ordering
            yc = centers[vertex][1]
            r = radii[vertex][call] # central radius
            plt.scatter(xc, yc, color='r', s=2)

            if vertex not in already_drawn:
                circle = plt.Circle((xc, yc), r, color=cmap(color), fill=False)
                ax.add_artist(circle)
                already_drawn.append(vertex)

            # PETALS
            shift = 0 # to orientate the circles in a consistent manner
            if vertex > BOUNDARY:
                # now I consider the petal before it and I find it in the current flower
                my_shift = neigh[vertex].index(neigh[prev][my_circ - 1])
                print("my_shift: ", my_shift, "neigh[%d][%d]" % (vertex, my_shift), neigh[vertex][my_shift])
                print("partial[%d][%d]: " % (vertex, call), partial[vertex][call])

                # shift due to the fact the circle I'm considering could be not the first
                # among the neighbours of the current vertex --> as if I were placing it in first position
                shift0 = -(partial[vertex][call][my_shift - 1])

                if len(vertices) < INTERIOR + 1: # DEBUG
                    shift += shift0
                shifts0[vertex] = shift0
                print("shift0: ", shift0)

                # shift due to the fact the actual circle could be shifted more with respect to the first position
                # (which in the end should be at 360 = 0 deg)
                a = radii[prev][call] + radii[neigh[vertex][my_shift]][call]
                b = r + radii[prev][call]
                c = r + radii[neigh[vertex][my_shift]][call]
                ang1 = np.rad2deg(np.arccos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c)))
                ang2 = 180 - (partial[prev][call][my_circ - 1] + shifts1[prev] + shifts0[prev])
                # '+ shifts1' due to the fact the previous center has been rotated itself, so the angle sum should
                # be adjusted considered this
                shift1 = ang1 - ang2
                print("partial[%d][%d][%d]: " % (prev, call, my_circ - 1),
                      partial[prev][call][my_circ - 1], "shifts1: %.3f" % shifts1[prev])
                print("ang1: ", ang1, "ang2: ", ang2, "shift1: ", shift1)
                shifts1[vertex] = ang1 - ang2

                if len(vertices) < INTERIOR + 1: # DEBUG
                    shift += shift1
                print("shifts0:", shifts0[vertex])
                print("shifts1:", shifts1[vertex])

            for i in range(len(neigh[vertex])): # loop on the circles composing the petals
                n_circ = neigh[vertex][i] # index of the circle I am considering
                alpha = partial[vertex][call][i - 1] + shift

                if n_circ not in [100]:#already_drawn:
                    if n_circ > BOUNDARY - 1: # interior vertices
                        xv = xc + (r + radii[n_circ][call]) * np.cos(np.deg2rad(alpha))
                        yv = yc + (r + radii[n_circ][call]) * np.sin(np.deg2rad(-alpha))
                        centers[n_circ] = [xv, yv]
                        circle = plt.Circle((xv, yv), radii[n_circ][call], color=cmap(color), fill=False)
                    else: # boundary vertices
                        xv = xc + (r + 2) * np.cos(np.deg2rad(alpha))
                        yv = yc + (r + 2) * np.sin(np.deg2rad(-alpha))
                        circle = plt.Circle((xv, yv), 2, color=cmap(color), fill=False)

                    already_drawn.append(n_circ)
                    # plt.scatter(xv, yv, color='r')

                    ax.add_artist(circle)
            color += .1 # updating color map

            l = l % INTERIOR # go to the next vertex to draw
            vertex = to_draw[l]

        for i, val in enumerate(vertices):
            ax.annotate(i + BOUNDARY, (centers[i + BOUNDARY][0], centers[i + BOUNDARY][1]), size='8')

    # plt.savefig("./cpack_debug.jpg")

    plt.show()



