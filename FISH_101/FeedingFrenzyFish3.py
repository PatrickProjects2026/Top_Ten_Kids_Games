import pygame
import random
import sys

# Initialize
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 500
FPS = 60
OCEAN_BLUE = (0, 70, 120)
FISH_ORANGE = (255, 165, 0)
SEAWEED_GREEN = (34, 139, 34)
OBSTACLE_COLOR = (120, 70, 50) # Rock-like color

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Courier New", 28, bold=True)

# Game Variables
player_pos = [100, 250]
player_speed = 7
score = 0
game_speed = 5

# --- Decoration Setup ---
# Seaweed (Trees) - Static positions
seaweed_list = []
for i in range(15):
    x = random.randint(0, WIDTH)
    h = random.randint(40, 100)
    seaweed_list.append({'rect': pygame.Rect(x, HEIGHT - h, 15, h), 'sway': random.uniform(0, 6.28)})

# Ambient Fish (Background busyness)
ambient_fish = []
for _ in range(10):
    ambient_fish.append({
        'x': random.randint(0, WIDTH),
        'y': random.randint(0, HEIGHT),
        'speed': random.uniform(1, 3),
        'size': random.uniform(0.4, 0.7),
        'color': (random.randint(50, 150), random.randint(150, 255), 255)
    })

# --- Obstacle Logic ---
obstacles = [pygame.Rect(WIDTH + i*300, random.randint(0,1)* (HEIGHT-200), 40, 200) for i in range(3)]

def draw_fish_shape(surface, x, y, color, scale=1.0, eye_color=(255,255,255)):
    # Body
    width, height = int(50 * scale), int(30 * scale)
    pygame.draw.ellipse(surface, color, (x, y, width, height))
    # Tail
    tail_pts = [(x, y + height//2), (x - int(15*scale), y), (x - int(15*scale), y + height)]
    pygame.draw.polygon(surface, color, tail_pts)
    # Eye
    eye_x = int(x + width * 0.7)
    eye_y = int(y + height * 0.3)
    pygame.draw.circle(surface, eye_color, (eye_x, eye_y), int(4 * scale))

while True:
    screen.fill(OCEAN_BLUE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # --- 1. Background Decorations (Seaweed & Small Fish) ---
    for s in seaweed_list:
        # Subtle sway effect using sine wave
        sway_offset = int(5 * pygame.math.Vector2(1, 0).rotate(pygame.time.get_ticks() * 0.2 + s['sway'] * 100).x)
        pygame.draw.rect(screen, SEAWEED_GREEN, (s['rect'].x + sway_offset, s['rect'].y, s['rect'].width, s['rect'].height), border_top_left_radius=10)

    for af in ambient_fish:
        af['x'] -= af['speed']
        if af['x'] < -50: af['x'] = WIDTH + 50
        draw_fish_shape(screen, af['x'], af['y'], af['color'], scale=af['size'], eye_color=(200,200,200))

    # --- 2. Player Movement ---
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player_pos[1] > 0: player_pos[1] -= player_speed
    if keys[pygame.K_DOWN] and player_pos[1] < HEIGHT - 30: player_pos[1] += player_speed

    player_rect = pygame.Rect(player_pos[0], player_pos[1], 50, 30)

    # --- 3. Obstacles & Collision ---
    for obs in obstacles:
        obs.x -= game_speed
        if obs.right < 0:
            obs.x = WIDTH + random.randint(100, 300)
            obs.height = random.randint(100, 250)
            if random.choice([True, False]): obs.y = 0 
            else: obs.y = HEIGHT - obs.height
            score += 1
            game_speed += 0.1

        if player_rect.colliderect(obs):
            score = 0
            game_speed = 5
            player_pos[1] = 250

        pygame.draw.rect(screen, OBSTACLE_COLOR, obs, border_radius=8)

    # --- 4. Draw Player ---
    draw_fish_shape(screen, player_pos[0], player_pos[1], FISH_ORANGE)

    # UI
    score_surf = font.render(f"SCORE: {score}", True, (255, 255, 255))
    screen.blit(score_surf, (20, 20))

    pygame.display.flip()
    clock.tick(FPS)