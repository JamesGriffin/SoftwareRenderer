from matrix4 import Matrix4


class RenderContext(object):
    """
    Render context is used for rendering polygons to a renderer instance
    """

    # Accepts renderer instance
    def __init__(self, renderer):
        self.renderer = renderer
        self.scan_buffer = [0 for x in xrange(renderer.height * 2)]

    # Draw x_min and x_max to scan buffer
    def draw_scan_buffer(self, y_coord, x_min, x_max):
        self.scan_buffer[y_coord * 2] = x_min
        self.scan_buffer[y_coord * 2 + 1] = x_max

    # Draw shape between y_min and y_max
    def draw_shape(self, y_min, y_max, fill=True):
        for j in xrange(y_min, y_max):
            x_min = self.scan_buffer[j * 2]
            x_max = self.scan_buffer[j * 2 + 1]

            # Ensure x_min and x_max are correctly assigned
            if x_min > x_max:
                x_min, x_max = x_max, x_min

            if fill:
                # Fill shape
                for i in xrange(x_min, x_max):
                    self.renderer.draw_pixel(i, j, (1, 86, 183))
            else:
                # Outline only
                self.renderer.draw_pixel(x_min, j, (1, 86, 183))
                self.renderer.draw_pixel(x_max, j, (1, 86, 183))

    # Draw triangle (v1, v2, v3)
    def draw_triangle(self, v1, v2, v3, fill=True):

        # Initialise screen space transform matrix
        matrix = Matrix4().init_screen_space_transform(float(self.renderer.width)/2.0, float(self.renderer.height)/2.0)

        # Apply screen space transform to vertices
        min_y_vert = v1.transform(matrix).perspective_divide()
        mid_y_vert = v2.transform(matrix).perspective_divide()
        max_y_vert = v3.transform(matrix).perspective_divide()

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
        self.draw_shape(int(min_y_vert.y), int(max_y_vert.y), fill=fill)

    # Write triangle lines scan buffer
    def scan_convert_triangle(self, min_y_vert, mid_y_vert, max_y_vert, handedness):
        self.scan_convert_line(min_y_vert, max_y_vert, 0 + handedness)
        self.scan_convert_line(min_y_vert, mid_y_vert, 1 - handedness)
        self.scan_convert_line(mid_y_vert, max_y_vert, 1 - handedness)

    # Write lines to scan buffer
    def scan_convert_line(self, min_y_vert, max_y_vert, handedness):

        y_start = int(min_y_vert.y)
        y_end = int(max_y_vert.y)
        x_start = int(min_y_vert.x)
        x_end = int(max_y_vert.x)

        y_dist = y_end - y_start
        x_dist = x_end - x_start

        if y_dist <= 0:
            return

        x_step = float(x_dist)/float(y_dist)
        cur_x = x_start

        for j in xrange(y_start, y_end):
            self.scan_buffer[j * 2 + handedness] = int(cur_x)
            cur_x += x_step
