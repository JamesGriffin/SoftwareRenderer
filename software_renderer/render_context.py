import numpy as np
from vertex import Vertex
from matrix4 import Matrix4
from edge import Edge


class RenderContext(object):
    """Render context is used for rendering polygons to a renderer instance"""
    draw_backfaces = False

    def __init__(self, renderer):
        """Accepts renderer instance"""
        self.renderer = renderer

    def draw_triangle(self, v1, v2, v3, colour=(255, 255, 255), fill=True, shaded=True):
        """Draw triangle formed by v1, v2, v3"""

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
        handedness = area >= 0

        # Write triangles to scan buffer and then draw triangles
        self.scan_triangle(min_y_vert, mid_y_vert, max_y_vert, handedness, c, fill)

    def draw_triangles(self, triangles, colour=(255, 255, 255), fill=True, shaded=True):
        """Draw triangle formed by v1, v2, v3"""

        # Initialise screen space transform matrix
        matrix = Matrix4.init_screen_space_transform(float(self.renderer.width) / 2.0,
                                                     float(self.renderer.height) / 2.0)

        for tri in triangles:

            # Apply screen space transform to vertices
            min_y_vert = tri[0].transform(matrix).perspective_divide()
            mid_y_vert = tri[1].transform(matrix).perspective_divide()
            max_y_vert = tri[2].transform(matrix).perspective_divide()

            # Experimental shading
            normal = tri[0].triangle_normal(tri[1], tri[2])

            # Backface culling
            # if (not self.draw_backfaces) and min_y_vert.triangle_area(max_y_vert, mid_y_vert) >= 0:
            #     return

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
            handedness = area >= 0

            # Write triangles to scan buffer and then draw triangles
            self.scan_triangle(min_y_vert, mid_y_vert, max_y_vert, handedness, c, fill)

    def draw_mesh(self, indexed_mesh, transformation, colour=(255, 255, 255), fill=True, shaded=True):
        """Draw indexed mesh"""

        tris = [None] * (indexed_mesh.faces.__len__())
        idx = 0

        for tri in indexed_mesh.faces:
            v1, v2, v3 = map(lambda i: indexed_mesh.vertices[i-1], tri)

            v1 = Vertex(v1[0], v1[1], v1[2]).transform(transformation)
            v2 = Vertex(v2[0], v2[1], v2[2]).transform(transformation)
            v3 = Vertex(v3[0], v3[1], v3[2]).transform(transformation)

            tris[idx] = [v1, v2, v3]
            idx += 1

        tris = sorted(tris, reverse=True, key=lambda z: (z[0].z + z[1].z + z[2].z) / 3.0)

        # self.draw_triangles(tris)

        for tri in tris:
            self.draw_triangle(tri[0], tri[1], tri[2], colour, fill, shaded)

    def scan_triangle(self, min_y_vert, mid_y_vert, max_y_vert, handedness, colour, fill):
        """Draw triangle scan lines"""

        top_to_bottom = Edge(min_y_vert, max_y_vert)
        top_to_middle = Edge(min_y_vert, mid_y_vert)
        middle_to_bottom = Edge(mid_y_vert, max_y_vert)

        left = top_to_bottom
        right = top_to_middle

        if handedness:
            left, right = right, left

        y_start = top_to_middle.y_start
        y_end = top_to_middle.y_end

        for j in xrange(y_start, y_end):
            self.draw_scan_line(left, right, j, colour, fill)
            left.step()
            right.step()

        left = top_to_bottom
        right = middle_to_bottom

        if handedness:
            left, right = right, left

        y_start = middle_to_bottom.y_start
        y_end = middle_to_bottom.y_end

        for j in xrange(y_start, y_end):
            self.draw_scan_line(left, right, j, colour, fill)
            left.step()
            right.step()

    def draw_scan_line(self, left, right, j, colour, fill):
        x_min = int(np.ceil(left.x))
        x_max = int(np.ceil(right.x))

        # Ensure x_min and x_max are correctly assigned
        if x_min > x_max:
            x_min, x_max = x_max, x_min

        # Draw line
        for i in xrange(x_min, x_max):
            if (0 <= i < self.renderer.width) and (0 <= j < self.renderer.height):
                self.renderer.framebuffer[i][j] = colour
