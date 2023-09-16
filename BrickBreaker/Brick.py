import pygame.draw


def interpolate(color_a, color_b, t):
    # color_a and color_b are RGB tuples
    # 't' is a value between 0.0 and 1.0
    # this is a native interpolation
    return tuple(int(a + (b - a) * t) for a, b in zip(color_a, color_b))


class Brick:
    def __init__(self, x, y, width, height, colors, health):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.max_health = health
        self.health = self.max_health

        self.colors = colors
        self.color = colors[0]

    def draw(self, win):
        pygame.draw.rect(win,
                         color=self.color,
                         rect=(self.x, self.y, self.width, self.height))

    def collide(self, ball) -> bool:
        collision = False
        if (self.x <= ball.x <= self.x + self.width
                and ball.y - ball.radius <= self.y + self.height):
            collision = True
            self.hit()
            ball.set_vel(ball.x_vel, ball.y_vel * -1)

        return collision

    def hit(self, damage=1):
        self.health -= damage
        self.color = interpolate(*self.colors, self.health/self.max_health)
