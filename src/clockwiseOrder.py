import math
import matplotlib.pyplot as plt
import numpy as np

def clockw_ad(origin, point):
    refvec = [1, 0]
    # Vector between point and the origin: v = p - o
    vector = [point[0] - origin[0], point[1] - origin[1]]
    # Length of vector: ||v||
    lenvector = math.hypot(vector[0], vector[1])
    # If length is zero there is no angle
    if lenvector == 0:
        return -math.pi, 0
    # Normalize vector: v/||v||
    normalized = [vector[0] / lenvector, vector[1] / lenvector]
    dotprod  = normalized[0] * refvec[0] + normalized[1] * refvec[1]     # x1*x2 + y1*y2
    diffprod = refvec[1] * normalized[0] - refvec[0] * normalized[1]     # x1*y2 - y1*x2
    angle = math.atan2(diffprod, dotprod)
    # Negative angles represent counter-clockwise angles so we need to subtract them
    # from 2*pi (360 degrees)
    if angle < 0:
        return 2 * math.pi + angle, lenvector
    # I return first the angle because that's the primary sorting criterium
    # but if two vectors have the same angle then the shorter distance should come first.
    return angle, lenvector

if __name__ == "__main__":
    pts = [[2, 3], [5, 2], [4, 1], [3.5, 1], [1, 2], [2, 1], [3, 1], [3, 3], [4, 3]]
    ref = [2, 2]

    fig = plt.figure()
    ax = fig.gca()

    for i, val in enumerate(pts):
        ax.annotate(i, (pts[i][0], pts[i][1]), size='10')

    plt_pts = np.array(pts).T
    plt.scatter(plt_pts[0], plt_pts[1]) # points
    plt.scatter(ref[0], ref[1], color='r')

    cword = sorted(pts, key=lambda x: clockw_ad(ref, x))

    for i, val in enumerate(cword):
        ax.annotate(i, (cword[i][0], cword[i][1]), size='10', color='r',
                    textcoords='offset points', xytext=(8, -8))

    plt.show()