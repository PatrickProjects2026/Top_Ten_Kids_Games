import pygame
import sys

# --- CONFIGURATION ---
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brick City 101")
clock = pygame.time.Clock()

# Colors (Matching your Hub's Palette)
DARK_BG = (15, 15, 25)
ACCENT = (0, 255, 200)
WHITE = (240, 240, 240)
RED = (255, 80, 80)
GRAY = (50, 50, 70)

# Fonts
font_score = pygame.font.SysFont("Arial", 24, bold=True)
font_msg = pygame.font.SysFont("Arial", 48, bold=True)

# Game Constants
PADDLE_WIDTH = 120
PADDLE_HEIGHT = 15
BALL_RADIUS = 8
BRICK_ROWS = 6
BRICK_COLS = 10
BRICK_WIDTH = 70
BRICK_HEIGHT = 25
BRICK_PADDING = 5
OFFSET_TOP = 60
OFFSET_LEFT = 35

# Game State
paddle = pygame.Rect(WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - 50, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Vector2(WIDTH // 2, HEIGHT // 2)
ball_speed = pygame.Vector2(4, -4)
score = 0
game_active = True
message = ""

# Build Bricks
bricks = []
for row in range(BRICK_ROWS):
    for col in range(BRICK_COLS):
        bx = col * (BRICK_WIDTH + BRICK_PADDING) + OFFSET_LEFT
        by = row * (BRICK_HEIGHT + BRICK_PADDING) + OFFSET_TOP
        bricks.append(pygame.Rect(bx, by, BRICK_WIDTH, BRICK_HEIGHT))

def reset_game():
    global score, game_active, message, bricks
    score = 0
    game_active = True
    message = ""
    ball.xy = (WIDTH // 2, HEIGHT // 2)
    ball_speed.xy = (4, -4)
    bricks = []
    for row in range(BRICK_ROWS):
        for col in range(BRICK_COLS):
            bx = col * (BRICK_WIDTH + BRICK_PADDING) + OFFSET_LEFT
            by = row * (BRICK_HEIGHT + BRICK_PADDING) + OFFSET_TOP
            bricks.append(pygame.Rect(bx, by, BRICK_WIDTH, BRICK_HEIGHT))

# --- MAIN LOOP ---
while True:
    screen.fill(DARK_BG)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r: reset_game()

    if game_active:
        # Paddle Movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle.left > 0:
            paddle.x -= 7
        if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
            paddle.x += 7

        # Ball Movement
        ball += ball_speed

        # Wall Collisions
        if ball.x - BALL_RADIUS <= 0 or ball.x + BALL_RADIUS >= WIDTH:
            ball_speed.x *= -1
        if ball.y - BALL_RADIUS <= 0:
            ball_speed.y *= -1
        
        # Paddle Collision
        if paddle.collidepoint(ball.x, ball.y + BALL_RADIUS):
            ball_speed.y *= -1
            # Add slight randomness to bounce based on where it hits the paddle
            ball_speed.x += (ball.x - paddle.centerx) / 10

        # Brick Collisions
        for brick in bricks[:]:
            if brick.collidepoint(ball.x, ball.y):
                bricks.remove(brick)
                ball_speed.y *= -1
                score += 10
                break

        # Lose Condition
        if ball.y > HEIGHT:
            game_active = False
            message = "CITY CRUMBLED! PRESS 'R'"

        # Win Condition
        if not bricks:
            game_active = False
            message = "CITY SECURED! PRESS 'R'"

    # --- DRAWING ---
    # Draw Bricks
    for brick in bricks:
        pygame.draw.rect(screen, ACCENT, brick, border_radius=3)
        pygame.draw.rect(screen, GRAY, brick, 1, border_radius=3)

    # Draw Paddle & Ball
    pygame.draw.rect(screen, WHITE, paddle, border_radius=5)
    pygame.draw.circle(screen, RED, (int(ball.x), int(ball.y)), BALL_RADIUS)

    # UI
    score_text = font_score.render(f"SCORE: {score}", True, WHITE)
    screen.blit(score_text, (20, 20))

    if not game_active:
        msg_surf = font_msg.render(message, True, RED if "CRUMBLED" in message else ACCENT)
        msg_rect = msg_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
        screen.blit(msg_surf, msg_rect)

    pygame.display.flip()
    clock.tick(60)