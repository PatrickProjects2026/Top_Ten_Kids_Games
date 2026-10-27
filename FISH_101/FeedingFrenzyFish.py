import pygame
import random
import sys
import math

# Initialize
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 500
FPS = 60
OCEAN_BLUE = (0, 70, 120)
FISH_ORANGE = (255, 165, 0)
SEAWEED_GREEN = (34, 139, 34)
OBSTACLE_COLOR = (120, 70, 50)
VICTORY_SCORE = 50

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Courier New", 28, bold=True)
big_font = pygame.font.SysFont("Courier New", 72, bold=True)

# Game State
player_pos = [100, 250]
player_speed = 7
score = 0
lives = 3
game_speed = 5
game_active = True
victory = False

# --- Decorations ---
seaweed = [{'x': random.randint(0, WIDTH), 'h': random.randint(40, 100), 's': random.uniform(0, 6)} for _ in range(15)]
ambient_fish = [{'x': random.randint(0, WIDTH), 'y': random.randint(0, HEIGHT), 'speed': random.uniform(1, 3), 'size': random.uniform(0.4, 0.7)} for _ in range(10)]
bubbles = [{'x': random.randint(0, WIDTH), 'y': random.randint(HEIGHT, HEIGHT+500), 'speed': random.uniform(1, 2)} for _ in range(20)]

# --- Obstacles ---
obstacles = [pygame.Rect(WIDTH + i*300, 0, 40, 150) for i in range(3)]

def draw_fish_shape(surface, x, y, color, scale=1.0):
    w, h = int(50 * scale), int(30 * scale)
    pygame.draw.ellipse(surface, color, (x, y, w, h)) # Body
    pygame.draw.polygon(surface, color, [(x, y + h//2), (x - int(15*scale), y), (x - int(15*scale), y + h)]) # Tail
    pygame.draw.circle(surface, (255,255,255), (int(x + w*0.7), int(y + h*0.3)), int(4*scale)) # Eye

def reset_player():
    global player_pos, game_speed
    player_pos = [100, 250]
    game_speed = 5
    # Invincibility flicker could go here

while True:
    screen.fill(OCEAN_BLUE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        if event.type == pygame.KEYDOWN and not game_active:
            # Restart game on key press if game over or victory
            score, lives, game_speed, game_active, victory = 0, 3, 5, True, False
            reset_player()

    if game_active:
        # --- 1. Background Logic ---
        for b in bubbles:
            b['y'] -= b['speed']
            if b['y'] < -10: b['y'] = HEIGHT + 10; b['x'] = random.randint(0, WIDTH)
            pygame.draw.circle(screen, (255, 255, 255), (int(b['x']), int(b['y'])), 2, 1)

        for af in ambient_fish:
            af['x'] -= af['speed']
            if af['x'] < -50: af['x'] = WIDTH + 50
            draw_fish_shape(screen, af['x'], af['y'], (100, 180, 230), af['size'])

        for s in seaweed:
            sway = int(math.sin(pygame.time.get_ticks() * 0.005 + s['s']) * 10)
            pygame.draw.rect(screen, SEAWEED_GREEN, (s['x'] + sway, HEIGHT - s['h'], 15, s['h']), border_top_left_radius=10)

        # --- 2. Player Controls ---
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and player_pos[1] > 0: player_pos[1] -= player_speed
        if keys[pygame.K_DOWN] and player_pos[1] < HEIGHT - 30: player_pos[1] += player_speed
        player_rect = pygame.Rect(player_pos[0], player_pos[1], 50, 30)

        # --- 3. Obstacles & Scoring ---
        for obs in obstacles:
            obs.x -= game_speed
            if obs.right < 0:
                obs.x = WIDTH + random.randint(100, 200)
                obs.height = random.randint(120, 250)
                obs.y = 0 if random.choice([True, False]) else HEIGHT - obs.height
                score += 1
                game_speed += 0.2
                if score >= VICTORY_SCORE:
                    game_active = False
                    victory = True

            if player_rect.colliderect(obs):
                lives -= 1
                if lives <= 0:
                    game_active = False
                else:
                    obs.x = WIDTH + 400 # Move the obstacle away so you don't hit it twice
                    reset_player()

            pygame.draw.rect(screen, OBSTACLE_COLOR, obs, border_radius=8)

        # --- 4. Draw Player & HUD ---
        draw_fish_shape(screen, player_pos[0], player_pos[1], FISH_ORANGE)
        
        score_txt = font.render(f"SCORE: {score}/{VICTORY_SCORE}", True, (255,255,255))
        lives_txt = font.render(f"LIVES: {'♥' * lives}", True, (255, 100, 100))
        screen.blit(score_txt, (20, 20))
        screen.blit(lives_txt, (20, 50))

    else:
        # --- Victory / Game Over Screens ---
        msg = "VICTORY!" if victory else "GAME OVER"
        color = (255, 215, 0) if victory else (255, 50, 50)
        txt_surf = big_font.render(msg, True, color)
        retry_surf = font.render("Press any key to Restart", True, (255, 255, 255))
        screen.blit(txt_surf, (WIDTH//2 - 180, HEIGHT//2 - 50))
        screen.blit(retry_surf, (WIDTH//2 - 180, HEIGHT//2 + 50))

    pygame.display.flip()
    clock.tick(FPS)