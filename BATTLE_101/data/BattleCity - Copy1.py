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
        self.vel = direction * 6
        self.rect = pygame.Rect(0, 0, 6, 6)
        self.rect.center = x, y
        self.owner = owner

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
        font = pygame.font.SysFont("Arial", 24, bold=True)
        
        # --- GAME STATE ---
        score = 0
        level = 1
        enemy_speed_multiplier = 1.0
        player_score = 0
        
        def spawn_enemies(multiplier):
            return [
                Tank(580, 580, ENEMY_RED), 
                Tank(580, 45, ENEMY_RED), 
                Tank(45, 580, ENEMY_RED)
            ]

        player = Tank(45, 45, TANK_GREEN, True)
        enemies = spawn_enemies(enemy_speed_multiplier)
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
                    
                    if e.move_timer <= 0:
                        e.direction = random.choice([pygame.Vector2(0,1), pygame.Vector2(0,-1), pygame.Vector2(1,0), pygame.Vector2(-1,0)])
                        e.move_timer = random.randint(30, 80)
                    
                    old_pos = e.rect.copy()
                    e.rect.x += e.direction.x * (2 * enemy_speed_multiplier)
                    e.rect.y += e.direction.y * (2 * enemy_speed_multiplier)
                    if any(e.rect.colliderect(w) for w in walls): e.rect = old_pos
                    
                    if e.shoot_timer <= 0:
                        bullets.append(Bullet(e.rect.centerx, e.rect.centery, e.direction, "enemy"))
                        e.shoot_timer = max(20, 60 - (level * 5)) # Enemies shoot faster each level

                # 3. BULLET LOGIC
                for b in bullets[:]:
                    b.pos += b.vel
                    b.rect.center = b.pos
                    if any(b.rect.colliderect(w) for w in walls):
                        if b in bullets: bullets.remove(b)
                        continue
                    if b.owner == "enemy" and b.rect.colliderect(player.rect):
                        game_over = True
                    if b.owner == "player":
                        for e in enemies[:]:
                            if b.rect.colliderect(e.rect):
                                enemies.remove(e)
                                if b in bullets: bullets.remove(b)
                                player_score += 100
                                break

                # 4. LEVEL UP LOGIC
                if not enemies:
                    level += 1
                    enemy_speed_multiplier += 0.3 # 30% speed boost
                    player.rect.topleft = (45, 45) # Reset player pos
                    enemies = spawn_enemies(enemy_speed_multiplier)
                    bullets = [] # Clear screen

            # 5. DRAWING
            for w in walls: pygame.draw.rect(screen, WALL_COLOR, w)
            player.draw(screen)
            for e in enemies: e.draw(screen)
            for b in bullets: pygame.draw.circle(screen, BULLET_YELLOW, (int(b.pos.x), int(b.pos.y)), 3)

            # UI Text
            ui_text = font.render(f"Level: {level}   Score: {player_score}", True, WHITE)
            screen.blit(ui_text, (50, 10))

            if game_over:
                msg = font.render("GAME OVER! Press Space to Exit", True, ENEMY_RED)
                screen.blit(msg, (WIDTH//2 - 150, HEIGHT//2))
                if keys[pygame.K_SPACE]: running = False

            pygame.display.flip()
        pygame.quit()
    except Exception as e:
        print(f"Error: {e}")
        input("Press Enter to close...")

if __name__ == "__main__":
    main()