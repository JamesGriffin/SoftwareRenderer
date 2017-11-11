import sys
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

    # Clear screen and fill with color (default is grey)
    def clear(self, colour=(128, 128, 128)):
        self.surface.fill(colour)
        self.update()

    # Update display
    def update(self):
        pygame.display.update()

    # Process pygame events
    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
