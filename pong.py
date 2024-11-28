import pygame

pygame.init()

WIDTH, HEIGHT = 700, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_RADIUS = 7

SCORE_FONT = pygame.font.SysFont("comicsans", 50)
WINNING_SCORE = 10


class Paddle:
    COLOR = WHITE
    VEL = 6 

    def __init__(self, x, y, width, height):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height

    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))

    def move(self, up=True):
        self.y += -self.VEL if up else self.VEL

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y


class Ball:
    MAX_VEL = 5
    COLOR = WHITE

    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0

    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel *= -1


def draw(win, paddles, ball, left_score, right_score):
    win.fill(BLACK)

    # Draw scores
    left_score_text = SCORE_FONT.render(f"{left_score}", 1, WHITE)
    right_score_text = SCORE_FONT.render(f"{right_score}", 1, WHITE)
    win.blit(left_score_text, (WIDTH // 4 - left_score_text.get_width() // 2, 20))
    win.blit(right_score_text, (WIDTH * 3 // 4 - right_score_text.get_width() // 2, 20))

    # Draw middle line
    for i in range(0, HEIGHT, 20):
        if i % 40 == 0:
            pygame.draw.rect(win, WHITE, (WIDTH // 2 - 5, i, 10, 20))

    # Draw paddles and ball
    for paddle in paddles:
        paddle.draw(win)
    ball.draw(win)

    pygame.display.update()


def handle_collision(ball, left_paddle, right_paddle):
    # Ball collision with top and bottom walls
    if ball.y - ball.radius <= 0 or ball.y + ball.radius >= HEIGHT:
        ball.y_vel *= -1

    # Ball collision with left paddle
    if ball.x_vel < 0 and left_paddle.y <= ball.y <= left_paddle.y + left_paddle.height:
        if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
            ball.x_vel *= -1
            adjust_ball_velocity(ball, left_paddle)

    # Ball collision with right paddle
    if ball.x_vel > 0 and right_paddle.y <= ball.y <= right_paddle.y + right_paddle.height:
        if ball.x + ball.radius >= right_paddle.x:
            ball.x_vel *= -1
            adjust_ball_velocity(ball, right_paddle)


def adjust_ball_velocity(ball, paddle):
    # Adjust ball velocity based on paddle position
    middle_y = paddle.y + paddle.height / 2
    difference_in_y = middle_y - ball.y
    reduction_factor = (paddle.height / 2) / ball.MAX_VEL
    ball.y_vel = -difference_in_y / reduction_factor


def handle_paddle_movement(keys, left_paddle, right_paddle):
    if keys[pygame.K_w] and left_paddle.y > 0:
        left_paddle.move(up=True)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.height < HEIGHT:
        left_paddle.move(up=False)

    if keys[pygame.K_UP] and right_paddle.y > 0:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.height < HEIGHT:
        right_paddle.move(up=False)


def main():
    clock = pygame.time.Clock()
    run = True

    left_paddle = Paddle(10, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)

    left_score = 0
    right_score = 0

    while run:
        clock.tick(FPS)
        draw(WIN, [left_paddle, right_paddle], ball, left_score, right_score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, left_paddle, right_paddle)

        ball.move()
        handle_collision(ball, left_paddle, right_paddle)

        # Score update
        if ball.x < 0:
            right_score += 1
            ball.reset()
        elif ball.x > WIDTH:
            left_score += 1
            ball.reset()

        # Check for winner
        if left_score >= WINNING_SCORE or right_score >= WINNING_SCORE:
            winner = "Left Player" if left_score >= WINNING_SCORE else "Right Player"
            win_text = SCORE_FONT.render(f"{winner} Wins!", 1, WHITE)
            WIN.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 - win_text.get_height() // 2))
            pygame.display.update()
            pygame.time.delay(3000)
            left_score, right_score = 0, 0
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()

    pygame.quit()


if __name__ == "__main__":
    main()
