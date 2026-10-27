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
WALL_COLOR = (80, 80, 80)
BULLET_YELLOW = (255, 255, 0)

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

class Bullet:
    def __init__(self, x, y, direction, owner):
        self.pos = pygame.Vector2(x, y)
        self.vel = direction * 5
        self.rect = pygame.Rect(0, 0, 6, 6)
        self.rect.center = x, y
        self.owner = owner # Keep track of who shot it

class Tank:
    def __init__(self, x, y, color, is_player=False):
        self.rect = pygame.Rect(x, y, TILE_SIZE-8, TILE_SIZE-8)
        self.color = color
        self.is_player = is_player
        self.direction = pygame.Vector2(0, -1)
        self.move_timer = 0
        self.shoot_timer = 0

    def draw(self, surf):
        pygame.draw.rect(surf, self.color, self.rect, border_radius=3)
        center = self.rect.center
        barrel_end = (center[0] + self.direction.x * 20, center[1] + self.direction.y * 20)
        pygame.draw.line(surf, WHITE if self.is_player else BLACK, center, barrel_end, 4)

def main():
    try:
        pygame.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        clock = pygame.time.Clock()
        
        player = Tank(45, 45, TANK_GREEN, True)
        enemies = [Tank(580, 580, ENEMY_RED), Tank(580, 45, ENEMY_RED), Tank(45, 580, ENEMY_RED)]
        bullets = []
        walls = [pygame.Rect(c*TILE_SIZE, r*TILE_SIZE, TILE_SIZE, TILE_SIZE) 
                 for r, row in enumerate(LEVEL_MAP) for c, val in enumerate(row) if val == 1]

        running = True
        game_over = False

        while running:
            screen.fill(BLACK)
            dt = clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT: running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not game_over:
                    bullets.append(Bullet(player.rect.centerx, player.rect.centery, player.direction, "player"))

            if not game_over:
                # 1. PLAYER MOVEMENT
                keys = pygame.key.get_pressed()
                p_vec = pygame.Vector2(0, 0)
                if keys[pygame.K_UP]: p_vec.y = -1
                elif keys[pygame.K_DOWN]: p_vec.y = 1
                elif keys[pygame.K_LEFT]: p_vec.x = -1
                elif keys[pygame.K_RIGHT]: p_vec.x = 1

                if p_vec.length() > 0:
                    player.direction = p_vec.normalize()
                    for axis in ['x', 'y']:
                        old = getattr(player.rect, axis)
                        setattr(player.rect, axis, old + getattr(player.direction, axis) * 3)
                        if any(player.rect.colliderect(w) for w in walls): setattr(player.rect, axis, old)

                # 2. ENEMY AI
                for e in enemies:
                    e.move_timer -= 1
                    e.shoot_timer -= 1
                    
                    # Random Movement
                    if e.move_timer <= 0:
                        e.direction = random.choice([pygame.Vector2(0,1), pygame.Vector2(0,-1), pygame.Vector2(1,0), pygame.Vector2(-1,0)])
                        e.move_timer = random.randint(30, 80)
                    
                    old_pos = e.rect.copy()
                    e.rect.x += e.direction.x * 2
                    e.rect.y += e.direction.y * 2
                    if any(e.rect.colliderect(w) for w in walls): e.rect = old_pos
                    
                    # AI Shooting (Cooldown)
                    if e.shoot_timer <= 0:
                        bullets.append(Bullet(e.rect.centerx, e.rect.centery, e.direction, "enemy"))
                        e.shoot_timer = 60

                # 3. BULLET LOGIC
                for b in bullets[:]:
                    b.pos += b.vel
                    b.rect.center = b.pos
                    
                    # Wall hit
                    if any(b.rect.colliderect(w) for w in walls):
                        bullets.remove(b)
                        continue
                    
                    # Hit Player
                    if b.owner == "enemy" and b.rect.colliderect(player.rect):
                        game_over = True
                        print("YOU DIED!")
                    
                    # Hit Enemy
                    if b.owner == "player":
                        for e in enemies[:]:
                            if b.rect.colliderect(e.rect):
                                enemies.remove(e)
                                bullets.remove(b)
                                break

            # 4. DRAWING
            for w in walls: pygame.draw.rect(screen, WALL_COLOR, w)
            player.draw(screen)
            for e in enemies: e.draw(screen)
            for b in bullets: pygame.draw.circle(screen, BULLET_YELLOW, (int(b.pos.x), int(b.pos.y)), 3)

            if game_over:
                font = pygame.font.SysFont("Arial", 40)
                msg = font.render("GAME OVER - YOU WERE HIT!", True, ENEMY_RED)
                screen.blit(msg, (WIDTH//2 - 200, HEIGHT//2))

            if not enemies:
                font = pygame.font.SysFont("Arial", 40)
                msg = font.render("VICTORY - ENEMIES DESTROYED!", True, TANK_GREEN)
                screen.blit(msg, (WIDTH//2 - 200, HEIGHT//2))

            pygame.display.flip()
        pygame.quit()
    except Exception as e:
        print(f"Error: {e}")
        input("Press Enter to close...")

if __name__ == "__main__":
    main()