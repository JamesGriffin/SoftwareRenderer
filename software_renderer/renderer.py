import sys
import time
import pygame
import numpy as np


class Renderer(object):
    """
    Software Renderer
    """

    def __init__(self, width, height, title):
        # Basic window parameters
        self.width = width
        self.height = height

        # Pixel Framebuffer
        self.framebuffer = np.zeros([width, height, 3])
        # Initialise PyGame Surface
        pygame.init()
        pygame.display.set_caption(title)
        self.surface = pygame.display.set_mode((width, height))

        # Time
        self.last_update = time.time()

        # Font
        self.font = pygame.font.SysFont("Arial", 12)

    # Calculate time delta since last update
    def get_delta(self):
        return time.time() - self.last_update

    # Clear screen and fill with color (default is grey)
    def clear(self, colour=(128, 128, 128)):
        self.surface.fill(colour)
        self.framebuffer = pygame.surfarray.array3d(self.surface)

    # Clear screen and draw checkerboard
    def draw_checkerboard(self, c1=(45, 45, 45), c2=(40, 40, 40), square_size=32):
        self.clear(c1)

        for x in xrange(0, self.width, square_size):
            for y in xrange(0, self.height, square_size):
                if (x / square_size) % 2 == (y / square_size) % 2:
                    pygame.draw.polygon(self.surface, c2, ((x, y), (x + square_size, y),
                                                           (x + square_size, y + square_size), (x, y + square_size)), 0)

        self.framebuffer = pygame.surfarray.array3d(self.surface)



    # Draw a single pixel at x,y with specified colour
    def draw_pixel(self, x, y, colour):
        if (0 <= x < self.width) and (0 <= y < self.height):
            self.framebuffer[x][y] = colour

    # Draw FPS counter
    def draw_fps_counter(self):
        # Create text surfaces
        text_surface_outline = self.font.render(("%d FPS" % (1 / self.get_delta())), True, (64, 64, 64))
        text_surface = self.font.render(("%d FPS" % (1 / self.get_delta())), True, (255, 255, 255))

        # Blit text multiple times to create outline
        self.surface.blit(text_surface_outline, (7, 8))
        self.surface.blit(text_surface_outline, (9, 8))
        self.surface.blit(text_surface_outline, (8, 7))
        self.surface.blit(text_surface_outline, (8, 9))

        self.surface.blit(text_surface, (8, 8))

    # Update display
    def update(self):
        pygame.surfarray.blit_array(self.surface, self.framebuffer)
        self.draw_fps_counter()
        pygame.display.update()
        self.last_update = time.time()

    # Process pygame events
    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
