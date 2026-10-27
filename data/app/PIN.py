import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 500, 600 # Slightly wider screen
WHITE, BLACK = (255, 255, 255), (10, 10, 15)
NEON_GREEN, NEON_BLUE = (57, 255, 20), (0, 255, 255)
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Courier New", 32, bold=True)

# Ball Setup
ball_pos = [WIDTH // 2, 100]
ball_speed = [4.0, 4.0]
ball_radius = 12
gravity = 0.12 # Stronger gravity for faster gameplay

# Paddle Setup (Covering most of the space)
# We leave a 60px gap in the middle
paddle_w = (WIDTH // 2) - 40 
paddle_h = 20
base_y = 550
kick_y = 510 # How high it jumps when "pushed"

left_rect = pygame.Rect(10, base_y, paddle_w, paddle_h)
right_rect = pygame.Rect(WIDTH - paddle_w - 10, base_y, paddle_w, paddle_h)

score = 0

def reset():
    global ball_pos, ball_speed, score
    ball_pos = [WIDTH // 2, 100]
    ball_speed = [4.0, 4.0]
    score = 0

while True:
    screen.fill(BLACK)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Controls: Left and Right "Push"
    keys = pygame.key.get_pressed()
    
    # Left Paddle Logic
    if keys[pygame.K_LEFT]:
        left_rect.y = kick_y # The "Push Up"
    else:
        left_rect.y = base_y # Back to resting

    # Right Paddle Logic
    if keys[pygame.K_RIGHT]:
        right_rect.y = kick_y
    else:
        right_rect.y = base_y

    # Ball Physics
    ball_speed[1] += gravity
    ball_pos[0] += ball_speed[0]
    ball_pos[1] += ball_speed[1]

    # Wall Bouncing
    if ball_pos[0] <= ball_radius or ball_pos[0] >= WIDTH - ball_radius:
        ball_speed[0] *= -1
    if ball_pos[1] <= ball_radius:
        ball_speed[1] *= -1

    # Collision Detection
    ball_rect = pygame.Rect(ball_pos[0]-ball_radius, ball_pos[1]-ball_radius, ball_radius*2, ball_radius*2)
    
    for pad, is_active in [(left_rect, keys[pygame.K_LEFT]), (right_rect, keys[pygame.K_RIGHT])]:
        if ball_rect.colliderect(pad) and ball_speed[1] > 0:
            score += 1
            # Basic Bounce
            ball_speed[1] *= -0.9 
            
            # The "Power Push": If you hit the key right as the ball touches, launch it!
            if is_active:
                ball_speed[1] = -12 # Big upward thrust
                ball_speed[0] *= 1.2 # Increase speed for difficulty
            else:
                ball_speed[1] = -6 # Gentle bounce if paddle is stationary

    # Game Over (Slipping through the gap or falling)
    if ball_pos[1] > HEIGHT:
        reset()

    # --- Draw ---
    # Draw the "Goal/Gap" visual
    pygame.draw.rect(screen, (50, 0, 0), (WIDTH//2 - 30, base_y, 60, 50))
    
    # Draw Paddles
    pygame.draw.rect(screen, NEON_BLUE, left_rect, border_radius=10)
    pygame.draw.rect(screen, NEON_BLUE, right_rect, border_radius=10)
    
    # Draw Ball
    pygame.draw.circle(screen, NEON_GREEN, (int(ball_pos[0]), int(ball_pos[1])), ball_radius)
    
    # Draw Score
    score_surf = font.render(f"SCORE: {score}", True, WHITE)
    screen.blit(score_surf, (20, 20))

    pygame.display.flip()
    clock.tick(FPS)