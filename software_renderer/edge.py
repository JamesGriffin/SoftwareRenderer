import numpy as np


class Edge(object):
    """Represents an edge in 2D space"""
    def __init__(self, min_y_vert, max_y_vert):

        self.y_start = int(np.ceil(min_y_vert.y))
        self.y_end = int(np.ceil(max_y_vert.y))

        y_dist = max_y_vert.y - min_y_vert.y
        x_dist = max_y_vert.x - min_y_vert.x

        if y_dist <= 0:
            return

        y_prestep = self.y_start - min_y_vert.y

        self.x_step = float(x_dist) / float(y_dist)
        self.x = min_y_vert.x + y_prestep * self.x_step

    def step(self):
        self.x += self.x_step
