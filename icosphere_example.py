import time
import numpy as np
from software_renderer import Renderer, RenderContext, IndexedMesh, Matrix4

WIDTH = 640
HEIGHT = 480
WINDOW_TITLE = "Icosphere"
MAX_FRAMERATE = 0

if __name__ == "__main__":

    # Create new renderer
    renderer = Renderer(WIDTH, HEIGHT, WINDOW_TITLE)

    # Create render context
    render_context = RenderContext(renderer)

    # Load mesh
    mesh = IndexedMesh("obj/ico.obj")

    # Initialise perspective projection matrix
    projection = Matrix4.init_perspective(45.0, float(WIDTH) / float(HEIGHT), 0.1, 1000.0)

    # Stores mesh rotation amount
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

            # Calculate time delta and update mesh rotation
            delta = time.time() - previous_time
            rot_counter += 50 * delta
            previous_time = time.time()

            # Initialise translation and rotation matrices
            translation = Matrix4().init_translation(0.0, 0.0, 2.5)
            rotation = Matrix4().init_rotation(0.0, rot_counter, rot_counter / 2.0)

            # Dot product matrices to form final transformation matrix
            transform = Matrix4()
            transform.m = np.dot(projection.m, np.dot(translation.m, rotation.m))

            # Draw transformed mesh
            render_context.draw_mesh(mesh, transform, colour=(50, 200, 60))

            # Draw FPS counter and update screen
            renderer.draw_fps_counter()
            renderer.update()
