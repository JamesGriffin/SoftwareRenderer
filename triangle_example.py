import time
import numpy as np
from software_renderer.matrix4 import Matrix4
from software_renderer.renderer import Renderer
from software_renderer.render_context import RenderContext
from software_renderer.vertex import Vertex

WIDTH = 640
HEIGHT = 480
WINDOW_TITLE = "3D Triangle"
MAX_FRAMERATE = 0

if __name__ == "__main__":

    # Create new renderer
    renderer = Renderer(WIDTH, HEIGHT, WINDOW_TITLE)

    # Create render context
    render_context = RenderContext(renderer)
    render_context.draw_backfaces = True

    # Triangle
    v1 = Vertex(-1.0, -1.0, 0.0)
    v2 = Vertex(0.0, 1.0, 0.0)
    v3 = Vertex(1.0, -1.0, 0.0)

    # Initialise perspective projection matrix
    projection = Matrix4.init_perspective(45.0, float(WIDTH) / float(HEIGHT), 0.1, 1000.0)

    # Stores triangle rotation amount
    rot_counter = 0.0

    # Stores time of last update
    previous_time = time.time()

    # Render Loop
    while True:
        if MAX_FRAMERATE == 0 or renderer.get_delta() >= (1.0/MAX_FRAMERATE):

            # Handle user events
            renderer.process_events()

            # Clear screen and draw checkerboard
            renderer.draw_checkerboard()

            # Calculate time delta and update triangle rotation
            delta = time.time() - previous_time
            rot_counter += 100 * delta
            previous_time = time.time()

            # Initialise translation and rotation matrices
            translation = Matrix4.init_translation(0.0, 0.0, 4.0)
            rotation = Matrix4.init_rotation(0.0, rot_counter, rot_counter / 2.0)

            # Dot product matrices to form final transformation matrix
            transform = Matrix4(np.dot(projection.m, np.dot(translation.m, rotation.m)))

            # Draw transformed triangle
            render_context.draw_triangle(v1.transform(transform), v2.transform(transform), v3.transform(transform),
                                         colour=(50, 200, 60), fill=False, shaded=False,)

            # Update screen
            renderer.update()
