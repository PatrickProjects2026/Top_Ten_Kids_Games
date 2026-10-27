import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 400, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 149, 221)
FPS = 60

# Game Variables
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python Simple Pinball")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

# Ball properties
ball_pos = [200, 100]
ball_speed = [4, 4]
ball_radius = 10
speed_increment = 0.3

# Paddle properties
paddle_w, paddle_h = 80, 15
left_paddle_x = 50
right_paddle_x = 270
paddle_y = 550
paddle_speed = 7

score = 0

def draw_text(text, x, y):
    img = font.render(text, True, WHITE)
    screen.blit(img, (x, y))

# Main Game Loop
while True:
    screen.fill(BLACK)
    
    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Keyboard Input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and left_paddle_x > 0:
        left_paddle_x -= paddle_speed
    if keys[pygame.K_RIGHT] and right_paddle_x < WIDTH - paddle_w:
        right_paddle_x += paddle_speed

    # Move Ball
    ball_pos[0] += ball_speed[0]
    ball_pos[1] += ball_speed[1]

    # Wall Collisions (Left, Right, Top)
    if ball_pos[0] - ball_radius <= 0 or ball_pos[0] + ball_radius >= WIDTH:
        ball_speed[0] *= -1
    if ball_pos[1] - ball_radius <= 0:
        ball_speed[1] *= -1

    # Paddle Collision Logic
    ball_rect = pygame.Rect(ball_pos[0] - ball_radius, ball_pos[1] - ball_radius, ball_radius*2, ball_radius*2)
    left_rect = pygame.Rect(left_paddle_x, paddle_y, paddle_w, paddle_h)
    right_rect = pygame.Rect(right_paddle_x, paddle_y, paddle_w, paddle_h)

    if ball_rect.colliderect(left_rect) or ball_rect.colliderect(right_rect):
        if ball_speed[1] > 0:  # Only bounce if falling down
            ball_speed[1] *= -1
            score += 1
            # Increase Speed
            ball_speed[0] += speed_increment if ball_speed[0] > 0 else -speed_increment
            ball_speed[1] -= speed_increment

    # Game Over
    if ball_pos[1] > HEIGHT:
        print(f"Game Over! Final Score: {score}")
        pygame.quit()
        sys.exit()

    # Drawing
    pygame.draw.circle(screen, GREEN, (int(ball_pos[0]), int(ball_pos[1])), ball_radius)
    pygame.draw.rect(screen, BLUE, left_rect)
    pygame.draw.rect(screen, BLUE, right_rect)
    draw_text(f"Score: {score}", 10, 10)

    pygame.display.flip()
    clock.tick(FPS)