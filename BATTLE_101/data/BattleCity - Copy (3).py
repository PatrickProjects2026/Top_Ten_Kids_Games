import pygame
import sys

# --- CONFIGURATION ---
WIDTH, HEIGHT = 640, 640
TILE_SIZE = 40
FPS = 60

# Colors
BLACK = (20, 20, 20)
WHITE = (250, 250, 250)
TANK_GREEN = (34, 139, 34)
TURRET_COLOR = (0, 100, 0)
WALL_COLOR = (100, 100, 100)

# 1 = Wall, 0 = Floor
# This map now has both horizontal rows and vertical pillars
LEVEL_MAP = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1],
    [1,0,1,1,0,1,0,1,0,1,1,1,1,0,0,1],
    [1,0,1,0,0,1,0,0,0,0,0,0,1,0,0,1],
    [1,0,1,0,1,1,1,1,1,1,0,0,1,0,1,1],
    [1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1],
    [1,1,1,1,0,1,1,1,0,1,1,1,1,0,0,1],
    [1,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1],
    [1,0,1,1,1,1,0,1,1,1,0,1,0,1,0,1],
    [1,0,0,0,0,0,0,1,0,0,0,0,0,1,0,1],
    [1,0,1,1,1,1,1,1,0,1,1,1,1,1,0,1],
    [1,0,1,0,0,0,0,0,0,0,0,0,0,1,0,1],
    [1,0,1,0,1,1,1,0,1,1,1,1,0,1,0,1],
    [1,0,0,0,1,0,0,0,0,0,0,1,0,0,0,1],
    [1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

class Tank:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, TILE_SIZE-6, TILE_SIZE-6)
        self.speed = 3
        self.direction = pygame.Vector2(0, -1) # Facing Up initially

    def draw(self, surf):
        # 1. Draw Tread (The base of the tank)
        pygame.draw.rect(surf, TANK_GREEN, self.rect, border_radius=3)
        
        # 2. Draw Turret (The top part)
        center = self.rect.center
        pygame.draw.circle(surf, TURRET_COLOR, center, 12)
        
        # 3. Draw Barrel (Pointing in direction)
        barrel_end = (center[0] + self.direction.x * 20, 
                      center[1] + self.direction.y * 20)
        pygame.draw.line(surf, TURRET_COLOR, center, barrel_end, 6)

def main():
    try:
        pygame.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Realistic Tank Movement")
        clock = pygame.time.Clock()

        player = Tank(45, 45)
        walls = []
        for r, row in enumerate(LEVEL_MAP):
            for c, val in enumerate(row):
                if val == 1:
                    walls.append(pygame.Rect(c*TILE_SIZE, r*TILE_SIZE, TILE_SIZE, TILE_SIZE))

        running = True
        while running:
            dt = clock.tick(FPS)
            screen.fill(BLACK)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # --- MOVEMENT LOGIC ---
            keys = pygame.key.get_pressed()
            move_vec = pygame.Vector2(0, 0)
            
            if keys[pygame.K_UP]:    move_vec.y = -1
            elif keys[pygame.K_DOWN]:  move_vec.y = 1
            elif keys[pygame.K_LEFT]:  move_vec.x = -1
            elif keys[pygame.K_RIGHT]: move_vec.x = 1

            if move_vec.length() > 0:
                move_vec = move_vec.normalize() # Prevents fast diagonal movement
                player.direction = move_vec      # Update barrel direction
                
                # Try moving X
                old_x = player.rect.x
                player.rect.x += move_vec.x * player.speed
                for wall in walls:
                    if player.rect.colliderect(wall):
                        player.rect.x = old_x

                # Try moving Y
                old_y = player.rect.y
                player.rect.y += move_vec.y * player.speed
                for wall in walls:
                    if player.rect.colliderect(wall):
                        player.rect.y = old_y

            # --- DRAWING ---
            for wall in walls:
                # Draw grid-based walls
                pygame.draw.rect(screen, WALL_COLOR, wall)
                pygame.draw.rect(screen, BLACK, wall, 1) # Outline for grid look

            player.draw(screen)
            pygame.display.flip()

        pygame.quit()

    except Exception as e:
        print(f"Error: {e}")
        input("Press Enter to close...")

if __name__ == "__main__":
    main()