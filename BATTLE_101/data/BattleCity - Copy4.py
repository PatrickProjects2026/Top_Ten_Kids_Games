import pygame
import random
import sys

# --- CONFIGURATION ---
WIDTH, HEIGHT = 640, 640
TILE_SIZE = 40
FPS = 60

# Colors
BLACK = (20, 20, 20)
WHITE = (250, 250, 250)
TANK_GREEN = (34, 139, 34)
ENEMY_RED = (200, 30, 30)
WALL_COLOR = (60, 60, 60)
BULLET_COLOR = (255, 200, 0)

# 1 = Wall, 0 = Floor
LEVEL_MAP = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,0,1,1,1,1,1,1,0,1,1,0,1],
    [1,0,1,0,0,0,0,0,0,0,0,0,0,1,0,1],
    [1,0,1,0,1,1,0,1,1,0,1,1,0,1,0,1],
    [1,0,0,0,1,0,0,0,0,0,0,1,0,0,0,1],
    [1,0,1,0,1,0,1,1,1,1,0,1,0,1,0,1],
    [1,0,1,0,0,0,1,0,0,1,0,0,0,1,0,1],
    [1,0,1,0,1,0,1,0,0,1,0,1,0,1,0,1],
    [1,0,0,0,1,0,1,1,1,1,0,1,0,0,0,1],
    [1,0,1,0,1,0,0,0,0,0,0,1,0,1,0,1],
    [1,0,1,0,1,1,1,1,1,1,1,1,0,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,0,1,1,0,0,1,1,0,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

class Bullet:
    def __init__(self, x, y, direction, owner):
        self.pos = pygame.Vector2(x, y)
        self.vel = direction * 7
        self.rect = pygame.Rect(0, 0, 6, 6)
        self.rect.center = x, y
        self.owner = owner

class Enemy:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, TILE_SIZE-10, TILE_SIZE-10)
        self.direction = pygame.Vector2(0, 1)
        self.speed = 2
        self.shoot_cooldown = random.randint(50, 100) # Stop them from shooting instantly

def main():
    try:
        pygame.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        clock = pygame.time.Clock()
        font = pygame.font.SysFont("Impact", 32)

        # 1. PLAYER START (Top Left)
        player_rect = pygame.Rect(50, 50, TILE_SIZE-10, TILE_SIZE-10)
        player_dir = pygame.Vector2(0, 1)
        
        walls = [pygame.Rect(c*TILE_SIZE, r*TILE_SIZE, TILE_SIZE, TILE_SIZE) 
                 for r, row in enumerate(LEVEL_MAP) for c, val in enumerate(row) if val == 1]
        
        # 2. ENEMY START (Far Corners only)
        # We spawn them at (550, 550) so they are as far as possible from the player
        enemies = [Enemy(550, 550), Enemy(500, 550), Enemy(550, 500)]
        bullets = []
        
        # 3. COUNTDOWN TIMER
        # 3 seconds * 60 FPS = 180 frames
        countdown = 180 
        running = True

        while running:
            screen.fill(BLACK)
            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT: running = False

            # --- COUNTDOWN LOGIC ---
            if countdown > 0:
                for w in walls: pygame.draw.rect(screen, WALL_COLOR, w)
                pygame.draw.rect(screen, TANK_GREEN, player_rect)
                for e in enemies: pygame.draw.rect(screen, ENEMY_RED, e.rect)
                
                # Show countdown on screen
                count_text = font.render(f"READY? {countdown//60 + 1}", True, WHITE)
                screen.blit(count_text, (WIDTH//2 - 50, HEIGHT//2))
                countdown -= 1
                pygame.display.flip()
                continue # Skip the rest of the game logic until countdown is 0

            # --- GAME LOGIC (Only runs after countdown) ---
            keys = pygame.key.get_pressed()
            move = pygame.Vector2(0, 0)
            if keys[pygame.K_UP]: move.y = -1
            elif keys[pygame.K_DOWN]: move.y = 1
            elif keys[pygame.K_LEFT]: move.x = -1
            elif keys[pygame.K_RIGHT]: move.x = 1
            
            if keys[pygame.K_SPACE]: # Shoot
                if len([b for b in bullets if b.owner == "player"]) < 3: # Limit bullets
                    bullets.append(Bullet(player_rect.centerx, player_rect.centery, player_dir, "player"))

            if move.length() > 0:
                move = move.normalize()
                player_dir = move
                player_rect.x += move.x * 4
                for w in walls:
                    if player_rect.colliderect(w): player_rect.x -= move.x * 4
                player_rect.y += move.y * 4
                for w in walls:
                    if player_rect.colliderect(w): player_rect.y -= move.y * 4

            for e in enemies:
                # Basic Chase AI
                hunt_vec = (pygame.Vector2(player_rect.center) - pygame.Vector2(e.rect.center))
                if hunt_vec.length() > 0:
                    e.direction = hunt_vec.normalize()
                
                e.rect.x += e.direction.x * e.speed
                if any(e.rect.colliderect(w) for w in walls): e.rect.x -= e.direction.x * e.speed
                e.rect.y += e.direction.y * e.speed
                if any(e.rect.colliderect(w) for w in walls): e.rect.y -= e.direction.y * e.speed

                e.shoot_cooldown -= 1
                if e.shoot_cooldown <= 0:
                    bullets.append(Bullet(e.rect.centerx, e.rect.centery, e.direction, "enemy"))
                    e.shoot_cooldown = 100 # Reset shoot timer

            for b in bullets[:]:
                b.pos += b.vel
                b.rect.center = b.pos
                if any(b.rect.colliderect(w) for w in walls): bullets.remove(b)
                elif b.owner == "enemy" and b.rect.colliderect(player_rect):
                    print("HIT! GAME OVER")
                    running = False
                elif b.owner == "player":
                    for e in enemies[:]:
                        if b.rect.colliderect(e.rect):
                            enemies.remove(e)
                            if b in bullets: bullets.remove(b)
                            break

            # --- DRAWING ---
            for w in walls: pygame.draw.rect(screen, WALL_COLOR, w)
            pygame.draw.rect(screen, TANK_GREEN, player_rect)
            pygame.draw.line(screen, WHITE, player_rect.center, player_rect.center + player_dir * 20, 3)
            for e in enemies: pygame.draw.rect(screen, ENEMY_RED, e.rect)
            for b in bullets: pygame.draw.circle(screen, BULLET_COLOR, (int(b.pos.x), int(b.pos.y)), 4)

            pygame.display.flip()
        
        pygame.quit()

    except Exception as e:
        print(f"ERROR DETECTED: {e}")
        input("Press ENTER to see error and close...")

if __name__ == "__main__":
    main()