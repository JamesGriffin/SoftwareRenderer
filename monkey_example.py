import time
import sys
import numpy as np
import pygame
from software_renderer import Renderer, RenderContext, IndexedMesh, Matrix4

WIDTH = 640
HEIGHT = 460
WINDOW_TITLE = "Monkey"
MAX_FRAMERATE = 0

if __name__ == "__main__":

    # Create new renderer
    renderer = Renderer(WIDTH, HEIGHT, WINDOW_TITLE)

    # Create render context
    render_context = RenderContext(renderer)
    render_context.draw_backfaces = False

    # Load mesh
    mesh = IndexedMesh("obj/monkey.obj")

    # Initialise perspective projection matrix
    projection = Matrix4.init_perspective(60.0, float(WIDTH) / float(HEIGHT), 0.1, 1000.0)

    # Stores mesh rotation amount
    rot_counter = [0.0, 0.0]

    # Stores time of last update
    previous_time = time.time()

    mouse_clicked = False
    mouse_last_position = None
    zoom = 0.0

    # Render Loop
    while True:
        if MAX_FRAMERATE == 0 or renderer.get_delta() >= (1.0/MAX_FRAMERATE):

            mouse_delta = [0, 0]

            # Handle user events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_clicked = True

                    if event.button == 4:
                        zoom -= 0.25

                    if event.button == 5:
                        zoom += 0.25

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        mouse_clicked = False
                        mouse_last_position = None

                if event.type == pygame.MOUSEMOTION:
                    pos = pygame.mouse.get_pos()
                    if mouse_last_position is not None and mouse_clicked:
                        mouse_delta = [
                            mouse_delta[0] + (mouse_last_position[0] - pos[0]),
                            mouse_delta[1] + (mouse_last_position[1] - pos[1]),
                        ]
                    mouse_last_position = pos

            # Clear screen and draw checkerboard
            renderer.draw_checkerboard()

            # Calculate time delta and update mesh rotation
            delta = time.time() - previous_time

            if not mouse_clicked:
                rot_counter[0] += 50 * delta
                rot_counter[1] += 50 * delta

            rot_counter[0] += mouse_delta[0]
            rot_counter[1] += mouse_delta[1]

            previous_time = time.time()

            # Initialise translation and rotation matrices
            translation = Matrix4.init_translation(0.0, 0.0, 3.0 + zoom)
            rotation = Matrix4.init_rotation(rot_counter[1], -rot_counter[0], 0.0)

            # Dot product matrices to form final transformation matrix
            transform = Matrix4(np.dot(projection.m, np.dot(translation.m, rotation.m)))

            # Draw transformed mesh
            render_context.draw_mesh(mesh, transform, fill=False, shaded=True, colour=(255, 255, 255))

            # Update screen
            renderer.update()
