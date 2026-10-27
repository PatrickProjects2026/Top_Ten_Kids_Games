import pygame
import random
import sys

# Initialize
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
WATER_COLOR = (0, 105, 148)
PLAYER_COLOR = (255, 165, 0) # Orange
ENEMY_COLOR = (200, 50, 50)  # Reddish

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24, bold=True)

# Player Properties
player_size = 20
player_pos = [WIDTH // 2, HEIGHT // 2]
score = 0

# Enemy List: stores [x, y, size, speed]
enemies = []

def spawn_enemy():
    size = random.randint(10, player_size + 40) # Can be smaller or bigger
    side = random.choice(["left", "right"])
    if side == "left":
        x = -50
        speed = random.randint(2, 5)
    else:
        x = WIDTH + 50
        speed = random.randint(-5, -2)
    y = random.randint(0, HEIGHT - size)
    return [x, y, size, speed]

# Initial spawn
for _ in range(8):
    enemies.append(spawn_enemy())

while True:
    screen.fill(WATER_COLOR)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Movement: Follow Mouse
    mouse_x, mouse_y = pygame.mouse.get_pos()
    player_pos[0] += (mouse_x - player_pos[0]) * 0.1
    player_pos[1] += (mouse_y - player_pos[1]) * 0.1
    
    player_rect = pygame.Rect(player_pos[0], player_pos[1], player_size, player_size)

    # Update Enemies
    for e in enemies[:]:
        e[0] += e[3] # Move x by speed
        
        # Remove if off-screen and spawn new one
        if e[0] < -100 or e[0] > WIDTH + 100:
            enemies.remove(e)
            enemies.append(spawn_enemy())
            
        # Collision Logic
        enemy_rect = pygame.Rect(e[0], e[1], e[2], e[2])
        if player_rect.colliderect(enemy_rect):
            if player_size >= e[2]:
                # Eat it!
                score += 1
                player_size += 2 # Grow!
                enemies.remove(e)
                enemies.append(spawn_enemy())
            else:
                # Game Over!
                print(f"Eaten by a bigger fish! Score: {score}")
                pygame.quit()
                sys.exit()

    # --- Draw ---
    # Draw Player (it gets bigger visually)
    pygame.draw.ellipse(screen, PLAYER_COLOR, player_rect)
    
    # Draw Enemies
    for e in enemies:
        color = (100, 255, 100) if player_size >= e[2] else ENEMY_COLOR
        enemy_draw_rect = pygame.Rect(e[0], e[1], e[2], e[2])
        pygame.draw.ellipse(screen, color, enemy_draw_rect)

    # Score and Current Size
    score_text = font.render(f"Score: {score}  |  Size: {player_size}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(FPS)