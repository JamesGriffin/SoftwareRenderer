import numpy as np
from matrix4 import Matrix4
from renderer import Renderer
from render_context import RenderContext
from vertex import Vertex

WIDTH = 800
HEIGHT = 600
WINDOW_TITLE = "Software Renderer"
MAX_FRAMERATE = 0

if __name__ == "__main__":

    # Create new renderer
    renderer = Renderer(WIDTH, HEIGHT, WINDOW_TITLE)

    # Create render context
    render_context = RenderContext(renderer)

    # Triangle
    v1 = Vertex(-1.0, -1.0, 0.0)
    v2 = Vertex(0.0, 1.0, 0.0)
    v3 = Vertex(1.0, -1.0, 0.0)

    projection = Matrix4().init_perspective(90, float(WIDTH) / float(HEIGHT), 0.1, 1000.0)
    rot_counter = -10.0
    # Render Loop
    while True:
        if MAX_FRAMERATE == 0 or renderer.get_delta() >= (1.0/MAX_FRAMERATE):
            renderer.process_events()
            renderer.clear((64, 64, 64))

            rot_counter -= 2000.0 * renderer.get_delta()
            translation = Matrix4().init_translation(0.0, 0.0, 2.5)
            rotation = Matrix4().init_rotation(-rot_counter, rot_counter, -rot_counter)

            transform = Matrix4()
            transform.m = np.dot(projection.m, np.dot(translation.m, rotation.m))

            render_context.fill_triangle(v1.transform(transform), v2.transform(transform), v3.transform(transform))

            renderer.draw_fps_counter()
            renderer.update()
