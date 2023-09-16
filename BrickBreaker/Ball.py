import pygame.draw


class Ball:
    VELOCITY = 10

    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

        self.x_vel = 0
        self.y_vel = -self.VELOCITY / 2

    def draw(self, win):
        pygame.draw.circle(win,
                           color=self.color,
                           center=(self.x, self.y),
                           radius=self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def set_vel(self, x_vel, y_vel):
        self.x_vel = x_vel
        self.y_vel = y_vel
