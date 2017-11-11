from renderer import Renderer

WIDTH = 800
HEIGHT = 600
WINDOW_TITLE = "Software Renderer"

if __name__ == "__main__":
    renderer = Renderer(WIDTH, HEIGHT, WINDOW_TITLE)

    while True:
        renderer.clear()
        renderer.process_events()