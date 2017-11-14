import math
import numpy as np


class Matrix4(object):
    """Represents a 4x4 matrix used for transformations."""

    def __init__(self, array=None):
        """Initialise with identity matrix or provided 2D array"""
        if array is not None:
            self.m = array
        else:
            self.m = np.identity(4)

    def transform(self, r):
        """Transform vector r using matrix"""
        return np.dot(self.m, r)

    @classmethod
    def init_screen_space_transform(cls, half_width, half_height):
        """Initialise and return screen space transform matrix"""
        return cls(
            np.array([
                [half_width, 0.0,           0.0,        half_width],
                [0.0,       -half_height,   0.0,        half_height],
                [0.0,        0.0,           1.0,        0.0],
                [0.0,        0.0,           0.0,        1.0]
            ])
        )

    @classmethod
    def init_translation(cls, x, y, z):
        """Initialise and return translation matrix"""
        matrix = cls()

        matrix.m[0][3] = x
        matrix.m[1][3] = y
        matrix.m[2][3] = z

        return matrix

    @classmethod
    def init_perspective(cls, fov, aspect_ratio, z_near, z_far):
        """Initialise and return perspective projection matrix"""
        tan_half_fov = float(np.tan(np.radians(fov) / 2))
        z_range = z_near - z_far

        return cls(
            np.array([
                [1.0 / (tan_half_fov * aspect_ratio), 0.0, 0.0, 0.0],
                [0.0, 1.0 / tan_half_fov, 0.0, 0.0],
                [0.0, 0.0, (-z_near - z_far) / z_range, 2 * z_far * z_near / z_range],
                [0.0, 0.0, 1.0, 0.0]
            ])
        )

    @classmethod
    def init_rotation(cls, x, y, z):
        """Initialise and return rotation matrix"""
        x = math.radians(x)
        y = math.radians(y)
        z = math.radians(z)

        rx = cls()
        ry = cls()
        rz = cls()

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

        return cls(np.dot(rz.m, np.dot(ry.m, rx.m)))
