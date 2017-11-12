from renderer import Renderer
from starfield import StarField

WIDTH = 800
HEIGHT = 600
WINDOW_TITLE = "3D Starfield"
MAX_FRAMERATE = 0

if __name__ == "__main__":

    # Create new renderer
    renderer = Renderer(WIDTH, HEIGHT, WINDOW_TITLE)

    # Create new starfield
    starfield = StarField(4096, 128.0, 40.0)

    # Render Loop
    while True:
        if MAX_FRAMERATE == 0 or renderer.get_delta() >= (1.0/MAX_FRAMERATE):
            renderer.process_events()
            starfield.render(renderer)
            renderer.draw_fps_counter()
            renderer.update()
