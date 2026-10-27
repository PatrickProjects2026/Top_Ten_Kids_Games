import pygame
import sys
import random

# Initialize
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 400
FPS = 60
WHITE = (255, 255, 255)
SKY_BLUE = (30, 30, 50)
JET_COLOR = (0, 255, 255)
OBSTACLE_RED = (255, 80, 80)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Courier New", 24, bold=True)

# Jet Properties
jet_rect = pygame.Rect(50, 200, 40, 20)
velocity = 0
gravity = 0.5
thrust = -8

# Obstacle Setup
obs_width = 50
obs_gap = 150
obs_x = WIDTH
obs_height = random.randint(50, 250)
speed = 5

score = 0

def reset():
    global velocity, obs_x, obs_height, score, speed
    jet_rect.y = 200
    velocity = 0
    obs_x = WIDTH
    obs_height = random.randint(50, 250)
    score = 0
    speed = 5

while True:
    screen.fill(SKY_BLUE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                velocity = thrust # Push up!

    # --- Physics ---
    velocity += gravity
    jet_rect.y += velocity

    # Move Obstacles
    obs_x -= speed
    if obs_x < -obs_width:
        obs_x = WIDTH
        obs_height = random.randint(50, 250)
        score += 1
        speed += 0.2 # Keep speed increasing

    # --- Collision Boxes ---
    # Top Obstacle
    top_obs = pygame.Rect(obs_x, 0, obs_width, obs_height)
    # Bottom Obstacle
    bottom_obs = pygame.Rect(obs_x, obs_height + obs_gap, obs_width, HEIGHT)

    # Check for hits
    if jet_rect.colliderect(top_obs) or jet_rect.colliderect(bottom_obs):
        reset()
    if jet_rect.top <= 0 or jet_rect.bottom >= HEIGHT:
        reset()

    # --- Drawing ---
    # Jet
    pygame.draw.rect(screen, JET_COLOR, jet_rect, border_radius=5)
    # Engine Flame (only when thrusting)
    if velocity < 0:
        pygame.draw.polygon(screen, (255, 165, 0), [
            (jet_rect.left, jet_rect.centery),
            (jet_rect.left - 20, jet_rect.centery - 5),
            (jet_rect.left - 20, jet_rect.centery + 5)
        ])

    # Obstacles
    pygame.draw.rect(screen, OBSTACLE_RED, top_obs)
    pygame.draw.rect(screen, OBSTACLE_RED, bottom_obs)

    # Score
    score_text = font.render(f"DISTANCE: {score}m", True, WHITE)
    screen.blit(score_text, (20, 20))

    pygame.display.flip()
    clock.tick(FPS)