####################################################################################################################
# IMPORTS
import pygame.draw


####################################################################################################################
# CORE
class Paddle:
    # ---> CONSTANTS
    PPF = 10
    COL_BLACK = "#000000"
    FONT_DIR = "res/font/"

    DIR_RIGHT = 1
    DIR_LEFT = -1

    # ---> CONSTRUCTOR
    def __init__(self, x, y, width, height, color, name):
        self.def_paddle_xy = (x, y)
        self._pad_x = x
        self._pad_y = y
        self._pad_width = width
        self._pad_height = height
        self._pad_color = color

        self._pad_name = name

        font_name = self.FONT_DIR + "Orbitron-Regular.ttf"
        self.font = pygame.font.Font(font_name, 16)
        # self.font.set_bold(True)
        self.font.set_italic(True)

        self._border = self._pad_height / self._pad_width

    # ---> FUNCTIONS
    def draw(self, surface):
        shadow_rect = (self._pad_x, self._pad_y, self._pad_width, self._pad_height)
        pygame.draw.rect(surface,
                         self.COL_BLACK,
                         rect=shadow_rect,
                         border_radius=10)

        rect = (self._pad_x + self._border * 10, self._pad_y + self._border * 10,
                self._pad_width - self._border * 15, self._pad_height - self._border * 10)
        pygame.draw.rect(surface,
                         self._pad_color,
                         rect=rect,
                         border_radius=10)

        lives_text = self.font.render(f"{self._pad_name}", True, "black")
        text_x = self._pad_x + self._pad_width / 2 - lives_text.get_width() / 2
        text_y = self._pad_y + self._pad_height / 2 - lives_text.get_height() / 2
        surface.blit(lives_text, (text_x, text_y))

    def get_surface(self):
        return [self._pad_x, self._pad_y, self._pad_width, self._pad_height]

    def check_collision(self, battlefield, direction):
        collision = False

        surf = battlefield.get_surface()
        bf_x, bf_width = surf[0], surf[2]

        gap = self.PPF * direction

        match direction:
            case self.DIR_RIGHT:
                if self._pad_x + self._pad_width > bf_x + bf_width - gap:
                    collision = True

            case self.DIR_LEFT:
                if self._pad_x + gap < bf_x:
                    collision = True

        return collision

    def move(self, x_dir):
        self._pad_x += self.PPF * x_dir

    def reset_position(self):
        self._pad_x = self.def_paddle_xy[0]
        self._pad_y = self.def_paddle_xy[1]
