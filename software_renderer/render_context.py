from matrix4 import Matrix4

import numpy as np
from vertex import Vertex


class RenderContext(object):
    """Render context is used for rendering polygons to a renderer instance"""
    draw_backfaces = False

    def __init__(self, renderer):
        """Accepts renderer instance"""
        self.renderer = renderer
        self.scan_buffer = [0 for x in xrange(renderer.height * 2)]

    def draw_scan_buffer(self, y_coord, x_min, x_max):
        """Draw x_min and x_max to scan buffer"""
        self.scan_buffer[y_coord * 2] = x_min
        self.scan_buffer[y_coord * 2 + 1] = x_max

    def draw_shape(self, y_min, y_max, fill=True, colour=(255, 255, 255)):
        """Draw shape between y_min and y_max"""
        for j in xrange(y_min, y_max):
            x_min = self.scan_buffer[j * 2]
            x_max = self.scan_buffer[j * 2 + 1]

            # Ensure x_min and x_max are correctly assigned
            if x_min > x_max:
                x_min, x_max = x_max, x_min

            if fill:
                # Fill shape
                for i in xrange(x_min, x_max):
                    self.renderer.draw_pixel(i, j, colour)
            else:
                # Outline only
                self.renderer.draw_pixel(x_min, j, colour)
                self.renderer.draw_pixel(x_max, j, colour)

    def draw_triangle(self, v1, v2, v3, colour=(255, 255, 255), fill=True, shaded=True):
        """# Draw triangle formed by v1, v2, v3"""

        # Initialise screen space transform matrix
        matrix = Matrix4.init_screen_space_transform(float(self.renderer.width)/2.0, float(self.renderer.height)/2.0)

        # Apply screen space transform to vertices
        min_y_vert = v1.transform(matrix).perspective_divide()
        mid_y_vert = v2.transform(matrix).perspective_divide()
        max_y_vert = v3.transform(matrix).perspective_divide()

        # Experimental shading
        normal = v1.triangle_normal(v2, v3)

        # Backface culling
        if (not self.draw_backfaces) and min_y_vert.triangle_area(max_y_vert, mid_y_vert) >= 0:
            return

        # Calculate shading
        if shaded:
            shading = np.dot(normal, np.array([-0.57735, -0.57735, 0.57735]))

            if shading < 0:
                shading = 0

            shading = np.array([shading, 0.2]).max()
        else:
            shading = 1

        c = (colour[0] * shading, colour[1] * shading, colour[2] * shading)

        # Swap vertices to reorder
        if min_y_vert.y > max_y_vert.y:
            temp = max_y_vert
            max_y_vert = min_y_vert
            min_y_vert = temp

        if min_y_vert.y > mid_y_vert.y:
            temp = mid_y_vert
            mid_y_vert = min_y_vert
            min_y_vert = temp

        if mid_y_vert.y > max_y_vert.y:
            temp = max_y_vert
            max_y_vert = mid_y_vert
            mid_y_vert = temp

        # Use triangle area to determine handedness
        area = min_y_vert.triangle_area(max_y_vert, min_y_vert)
        handedness = 1 if area >= 0 else 0

        # Write triangles to scan buffer and then draw triangles
        self.scan_convert_triangle(min_y_vert, mid_y_vert, max_y_vert, handedness)
        self.draw_shape(int(np.ceil(min_y_vert.y)), int(np.ceil(max_y_vert.y)), fill, c)

    def draw_mesh(self, indexed_mesh, transformation, colour=(255, 255, 255), fill=True, shaded=True):
        """Draw indexed mesh"""
        for tri in indexed_mesh.faces:
            v1, v2, v3 = map(lambda i: indexed_mesh.vertices[i-1], tri)

            v1 = Vertex(v1[0], v1[1], v1[2]).transform(transformation)
            v2 = Vertex(v2[0], v2[1], v2[2]).transform(transformation)
            v3 = Vertex(v3[0], v3[1], v3[2]).transform(transformation)

            self.draw_triangle(v1, v2, v3, fill=fill, colour=colour, shaded=shaded)

    def scan_convert_triangle(self, min_y_vert, mid_y_vert, max_y_vert, handedness):
        """Write triangle lines scan buffer"""
        self.scan_convert_line(min_y_vert, max_y_vert, 0 + handedness)
        self.scan_convert_line(min_y_vert, mid_y_vert, 1 - handedness)
        self.scan_convert_line(mid_y_vert, max_y_vert, 1 - handedness)

    def scan_convert_line(self, min_y_vert, max_y_vert, handedness):
        """Write lines to scan buffer"""
        y_start = int(np.ceil(min_y_vert.y))
        y_end = int(np.ceil(max_y_vert.y))

        y_dist = max_y_vert.y - min_y_vert.y
        x_dist = max_y_vert.x - min_y_vert.x

        if y_dist <= 0:
            return

        x_step = float(x_dist)/float(y_dist)
        y_prestep = y_start - min_y_vert.y
        cur_x = min_y_vert.x + y_prestep * x_step

        for j in xrange(y_start, y_end):
            self.scan_buffer[j * 2 + handedness] = int(np.ceil(cur_x))
            cur_x += x_step
