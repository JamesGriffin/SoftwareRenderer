import sys
import time
import pygame


class Renderer(object):
    """
    Software Renderer
    """
    def __init__(self, width, height, title):
        # Basic parameters
        self.width = width
        self.height = height

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

    # Draw a single pixel at x,y with specified colour
    def draw_pixel(self, x, y, colour):
        self.surface.set_at((x, y), colour)

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
        pygame.display.update()
        self. last_update = time.time()

    # Process pygame events
    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
