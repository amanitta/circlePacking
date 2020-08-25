import numpy as np
import matplotlib.pyplot as plt
import sys
import matplotlib as mpl
import matplotlib.animation as animation

if __name__ == "__main__":

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

    fig = plt.figure()
    ax = fig.gca()
    ax.axis('equal') # forces same n. of pixels along different axes
    ax.set_xlim(-20, 20)
    ax.set_ylim(-20, 20)
    ax.set_xticks([])
    ax.set_yticks([])

    ims = []

    for call in range(len(radii[0])): # loop on the iterations of the algorithm
        ims.append([])
        # titles
        title = ax.text(.5, .9, "", bbox={'facecolor': 'w', 'alpha': 0.5, 'pad': 5},
                        transform=ax.transAxes, ha="center", animated=True)
        title.set_text("Iteration n. %d" % call)
        ims[call].append(title)

        already_drawn = list()
        centers = [[0, 0] for i in range(BOUNDARY + INTERIOR)] # position of the centers of the internal vertices
        # intially all set as (0, 0)

        # progressive shifts will need to be taken into account
        shifts = [0 for i in range(BOUNDARY + INTERIOR)]  # initially set them all as 0

        # defining color map (helpful in debugging)
        cmap = mpl.cm.Paired
        color = 0

        to_draw = [x for x in range(BOUNDARY, BOUNDARY + INTERIOR)] # list of the interior vertices
        # exluding the first one cause it will always be drawn as first
        vertices = list()
        vertex = BOUNDARY

        l = 0
        while len(vertices) < INTERIOR: # loop on the flowers
            # print(vertex)
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
                        vertices.append(vertex)
                        # print("vertices: ", vertices)
                        flag = True  # the vertex was found among the neighbours
                        prev = v
                        my_circ = neigh[v].index(vertex)
                        break

                if not flag:
                    # print("VERTEX NOT FOUND among the neighbours of the circles already constructed\n"
                    #       "or ALREADY PRINTED")
                    l = l % INTERIOR # go to the next vertex to draw
                    # not the most efficient method...
                    vertex = to_draw[l]
                    continue

            # CENTRAL CIRCLE
            xc = centers[vertex][0] # first index always 0 for how I defined the centers.. wanted to keep ordering
            yc = centers[vertex][1]
            r = radii[vertex][call] # central radius
            cent = ax.scatter(xc, yc, color='r', s=2, animated=True)
            # appending centers to the animation
            ims[call].append(cent)

            if vertex not in already_drawn:
                circle = plt.Circle((xc, yc), r, color=cmap(color), fill=False, animated=True)
                ims[call].append(ax.add_artist(circle))
                already_drawn.append(vertex)

            # PETALS
            shift = 0 # to orientate the circles in a consistent manner
            if vertex > BOUNDARY:
                # now I consider the petal before it and I find it in the current flower
                my_shift = neigh[vertex].index(neigh[prev][my_circ - 1])
                # shift due to the fact the circle I'm considering could not be the first
                # among the neighbours of the current vertex --> as if I were placing it in first position
                shift0 = -(partial[vertex][call][my_shift - 1])
                shift += shift0
                # shift due to the fact the actual circle could be shifted more with respect to the first position
                # (which in the end should be at 360 = 0 deg)
                a = radii[prev][call] + radii[neigh[vertex][my_shift]][call]
                b = r + radii[prev][call]
                c = r + radii[neigh[vertex][my_shift]][call]
                ang1 = np.rad2deg(np.arccos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c)))
                ang2 = 180 - (partial[prev][call][my_circ - 1] + shifts[prev])
                # '+ shifts[]' due to the fact the previous center has been rotated itself, so the angle sum should
                # be adjusted considered this
                shift1 = (ang1 - ang2)
                shift += shift1
                shifts[vertex] = shift

            for i in range(len(neigh[vertex])): # loop on the circles composing the petals
                n_circ = neigh[vertex][i] # index of the circle I am considering
                alpha = partial[vertex][call][i - 1] + shift

                if n_circ not in already_drawn:
                    xv = xc + (r + radii[n_circ][call]) * np.cos(np.deg2rad(alpha))
                    yv = yc + (r + radii[n_circ][call]) * np.sin(np.deg2rad(-alpha))
                    centers[n_circ] = [xv, yv]
                    circle = plt.Circle((xv, yv), radii[n_circ][call], color=cmap(color), fill=False, animated=True)
                    already_drawn.append(n_circ)
                    # plt.scatter(xv, yv, color='r')

                    # appending to the list for the animation
                    ims[call].append(ax.add_artist(circle))

            color += .1 # updating color map

            l = l % INTERIOR # go to the next vertex to draw
            vertex = to_draw[l]

    ani = animation.ArtistAnimation(fig, ims, interval=500, blit=True, repeat_delay=1000)

    ani.save("cpack_01.gif", writer='imagemagick') # save as .gif

    # show animation
    plt.show()

