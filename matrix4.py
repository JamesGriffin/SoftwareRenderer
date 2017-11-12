import math
import numpy as np


class Matrix4(object):
    """
    Represents a 4x4 matrix used for transformations.
    """

    # Initialise with identity matrix
    def __init__(self):
        self.m = np.array([
            [1.0, 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0]
        ])

    # Transform vector r using matrix
    def transform(self, r):
        return np.array([
            self.m[0][0] * r[0] + self.m[0][1] * r[1] + self.m[0][2] * r[2] + self.m[0][3] * r[3],
            self.m[1][0] * r[0] + self.m[1][1] * r[1] + self.m[1][2] * r[2] + self.m[1][3] * r[3],
            self.m[2][0] * r[0] + self.m[2][1] * r[1] + self.m[2][2] * r[2] + self.m[2][3] * r[3],
            self.m[3][0] * r[0] + self.m[3][1] * r[1] + self.m[3][2] * r[2] + self.m[3][3] * r[3]
        ])

    # Initialise and return screen space transform matrix
    def init_screen_space_transform(self, half_width, half_height):
        self.m = np.array([
            [half_width, 0.0, 0.0, half_width],
            [0.0, -half_height, 0.0, half_height],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0]
        ])

        return self

    # Initialise and return translation matrix
    def init_translation(self, x, y, z):
        self.m[0][0] = 1.0
        self.m[0][1] = 0.0
        self.m[0][2] = 0.0
        self.m[0][3] = x

        self.m[1][0] = 0.0
        self.m[1][1] = 1.0
        self.m[1][2] = 0.0
        self.m[1][3] = y

        self.m[2][0] = 0.0
        self.m[2][1] = 0.0
        self.m[2][2] = 1.0
        self.m[2][3] = z

        self.m[3][0] = 0.0
        self.m[3][1] = 0.0
        self.m[3][2] = 0.0
        self.m[3][3] = 1.0

        return self

    # Initialise and return perspective transformation matrix
    def init_perspective(self, fov, aspect_ratio, z_near, z_far):
        
        tan_half_fov = float(np.tan(np.radians(fov) / 2))
        z_range = z_near - z_far

        self.m[0][0] = 1.0 / (tan_half_fov * aspect_ratio)
        self.m[0][1] = 0.0
        self.m[0][2] = 0.0
        self.m[0][3] = 0.0
        self.m[1][0] = 0.0
        self.m[1][1] = 1.0 / tan_half_fov
        self.m[1][2] = 0.0
        self.m[1][3] = 0.0
        self.m[2][0] = 0.0
        self.m[2][1] = 0.0
        self.m[2][2] = (-z_near - z_far) / z_range
        self.m[2][3] = 2 * z_far * z_near / z_range
        self.m[3][0] = 0.0
        self.m[3][1] = 0.0
        self.m[3][2] = 1.0
        self.m[3][3] = 0.0

        return self

    # Initialise and return rotation matrix
    def init_rotation(self, x, y, z):

        x = math.radians(x)
        y = math.radians(y)
        z = math.radians(z)

        rx = Matrix4()
        ry = Matrix4()
        rz = Matrix4()

        rz.m[0][0] = float(math.cos(z))
        rz.m[0][1] = -float(math.sin(z))
        rz.m[0][2] = 0.0
        rz.m[0][3] = 0.0
        rz.m[1][0] = float(math.sin(z))
        rz.m[1][1] = float(math.cos(z))
        rz.m[1][2] = 0.0
        rz.m[1][3] = 0.0
        rz.m[2][0] = 0.0
        rz.m[2][1] = 0.0
        rz.m[2][2] = 1.0
        rz.m[2][3] = 0.0
        rz.m[3][0] = 0.0
        rz.m[3][1] = 0.0
        rz.m[3][2] = 0.0
        rz.m[3][3] = 1.0

        rx.m[0][0] = 1.0
        rx.m[0][1] = 0.0
        rx.m[0][2] = 0.0
        rx.m[0][3] = 0.0
        rx.m[1][0] = 0.0
        rx.m[1][1] = float(math.cos(x))
        rx.m[1][2] = -float(math.sin(x))
        rx.m[1][3] = 0.0
        rx.m[2][0] = 0.0
        rx.m[2][1] = float(math.sin(x))
        rx.m[2][2] = float(math.cos(x))
        rx.m[2][3] = 0.0
        rx.m[3][0] = 0.0
        rx.m[3][1] = 0.0
        rx.m[3][2] = 0.0
        rx.m[3][3] = 1.0

        ry.m[0][0] = float(math.cos(y))
        ry.m[0][1] = 0.0
        ry.m[0][2] = -float(math.sin(y))
        ry.m[0][3] = 0.0
        ry.m[1][0] = 0.0
        ry.m[1][1] = 1.0
        ry.m[1][2] = 0.0
        ry.m[1][3] = 0.0
        ry.m[2][0] = float(math.sin(y))
        ry.m[2][1] = 0.0
        ry.m[2][2] = float(math.cos(y))
        ry.m[2][3] = 0.0
        ry.m[3][0] = 0.0
        ry.m[3][1] = 0.0
        ry.m[3][2] = 0.0
        ry.m[3][3] = 1.0

        self.m = np.dot(rz.m, np.dot(ry.m, rx.m))

        return self
