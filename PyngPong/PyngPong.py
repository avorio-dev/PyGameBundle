####################################################################################################################
# IMPORTS
import random

import pyautogui
import pygame
import win32api
import win32gui

from win32api import GetSystemMetrics

from models.Battlefield import Battlefield
from models.Paddle import Paddle
from models.Ball import Ball


####################################################################################################################
# CORE
class PyngPong:
    # ---> CONSTANTS
    FPS = 120
    TITLE = "Pyng Pong!"
    FONT_DIR = "res/font/"

    BG_COLOR = "#00ff00"

    MAX_LIVES = 3

    # ---> CONSTRUCTOR
    def __init__(self, player_up, player_down):
        # Init Pygame Module
        pygame.init()
        self.window = None

        # Set Frame Rate
        self.clock = pygame.time.Clock()
        self.clock.tick(self.FPS)
        self.clock.tick(self.FPS)

        # Set Screen Size
        self.scr_width = int(GetSystemMetrics(0))
        self.scr_height = int(GetSystemMetrics(1))

        # Set Pygame
        pygame.display.set_caption(self.TITLE)
        self.window = pygame.display.set_mode((self.scr_width, self.scr_height))
        self.buffer = pygame.Surface((self.scr_width, self.scr_height))

        # Set Font
        font_name = self.FONT_DIR + "Orbitron-Regular.ttf"
        self.font = pygame.font.Font(font_name, 30)

        # Set Attributes
        self.game_running, self.on_pause = False, False
        self.draw_winner, self.draw_with_delay = False, False

        self.lives_player_up = self.MAX_LIVES
        self.lives_player_down = self.MAX_LIVES
        self.winner, self.loser = "", ""

        self.player_up = player_up
        self.player_down = player_down

    # ---> FUNCTIONS
    def _check_quit_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_running = False
                break

    def _init_objects(self):
        # ---> Battlefield
        bf_col = "#002db3"
        gap = 5

        # Battlefield (X, Y) Top Left Corner, Width, Height
        bf_x = self.scr_width // 4
        bf_y = gap
        bf_width = self.scr_width // 2
        bf_height = self.scr_height - gap * 2

        battlefield = Battlefield(bf_x,
                                  bf_y,
                                  bf_width,
                                  bf_height,
                                  bf_col)

        # ---> Players Paddle
        paddle_color = "#ffcc00"
        paddle_width = 125
        paddle_height = 20
        gap = 20
        rounding_error = 10

        paddle_up = Paddle(bf_x * 2 - paddle_width / 2,
                           bf_y + gap + rounding_error,
                           paddle_width, paddle_height, paddle_color, self.player_up)

        paddle_down = Paddle(bf_x * 2 - paddle_width / 2,
                             bf_height - gap * 2,
                             paddle_width, paddle_height, paddle_color, self.player_down)

        # ---> Ball
        ball_radius = 15
        ball_color = "#ff5500"
        ball = Ball(bf_x * 2,
                    bf_height / 2,
                    ball_radius,
                    ball_color)

        return [battlefield, paddle_up, paddle_down, ball]

    def _draw_objects(self, battlefield, paddle_up, paddle_down, ball):
        gap = 25
        self.buffer.fill(self.BG_COLOR)

        battlefield.draw(self.buffer)

        if not self.draw_winner:
            paddle_up.draw(self.buffer)
            paddle_down.draw(self.buffer)
            ball.draw(self.buffer)

            # Upper Player Lives
            lives_text = self.font.render(f"Lives: {self.lives_player_up}", True, "white")
            text_x = gap
            text_y = lives_text.get_height() + lives_text.get_height() / 2

            rect_x = text_x - gap / 2
            rect_y = text_y - gap / 2
            rect_width = lives_text.get_width() + gap
            rect_height = lives_text.get_height() + gap

            rounded_rect = pygame.Rect(rect_x, rect_y, rect_width, rect_height)
            pygame.draw.rect(self.buffer, "black", rounded_rect, border_radius=10)
            self.buffer.blit(lives_text, (text_x, text_y))

            # Down Player Lives
            lives_text = self.font.render(f"Lives: {self.lives_player_down}", True, "white")
            text_x = gap
            text_y = self.scr_height - lives_text.get_height() - gap * 2

            rect_x = text_x - gap / 2
            rect_y = text_y - gap / 2
            rect_width = lives_text.get_width() + gap
            rect_height = lives_text.get_height() + gap

            rounded_rect = pygame.Rect(rect_x, rect_y, rect_width, rect_height)
            pygame.draw.rect(self.buffer, "black", rounded_rect, border_radius=10)
            self.buffer.blit(lives_text, (text_x, text_y))

            # Game Pause Texts
            if self.on_pause:
                # Move Player UP
                move_up_text = self.font.render(f"Move with  <a>  and  <d>", True, "white")
                text_x = self.scr_width / 2 - move_up_text.get_width() / 2
                text_y = self.scr_height / 8 - move_up_text.get_height() / 2

                rect_x = text_x - gap / 2
                rect_y = text_y - gap / 2
                rect_width = move_up_text.get_width() + gap
                rect_height = move_up_text.get_height() + gap

                rounded_rect = pygame.Rect(rect_x, rect_y, rect_width, rect_height)
                pygame.draw.rect(self.buffer, "black", rounded_rect, border_radius=10)
                self.buffer.blit(move_up_text, (text_x, text_y))

                # Move Player DOWN
                move_down_text = self.font.render(f"Move with  <left>  and  <right>", True, "white")
                text_x = self.scr_width / 2 - move_down_text.get_width() / 2
                text_y = self.scr_height - self.scr_height / 8 - move_down_text.get_height() / 2

                rect_x = text_x - gap / 2
                rect_y = text_y - gap / 2
                rect_width = move_down_text.get_width() + gap
                rect_height = move_down_text.get_height() + gap

                rounded_rect = pygame.Rect(rect_x, rect_y, rect_width, rect_height)
                pygame.draw.rect(self.buffer, "black", rounded_rect, border_radius=10)
                self.buffer.blit(move_down_text, (text_x, text_y))

                # Play Pause
                play_pause_text = self.font.render(f"Press SPACE to Play/Pause", True, "white")
                text_x = self.scr_width / 2 - play_pause_text.get_width() / 2
                text_y = self.scr_height / 2 - play_pause_text.get_height() / 2

                rect_x = text_x - gap / 2
                rect_y = text_y - gap / 2
                rect_width = play_pause_text.get_width() + gap
                rect_height = play_pause_text.get_height() + gap

                rounded_rect = pygame.Rect(rect_x, rect_y, rect_width, rect_height)
                pygame.draw.rect(self.buffer, "black", rounded_rect, border_radius=10)
                self.buffer.blit(play_pause_text, (text_x, text_y))

            # Print Buffer
            self.window.blit(self.buffer, (0, 0))
            pygame.display.update()
            if self.draw_with_delay:
                pygame.time.wait(500)
                self.draw_with_delay = False

        else:
            winner_height = 0
            loser_height = 0

            if self.winner == self.player_up:
                winner_height = self.scr_height / 4
                loser_height = self.scr_height / 2 + self.scr_height / 4

            elif self.winner == self.player_down:
                winner_height = self.scr_height / 2 + self.scr_height / 4
                loser_height = self.scr_height / 4

            # Winner Text
            gap = 25
            winner_text = self.font.render(f"{self.winner}, You WIN!", True, "green")
            text_x = self.scr_width / 2 - winner_text.get_width() / 2
            text_y = winner_height

            rect_x = text_x - gap / 2
            rect_y = text_y - gap / 2
            rect_width = winner_text.get_width() + gap
            rect_height = winner_text.get_height() + gap

            rounded_rect = pygame.Rect(rect_x, rect_y, rect_width, rect_height)
            pygame.draw.rect(self.buffer, "black", rounded_rect, border_radius=10)
            self.buffer.blit(winner_text, (text_x, text_y))

            # Looser Text
            loser_text = self.font.render(f"{self.loser}, You LOSE!", True, "red")
            text_x = self.scr_width / 2 - loser_text.get_width() / 2
            text_y = loser_height

            rect_x = text_x - gap / 2
            rect_y = text_y - gap / 2
            rect_width = loser_text.get_width() + gap
            rect_height = loser_text.get_height() + gap

            rounded_rect = pygame.Rect(rect_x, rect_y, rect_width, rect_height)
            pygame.draw.rect(self.buffer, "black", rounded_rect, border_radius=10)
            self.buffer.blit(loser_text, (text_x, text_y))

            # Reset Flags
            self.draw_winner = False
            self.winner = ""
            self.loser = ""

            # Print Buffer
            self.window.blit(self.buffer, (0, 0))
            pygame.display.update()
            pygame.time.wait(3000)

    def _check_winner(self):
        self.winner = ""
        self.loser = ""
        self.draw_winner = False
        if self.lives_player_down == 0:
            self.winner = self.player_up
            self.loser = self.player_down
            self.draw_winner = True

        if self.lives_player_up == 0:
            self.winner = self.player_down
            self.loser = self.player_up
            self.draw_winner = True

    def _reset_objects(self, paddle_up, paddle_down, ball):
        ball.reset_position()
        ball.set_velocity(0, random.choice([-1, 1]) * ball.PPF)
        # ball.set_velocity(0, -ball.PPF)

        paddle_up.reset_position()
        paddle_down.reset_position()

        if self.lives_player_up == 0 or self.lives_player_down == 0:
            self.lives_player_up = self.MAX_LIVES
            self.lives_player_down = self.MAX_LIVES

    def play(self):
        objects = self._init_objects()

        battlefield = objects[0]
        paddle_up = objects[1]
        paddle_down = objects[2]
        ball = objects[3]

        ball.set_velocity(0, random.choice([-1, 1]) * ball.PPF)
        # ball.set_velocity(0, -ball.PPF)

        self._draw_objects(battlefield, paddle_up, paddle_down, ball)
        self.on_pause = True

        self.game_running = True

        while self.game_running:
            self._check_quit_event()

            keys = pygame.key.get_pressed()

            # ---> Game Options
            if keys[pygame.K_ESCAPE]:
                self.game_running = False

            if keys[pygame.K_p]:
                self._reset_objects(paddle_up, paddle_down, ball)

            if keys[pygame.K_SPACE]:
                if self.on_pause:
                    self.on_pause = False
                    self.draw_with_delay = True
                    self._draw_objects(battlefield, paddle_up, paddle_down, ball)
                    self.clock.tick(self.FPS)
                    continue
                else:
                    self.on_pause = True
                    pygame.time.wait(200)

            # ---> Paddle Movement and collision
            if not self.on_pause:
                # Player Down commands
                if keys[pygame.K_RIGHT]:
                    if not paddle_down.check_collision(battlefield, Paddle.DIR_RIGHT):
                        paddle_down.move(Paddle.DIR_RIGHT)

                if keys[pygame.K_LEFT]:
                    if not paddle_down.check_collision(battlefield, Paddle.DIR_LEFT):
                        paddle_down.move(Paddle.DIR_LEFT)

                if keys[pygame.K_RCTRL]:
                    # TODO rctrl
                    pass

                # Player Up commands
                if keys[pygame.K_d]:
                    if not paddle_up.check_collision(battlefield, Paddle.DIR_RIGHT):
                        paddle_up.move(Paddle.DIR_RIGHT)

                if keys[pygame.K_a]:
                    if not paddle_up.check_collision(battlefield, Paddle.DIR_LEFT):
                        paddle_up.move(Paddle.DIR_LEFT)

                if keys[pygame.K_LCTRL]:
                    # TODO lctrl
                    pass

                # ---> Ball movement and collisions
                ball.move()

                # ---> Check Collisions with Battlefield Sides and Paddles
                collision = ball.check_collisions(battlefield, paddle_up, paddle_down)

                if not collision:
                    # ---> Check boundary Crossed
                    boundary_crossed = False
                    if ball.check_boundary_cross(paddle_up=paddle_up):
                        self.lives_player_up -= 1
                        boundary_crossed = True

                    if ball.check_boundary_cross(paddle_down=paddle_down):
                        self.lives_player_down -= 1
                        boundary_crossed = True

                    if boundary_crossed:
                        self._check_winner()
                        self._reset_objects(paddle_up, paddle_down, ball)
                        if not self.draw_winner:
                            pygame.time.wait(500)

            # ---> Update game surface
            self._draw_objects(battlefield, paddle_up, paddle_down, ball)
            self.clock.tick(self.FPS)

        pygame.quit()
        quit()


