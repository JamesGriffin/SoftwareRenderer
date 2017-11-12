import numpy as np


class Vertex(object):
    """
    Represents a vertex with a 2D array
    """
    def __init__(self, x=0, y=0, z=0, w=1):
        self.pos = [x, y, z, w]

    def set_pos(self, pos):
        self.pos = pos
        return self

    @property
    def x(self):
        return self.pos[0]

    @property
    def y(self):
        return self.pos[1]

    @property
    def z(self):
        return self.pos[2]

    @property
    def w(self):
        return self.pos[3]

    def transform(self, matrix):
        return Vertex().set_pos(matrix.transform(self.pos))

    def perspective_divide(self):
        return Vertex().set_pos([self.x/self.w, self.y/self.w, self.z/self.w, self.w])

    # Calculate triangle area
    def triangle_area(self, max_y_vert, mid_y_vert):
        x1 = max_y_vert.x - self.x
        y1 = max_y_vert.y - self.y

        x2 = mid_y_vert.x - self.x
        y2 = mid_y_vert.y - self.y

        return (x1 * y2 - x2 * y1) / 2
