import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 500, 600
BLACK = (10, 10, 15)
NEON_GREEN = (57, 255, 20)
NEON_BLUE = (0, 255, 255)
NEON_PINK = (255, 0, 255)
WHITE = (255, 255, 255)
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cyber-Roll Pinball")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Courier New", 28, bold=True)

# Game State
ball_pos = [WIDTH // 2, 100]
ball_speed = [4.0, 4.0]
ball_radius = 10
gravity = 0.25
score = 0
high_score = 0

# Paddle Config
base_y = 540
kick_offset = 40  # How much it jumps up
gap_half_width = 40

def draw_background():
    # Draw a perspective grid for a "Synthwave" look
    for i in range(0, WIDTH + 50, 40):
        pygame.draw.line(screen, (30, 30, 60), (i, 0), (i, HEIGHT), 1)
    for i in range(0, HEIGHT, 40):
        pygame.draw.line(screen, (30, 30, 60), (0, i), (WIDTH, i), 1)
    # Bottom danger zone glow
    pygame.draw.rect(screen, (80, 0, 0), (WIDTH//2 - gap_half_width, base_y, gap_half_width*2, HEIGHT-base_y))

def get_paddle_polys(left_active, right_active):
    # We define the paddles as slanting DOWN towards the center
    ly = base_y - (kick_offset if left_active else 0)
    ry = base_y - (kick_offset if right_active else 0)
    
    # Left Paddle (Slants down to the right)
    left_pts = [(10, ly - 20), (WIDTH//2 - gap_half_width, ly + 10), 
                (WIDTH//2 - gap_half_width, ly + 30), (10, ly)]
    
    # Right Paddle (Slants down to the left)
    right_pts = [(WIDTH - 10, ry - 20), (WIDTH//2 + gap_half_width, ry + 10), 
                 (WIDTH//2 + gap_half_width, ry + 30), (WIDTH - 10, ry)]
    
    return left_pts, right_pts

def reset():
    global ball_pos, ball_speed, score, high_score
    if score > high_score: high_score = score
    ball_pos = [WIDTH // 2, 100]
    ball_speed = [4.0, 2.0]
    score = 0

# --- Main Loop ---
while True:
    screen.fill(BLACK)
    draw_background()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    l_up, r_up = keys[pygame.K_LEFT], keys[pygame.K_RIGHT]
    
    # Physics
    ball_speed[1] += gravity
    ball_pos[0] += ball_speed[0]
    ball_pos[1] += ball_speed[1]

    # Wall Bounce
    if ball_pos[0] <= ball_radius or ball_pos[0] >= WIDTH - ball_radius:
        ball_speed[0] *= -0.9
        ball_pos[0] = max(ball_radius, min(WIDTH - ball_radius, ball_pos[0]))
    if ball_pos[1] <= ball_radius:
        ball_speed[1] *= -1

    # Collision Logic
    left_pts, right_pts = get_paddle_polys(l_up, r_up)
    
    # Simple Point-in-Polygon is heavy, so we use a Rect proxy for collision 
    # but adjust velocity based on the slant!
    ball_rect = pygame.Rect(ball_pos[0]-ball_radius, ball_pos[1]-ball_radius, ball_radius*2, ball_radius*2)
    
    for i, pts in enumerate([left_pts, right_pts]):
        pad_rect = pygame.Rect(min(p[0] for p in pts), min(p[1] for p in pts), 
                               max(p[0] for p in pts) - min(p[0] for p in pts), 20)
        
        if ball_rect.colliderect(pad_rect) and ball_speed[1] > 0:
            score += 1
            is_active = l_up if i == 0 else r_up
            
            # Physics: Slant force (Roll toward center)
            # Left paddle pushes right (+), Right paddle pushes left (-)
            slant_dir = 1.5 if i == 0 else -1.5
            ball_speed[0] += slant_dir 
            
            if is_active:
                ball_speed[1] = -14 # Massive Kick
                ball_speed[0] *= 1.1 # Speed up
            else:
                ball_speed[1] *= -0.8 # Dead bounce
            
            # Prevent clipping
            ball_pos[1] = pad_rect.top - ball_radius

    # Win/Loss
    if ball_pos[1] > HEIGHT:
        reset()

    # Draw everything
    pygame.draw.polygon(screen, NEON_BLUE, left_pts)
    pygame.draw.polygon(screen, NEON_BLUE, right_pts)
    pygame.draw.circle(screen, WHITE, (int(ball_pos[0]), int(ball_pos[1])), ball_radius + 2)
    pygame.draw.circle(screen, NEON_GREEN, (int(ball_pos[0]), int(ball_pos[1])), ball_radius)
    
    # UI
    score_txt = font.render(f"SCORE: {score}", True, NEON_PINK)
    high_txt = font.render(f"BEST: {high_score}", True, WHITE)
    screen.blit(score_txt, (20, 20))
    screen.blit(high_txt, (WIDTH - 160, 20))

    pygame.display.flip()
    clock.tick(FPS)