####################################################################################################################
# RUN
if __name__ == "__main__":
    # Definizione Parametri di Finestra Pygame
    # Definizione Main Loop con cattura evento Quit
    # Definizione degli FPS
    # Creazione di un buffer su cui verrà diegnata tutta la superfice di gioco
    # Definizione metodo Draw per sfondo pygame da chiamare all'interno del loop principale
    # Creazione game object con relativo metodo draw
    # Disegno da buffer degli oggetti
    # Cattura tasti premuti
    # Definizione metodo per movimento
    # Aggiunta nelle condizioni per verificare che l'oggetto non esca dai bordi
    # Aggiunta condizioni di collisione tra ball e paddle
    # Aggiunta testi

    # python -m PyInstaller --name PyngPong PyngPong.py
    # python -m PyInstaller PyngPong.spec

    # player_1, player_2 = "", ""
    player_1 = input("Player 1 Name: ").strip()
    player_2 = input("Player 2 Name: ").strip()

    if player_1 == "":
        player_1 = "Player 1"

    if player_2 == "":
        player_2 = "Player 2"

    pyng_pong = PyngPong(player_1, player_2)
    hwnd = win32gui.FindWindow(None, PyngPong.TITLE)
    if hwnd:
        pyautogui.press("alt")
        win32gui.SetForegroundWindow(hwnd)
        win32gui.SetFocus(hwnd)
        win32api.SetCursorPos((pyng_pong.scr_width, 0))

    pyng_pong.play()
