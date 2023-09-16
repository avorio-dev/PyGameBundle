####################################################################################################################
# IMPORTS
import pygame.draw


####################################################################################################################
# CORE
class Battlefield:
    # ---> CONSTANTS
    COL_WHITE = "#ffffff"
    COL_BLACK = "#000000"

    # ---> CONSTRUCTOR
    def __init__(self, x, y, width, height, color):
        self._bf_x = x
        self._bf_y = y
        self._bf_width = width
        self._bf_height = height
        self._bf_color = color

        self._border = self._bf_height / self._bf_width

    # ---> FUNCTIONS
    def draw(self, surface):
        gap = 5

        rect = (self._bf_x, self._bf_y, self._bf_width, self._bf_height)
        pygame.draw.rect(surface,
                         self.COL_BLACK,
                         rect=rect,
                         border_radius=10)

        rect = (self._bf_x + self._border, self._bf_y + self._border,
                self._bf_width - self._border * 2, self._bf_height - self._border * 2)
        pygame.draw.rect(surface,
                         self._bf_color,
                         rect=rect,
                         border_radius=10)

        vertical_line_start = (self._bf_x * 2, self._bf_y + gap)
        vertical_line_end = (self._bf_x * 2, self._bf_height)
        pygame.draw.line(surface,
                         self.COL_WHITE,
                         start_pos=(vertical_line_start[0], vertical_line_start[1]),
                         end_pos=(vertical_line_end[0], vertical_line_end[1]),
                         width=5)

        horiz_line_start = (self._bf_x + gap, self._bf_height / 2)
        horiz_line_end = (self._bf_x + self._bf_width - gap, self._bf_height / 2)
        pygame.draw.line(surface,
                         self.COL_WHITE,
                         start_pos=(horiz_line_start[0], horiz_line_start[1]),
                         end_pos=(horiz_line_end[0], horiz_line_end[1]),
                         width=1)

        center_circle = ((self._bf_width, self._bf_height / 2), self._bf_height / 8)
        pygame.draw.circle(surface,
                           self.COL_WHITE,
                           center=center_circle[0],
                           radius=center_circle[1],
                           width=3)

    def get_surface(self):
        return [self._bf_x, self._bf_y, self._bf_width, self._bf_height]
