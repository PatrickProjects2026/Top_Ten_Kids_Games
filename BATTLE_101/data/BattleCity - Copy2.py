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

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.rect = pygame.Rect(x, y, TILE_SIZE-10, TILE_SIZE-10)
        self.direction = pygame.Vector2(0, 1)
        self.speed = 2
        self.shoot_cooldown = 0
        self.state = "patrol" # States: patrol, hunt

    def can_see_player(self, player_rect, walls):
        # Basic Line of Sight check
        line = pygame.draw.line(pygame.Surface((WIDTH, HEIGHT)), (0,0,0), self.rect.center, player_rect.center)
        for wall in walls:
            if wall.clipline(self.rect.center, player_rect.center):
                return False
        return True

def main():
    try:
        pygame.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        clock = pygame.time.Clock()
        font = pygame.font.SysFont("Impact", 24)

        # Player Setup
        player_rect = pygame.Rect(50, 50, TILE_SIZE-10, TILE_SIZE-10)
        player_dir = pygame.Vector2(0, 1)
        
        # Level Setup
        walls = []
        enemies = []
        for r, row in enumerate(LEVEL_MAP):
            for c, val in enumerate(row):
                if val == 1:
                    walls.append(pygame.Rect(c*TILE_SIZE, r*TILE_SIZE, TILE_SIZE, TILE_SIZE))
        
        # Spawn 3 Hunters
        enemies = [Enemy(550, 550), Enemy(50, 550), Enemy(550, 50)]
        bullets = []
        score = 0
        level = 1

        running = True
        while running:
            screen.fill(BLACK)
            dt = clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT: running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        bullets.append(Bullet(player_rect.centerx, player_rect.centery, player_dir, "player"))

            # 1. PLAYER MOVEMENT
            keys = pygame.key.get_pressed()
            move = pygame.Vector2(0, 0)
            if keys[pygame.K_UP]: move.y = -1
            elif keys[pygame.K_DOWN]: move.y = 1
            elif keys[pygame.K_LEFT]: move.x = -1
            elif keys[pygame.K_RIGHT]: move.x = 1

            if move.length() > 0:
                move = move.normalize()
                player_dir = move
                # X move
                player_rect.x += move.x * 4
                for w in walls:
                    if player_rect.colliderect(w): player_rect.x -= move.x * 4
                # Y move
                player_rect.y += move.y * 4
                for w in walls:
                    if player_rect.colliderect(w): player_rect.y -= move.y * 4

            # 2. HUNTER AI
            for e in enemies:
                # Decide direction
                if e.can_see_player(player_rect, walls):
                    e.state = "hunt"
                    # Vector pointing from Enemy to Player
                    hunt_vec = (pygame.Vector2(player_rect.center) - pygame.Vector2(e.rect.center))
                    if hunt_vec.length() > 0:
                        e.direction = hunt_vec.normalize()
                    
                    # Shoot if clear shot
                    if e.shoot_cooldown <= 0:
                        bullets.append(Bullet(e.rect.centerx, e.rect.centery, e.direction, "enemy"))
                        e.shoot_cooldown = 50
                else:
                    e.state = "patrol"
                
                e.shoot_cooldown -= 1

                # Move Enemy
                old_pos = e.rect.copy()
                e.rect.x += e.direction.x * e.speed
                e.rect.y += e.direction.y * e.speed
                if any(e.rect.colliderect(w) for w in walls):
                    e.rect = old_pos
                    # If patrolling and hit wall, pick random dir
                    if e.state == "patrol":
                        e.direction = pygame.Vector2(random.choice([-1, 0, 1]), random.choice([-1, 0, 1]))

            # 3. BULLETS
            for b in bullets[:]:
                b.pos += b.vel
                b.rect.center = b.pos
                # Hit Wall
                if any(b.rect.colliderect(w) for w in walls):
                    bullets.remove(b)
                    continue
                # Hit Player
                if b.owner == "enemy" and b.rect.colliderect(player_rect):
                    print("GAME OVER")
                    running = False
                # Hit Enemy
                if b.owner == "player":
                    for e in enemies[:]:
                        if b.rect.colliderect(e.rect):
                            enemies.remove(e)
                            bullets.remove(b)
                            score += 100
                            break

            # 4. DRAWING
            for w in walls: pygame.draw.rect(screen, WALL_COLOR, w)
            pygame.draw.rect(screen, TANK_GREEN, player_rect) # Player
            # Draw Barrel
            pygame.draw.line(screen, WHITE, player_rect.center, player_rect.center + player_dir * 20, 4)
            
            for e in enemies:
                pygame.draw.rect(screen, ENEMY_RED, e.rect)
                pygame.draw.line(screen, BLACK, e.rect.center, e.rect.center + e.direction * 20, 3)
            
            for b in bullets:
                pygame.draw.circle(screen, BULLET_COLOR, (int(b.pos.x), int(b.pos.y)), 4)

            score_txt = font.render(f"SCORE: {score}", True, WHITE)
            screen.blit(score_txt, (20, 20))

            if not enemies:
                win_txt = font.render("LEVEL CLEARED!", True, WHITE)
                screen.blit(win_txt, (WIDTH//2-100, HEIGHT//2))

            pygame.display.flip()
        pygame.quit()
    except Exception as e:
        print(f"Error: {e}")
        input("Press Enter to close...")

if __name__ == "__main__":
    main()