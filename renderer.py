import sys
import time
import pygame

class Renderer:
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

    # Render FPS counter
    def render_fps(self):
        text_surface = self.font.render(("%d FPS" % (1 / self.get_delta())), True, (0, 0, 0))
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
