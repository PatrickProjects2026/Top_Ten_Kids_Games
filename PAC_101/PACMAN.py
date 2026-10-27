import pygame
import sys
import math
import random

# --- CONFIGURATION ---
pygame.init()
WIDTH, HEIGHT = 600, 500 
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man 101 - MMP Edition")
clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
WHITE = (240, 240, 240)
RED = (255, 80, 80)
ACCENT = (0, 255, 200)

# Game Variables
score = 0
lives = 3
font = pygame.font.SysFont("Arial", 24, bold=True)
status_font = pygame.font.SysFont("Arial", 48, bold=True)

# 1 = Wall, 0 = Path/Pellet
MAZE = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]
TILE_SIZE = 50

# Player Setup
player_pos = [75.0, 75.0] 
player_speed = 3
direction = 0 

# --- RANDOM ENEMIES SETUP ---
num_enemies = random.randint(1, 3)
ghosts = []
spawn_points = [[525, 75], [525, 275], [75, 275]] # Corners

for i in range(num_enemies):
    # Each ghost gets a random spawn point and a slight speed variation
    ghosts.append({
        "pos": list(random.choice(spawn_points)),
        "speed": 1.2 + (random.random() * 0.5)
    })

pellets = []
for r in range(len(MAZE)):
    for c in range(len(MAZE[r])):
        if MAZE[r][c] == 0:
            pellets.append(pygame.Rect(c * TILE_SIZE + 22, r * TILE_SIZE + 22, 6, 6))

def check_collision(x, y):
    rect = pygame.Rect(x - 12, y - 12, 24, 24)
    for r in range(len(MAZE)):
        for c in range(len(MAZE[r])):
            if MAZE[r][c] == 1:
                wall = pygame.Rect(c * TILE_SIZE, r * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if rect.colliderect(wall):
                    return True
    return False

def reset_positions():
    global player_pos, ghosts
    player_pos = [75.0, 75.0]
    for g in ghosts:
        g["pos"] = list(random.choice(spawn_points))

# --- MAIN LOOP ---
while True:
    screen.fill(BLACK)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # --- VICTORY CHECK ---
    if score >= 200: # Increased victory requirement for more fun with 3 ghosts
        vic_text = status_font.render("VICTORY!", True, ACCENT)
        screen.blit(vic_text, (WIDTH//2 - 100, HEIGHT//2 - 50))
        pygame.display.flip()
        pygame.time.delay(2000)
        pygame.quit()
        sys.exit()

    # --- PLAYER MOVEMENT ---
    keys = pygame.key.get_pressed()
    next_x, next_y = player_pos[0], player_pos[1]
    
    if keys[pygame.K_LEFT]:  next_x -= player_speed; direction = 180
    elif keys[pygame.K_RIGHT]: next_x += player_speed; direction = 0
    elif keys[pygame.K_UP]:    next_y -= player_speed; direction = 90
    elif keys[pygame.K_DOWN]:  next_y += player_speed; direction = 270

    if not check_collision(next_x, next_y):
        player_pos = [next_x, next_y]

    # --- GHOST AI (MULTIPLE ENEMIES) ---
    for g in ghosts:
        gx, gy = g["pos"]
        if gx < player_pos[0]: gx += g["speed"]
        else: gx -= g["speed"]
        if gy < player_pos[1]: gy += g["speed"]
        else: gy -= g["speed"]

        if not check_collision(gx, gy):
            g["pos"] = [gx, gy]

    # --- PELLET COLLECTION ---
    p_rect = pygame.Rect(player_pos[0]-12, player_pos[1]-12, 24, 24)
    for pellet in pellets[:]:
        if p_rect.colliderect(pellet):
            pellets.remove(pellet)
            score += 10

    # --- DRAWING ---
    for r in range(len(MAZE)):
        for c in range(len(MAZE[r])):
            if MAZE[r][c] == 1:
                pygame.draw.rect(screen, BLUE, (c*TILE_SIZE, r*TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)
    
    for p in pellets:
        pygame.draw.circle(screen, WHITE, p.center, 3)

    # Animated Pacman
    mouth_var = abs(math.sin(pygame.time.get_ticks() * 0.01)) * 45
    pygame.draw.circle(screen, YELLOW, (int(player_pos[0]), int(player_pos[1])), 15)
    p1 = (int(player_pos[0]), int(player_pos[1]))
    angle_rad = math.radians(mouth_var)
    p2 = (player_pos[0] + 20 * math.cos(math.radians(direction) - angle_rad),
          player_pos[1] - 20 * math.sin(math.radians(direction) - angle_rad))
    p3 = (player_pos[0] + 20 * math.cos(math.radians(direction) + angle_rad),
          player_pos[1] - 20 * math.sin(math.radians(direction) + angle_rad))
    pygame.draw.polygon(screen, BLACK, [p1, p2, p3])

    # Draw All Ghosts
    for g in ghosts:
        pygame.draw.circle(screen, RED, (int(g["pos"][0]), int(g["pos"][1])), 15)

    # UI (Score & Lives)
    s_text = font.render(f"SCORE: {score} | LIVES: {lives} | ENEMIES: {num_enemies}", True, ACCENT)
    screen.blit(s_text, (20, HEIGHT - 40))

    # --- COLLISION & RESTART LOGIC ---
    for g in ghosts:
        g_rect = pygame.Rect(g["pos"][0]-12, g["pos"][1]-12, 24, 24)
        if p_rect.colliderect(g_rect):
            lives -= 1
            if lives > 0:
                # Restart/Reset Positions
                reset_positions()
                pygame.time.delay(500)
            else:
                # Total Loss
                loss_text = status_font.render("GAME OVER", True, RED)
                screen.blit(loss_text, (WIDTH//2 - 130, HEIGHT//2 - 50))
                pygame.display.flip()
                pygame.time.delay(2000)
                pygame.quit()
                sys.exit()

    pygame.display.flip()
    clock.tick(60)