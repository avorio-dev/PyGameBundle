import pygame.draw


class Paddle:
    VELOCITY = 5
    DIR_RIGHT = 1
    DIR_LEFT = -1

    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def draw(self, win):
        pygame.draw.rect(win,
                         color=self.color,
                         rect=(self.x, self.y, self.width, self.height))

    def move(self, direction=DIR_RIGHT):
        self.x = self.x + self.VELOCITY * direction
