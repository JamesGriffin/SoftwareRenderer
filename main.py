from renderer import Renderer

WIDTH = 800
HEIGHT = 600
WINDOW_TITLE = "Software Renderer"
MAX_FRAMERATE = 60

if __name__ == "__main__":
    renderer = Renderer(WIDTH, HEIGHT, WINDOW_TITLE)

    while True:
        if renderer.get_delta() >= (1.0/MAX_FRAMERATE):
            renderer.process_events()
            renderer.clear()
            renderer.render_fps()
            renderer.update()
