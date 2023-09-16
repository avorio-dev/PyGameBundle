import math
import pygame

from BrickBreaker.Ball import Ball
from BrickBreaker.Brick import Brick
from BrickBreaker.Paddle import Paddle

pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 15
BALL_RADIUS = 10
MAX_LIVES = 3
LIVES_FONT = pygame.font.SysFont("consolas", 25)

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brick Breaker")


def draw(surface, paddle, ball, bricks, lives):
    surface.fill("white")

    paddle.draw(surface)
    ball.draw(surface)
    for brick in bricks:
        brick.draw(win)

    lives_text = LIVES_FONT.render(f"Lives: {lives}", 1, "black")
    win.blit(lives_text, (10, HEIGHT - lives_text.get_height() - 10))

    pygame.display.update()


def ball_window_collision(ball):
    if (ball.x - ball.radius <= 0
            or ball.x + ball.radius >= WIDTH):
        ball.set_vel(ball.x_vel * -1, ball.y_vel)

    if (ball.y - ball.radius <= 0
            or ball.y + ball.radius >= HEIGHT):
        ball.set_vel(ball.x_vel, ball.y_vel * -1)


def ball_paddle_collision(ball, paddle):
    # Ball X between paddle start and paddle end
    # Ball Y reach paddle
    if (paddle.x <= ball.x <= paddle.x + paddle.width
            and ball.y + ball.radius >= paddle.y):
        # It works, but direction will not change based on hit angle
        # ball.set_vel(ball.x_vel, ball.y_vel * -1)

        paddle_center = paddle.x + paddle.width / 2
        distance_to_center = ball.x - paddle_center

        percent_width = distance_to_center / paddle.width
        angle = percent_width * 90
        angle_radians = math.radians(angle)

        x_vel = math.sin(angle_radians) * ball.VELOCITY
        y_vel = math.cos(angle_radians) * ball.VELOCITY * -1

        ball.set_vel(x_vel, y_vel)


def ball_paddle_overcome(ball, paddle, lives):
    if ball.y > paddle.y:
        lives -= 1

        ball.x = paddle.x + PADDLE_WIDTH / 2
        ball.y = paddle.y - BALL_RADIUS
        ball.set_vel(0, -ball.VELOCITY)

    return lives


def generate_bricks(rows, cols):
    gap = 2
    brick_width = (WIDTH // cols) - gap
    brick_height = 20
    brick_health = 2

    bricks = []
    for row in range(rows):
        for col in range(cols):
            brick = Brick(col * brick_width + gap * col,
                          row * brick_height + gap * row,
                          brick_width,
                          brick_height,
                          [(0, 255, 0), (255, 0, 0)],
                          brick_health)
            bricks.append(brick)

    return bricks


def main():
    clock = pygame.time.Clock()

    paddle_x = WIDTH / 2 - PADDLE_WIDTH / 2
    paddle_y = HEIGHT - PADDLE_HEIGHT - 40

    paddle = Paddle(paddle_x, paddle_y,
                    PADDLE_WIDTH, PADDLE_HEIGHT, "black")

    ball = Ball(paddle_x + PADDLE_WIDTH / 2,
                paddle_y - BALL_RADIUS,
                BALL_RADIUS,
                "black")

    bricks = generate_bricks(2, 8)

    lives = MAX_LIVES

    run = True
    while run:
        clock.tick(FPS)

        # Check QUIT Event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        # Check pressed keys
        keys = pygame.key.get_pressed()

        if (keys[pygame.K_RIGHT]
                and paddle.x + paddle.width + paddle.VELOCITY < WIDTH):
            paddle.move(paddle.DIR_RIGHT)

        if (keys[pygame.K_LEFT]
                and paddle.x - paddle.VELOCITY > 0):
            paddle.move(paddle.DIR_LEFT)

        if len(bricks) == 0:
            win_text = LIVES_FONT.render("You WIN!", 1, "green")
            win.blit(win_text, (WIDTH / 2 - win_text.get_width() / 2, HEIGHT / 2 - win_text.get_height() / 2))
            pygame.display.update()
            pygame.time.delay(3000)
            run = False

        # Ball movements and collision
        ball.move()
        ball_window_collision(ball)
        ball_paddle_collision(ball, paddle)

        for brick in bricks[:]:
            if brick.collide(ball):
                if brick.health <= 0:
                    bricks.remove(brick)
                else:
                    pass

        lives = ball_paddle_overcome(ball, paddle, lives)
        if lives <= 0:
            lost_text = LIVES_FONT.render("You lost!", 1, "red")
            win.blit(lost_text, (WIDTH / 2 - lost_text.get_width() / 2, HEIGHT / 2 - lost_text.get_height() / 2))
            pygame.display.update()
            pygame.time.delay(3000)
            run = False

        draw(win, paddle, ball, bricks, lives)

    pygame.quit()
    quit()


if __name__ == "__main__":
    main()

    # Definizione Parametri di Finestra Pygame
    # Definizione Main Loop con cattura evento Quit
    # Definizione degli FPS
    # Definizione metodo Draw per sfondo pymae da chiamare all'interno del loop principale
    # Creazione game object con relativo metodo draw
    # Cattura tasti premuti
    # Definizione metodo per movimento
    # Aggiunta nelle condizioni per verificare che l'oggetto non esca dai bordi
    # Aggiunta condizioni di collisione tra ball e paddle
