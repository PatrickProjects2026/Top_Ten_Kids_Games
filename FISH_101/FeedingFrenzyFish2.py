import pygame
import random
import sys

# Initialize
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 500
FPS = 60
OCEAN_BLUE = (0, 70, 120)
FISH_ORANGE = (255, 120, 0)
CORAL_RED = (200, 50, 50)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Courier New", 28, bold=True)

# Game Variables
player_pos = [100, 250]
player_speed = 6
score = 0
game_speed = 5  # Initial obstacle speed

# Obstacles: list of Rects
obstacles = []
def spawn_obstacle():
    h = random.randint(100, 300)
    # Randomly spawn from top or bottom
    if random.choice([True, False]):
        return pygame.Rect(WIDTH, 0, 40, h) # Top spike
    else:
        return pygame.Rect(WIDTH, HEIGHT - h, 40, h) # Bottom spike

# Initial spawn
for i in range(3):
    obs = spawn_obstacle()
    obs.x += i * 300
    obstacles.append(obs)

def draw_fish(surface, pos):
    x, y = pos
    # Body (Ellipse)
    pygame.draw.ellipse(surface, FISH_ORANGE, (x, y, 50, 30))
    # Tail (Triangle)
    points = [(x, y + 15), (x - 15, y), (x - 15, y + 30)]
    pygame.draw.polygon(surface, FISH_ORANGE, points)
    # Eye
    pygame.draw.circle(surface, (255, 255, 255), (int(x + 35), int(y + 10)), 4)
    pygame.draw.circle(surface, (0, 0, 0), (int(x + 36), int(y + 10)), 2)

while True:
    screen.fill(OCEAN_BLUE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # --- Movement Logic ---
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player_pos[1] > 0:
        player_pos[1] -= player_speed
    if keys[pygame.K_DOWN] and player_pos[1] < HEIGHT - 30:
        player_pos[1] += player_speed

    # Create a hit-box for the fish
    player_rect = pygame.Rect(player_pos[0] - 10, player_pos[1], 60, 30)

    # --- Obstacle & Difficulty Logic ---
    for obs in obstacles[:]:
        obs.x -= game_speed
        
        # Collision
        if player_rect.colliderect(obs):
            print(f"Final Score: {score}")
            pygame.quit()
            sys.exit()
            
        # Reset obstacle when it leaves screen
        if obs.right < 0:
            obstacles.remove(obs)
            obstacles.append(spawn_obstacle())
            score += 1
            # Increase speed every 5 points
            if score % 5 == 0:
                game_speed += 0.5

    # --- Drawing ---
    # Draw obstacles
    for obs in obstacles:
        pygame.draw.rect(screen, CORAL_RED, obs, border_radius=5)
    
    # Draw the fish shape
    draw_fish(screen, player_pos)
    
    # Draw Score
    text = font.render(f"SCORE: {score} SPEED: {int(game_speed)}", True, (255, 255, 255))
    screen.blit(text, (20, 20))

    pygame.display.flip()
    clock.tick(FPS)