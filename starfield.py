import random

X = 0
Y = 1
Z = 2


class StarField:
    """
    Renders a 3D starfield effect
    """
    def __init__(self, num_stars, spread, speed):
        self.spread = spread
        self.speed = speed

        self.stars = [[0, 0, 0] for x in xrange(num_stars)]

        for i in xrange(num_stars):
            self.init_star(i)

    # Initialise a star to a new random position
    def init_star(self, index):
        self.stars[index] = [
            2 * (random.random() - 0.5) * self.spread,
            2 * (random.random() - 0.5) * self.spread,
            (random.random() + 0.00001) * self.spread
        ]

    # Render
    def render(self, renderer):
        # Clear screen to black
        renderer.clear((0, 0, 0))

        half_width = renderer.width/2
        half_height = renderer.height/2

        for i in xrange(self.stars.__len__()):
            self.stars[i][Z] -= renderer.get_delta() * self.speed

            if self.stars[i][Z] <= 0:
                self.init_star(i)

            x = int((self.stars[i][X]/self.stars[i][Z]) * half_width + half_width)
            y = int((self.stars[i][Y]/self.stars[i][Z]) * half_height + half_height)

            if (x <= 0) or (x >= renderer.width) or (y <= 0) or (y >= renderer.height):
                self.init_star(i)
            else:
                renderer.draw_pixel(x, y, (255, 255, 255))
