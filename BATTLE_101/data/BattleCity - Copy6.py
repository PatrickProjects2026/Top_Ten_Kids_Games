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
HEART_RED = (255, 50, 50)

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
        self.rect.center = (x, y)
        self.owner = owner

class Enemy:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, TILE_SIZE-12, TILE_SIZE-12)
        self.direction = pygame.Vector2(random.choice([-1, 1]), 0)
        self.speed = 2.0
        self.shoot_cooldown = 0
        self.state = "patrol"
        self.hunt_timer = 0

    def can_see_player(self, player_rect, walls):
        # Line of sight check
        line = (self.rect.center, player_rect.center)
        for wall in walls:
            if wall.clipline(line):
                return False
        return True

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tank Battle - Stable Build")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 22, bold=True)

    def reset_game():
        return {
            "player_rect": pygame.Rect(60, 60, TILE_SIZE-12, TILE_SIZE-12),
            "player_dir": pygame.Vector2(0, 1),
            "enemies": [Enemy(540, 540), Enemy(540, 60), Enemy(60, 540)],
            "bullets": [],
            "score": 0, "lives": 3, "invuln": 0, "state": "PLAYING"
        }

    game = reset_game()
    walls = [pygame.Rect(c*TILE_SIZE, r*TILE_SIZE, TILE_SIZE, TILE_SIZE) 
             for r, row in enumerate(LEVEL_MAP) for c, val in enumerate(row) if val == 1]

    # --- MAIN LOOP ---
    while True:
        # 1. Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if game["state"] == "PLAYING" and event.key == pygame.K_SPACE:
                    game["bullets"].append(Bullet(game["player_rect"].centerx, game["player_rect"].centery, game["player_dir"], "player"))
                elif game["state"] != "PLAYING" and event.key == pygame.K_r:
                    game = reset_game()

        # 2. Logic Update
        if game["state"] == "PLAYING":
            # Player Movement
            keys = pygame.key.get_pressed()
            move = pygame.Vector2(0, 0)
            if keys[pygame.K_UP]: move.y = -1
            elif keys[pygame.K_DOWN]: move.y = 1
            elif keys[pygame.K_LEFT]: move.x = -1
            elif keys[pygame.K_RIGHT]: move.x = 1

            if move.length() > 0:
                move = move.normalize()
                game["player_dir"] = move
                # X-axis movement
                game["player_rect"].x += move.x * 4
                for w in walls:
                    if game["player_rect"].colliderect(w):
                        game["player_rect"].x -= move.x * 4
                # Y-axis movement
                game["player_rect"].y += move.y * 4
                for w in walls:
                    if game["player_rect"].colliderect(w):
                        game["player_rect"].y -= move.y * 4

            # Enemy Update
            for e in game["enemies"]:
                if e.can_see_player(game["player_rect"], walls):
                    e.state = "hunt"
                    e.hunt_timer = 90 # Stay aggressive for 1.5 seconds
                
                if e.state == "hunt":
                    target_vec = (pygame.Vector2(game["player_rect"].center) - pygame.Vector2(e.rect.center))
                    if target_vec.length() > 0:
                        e.direction = target_vec.normalize()
                    
                    if e.shoot_cooldown <= 0:
                        game["bullets"].append(Bullet(e.rect.centerx, e.rect.centery, e.direction, "enemy"))
                        e.shoot_cooldown = 60
                    
                    e.hunt_timer -= 1
                    if e.hunt_timer <= 0: e.state = "patrol"

                # Move Enemy
                e.shoot_cooldown -= 1
                old_rect = e.rect.copy()
                e.rect.x += e.direction.x * e.speed
                e.rect.y += e.direction.y * e.speed
                
                if any(e.rect.colliderect(w) for w in walls):
                    e.rect = old_rect
                    if e.state == "patrol":
                        e.direction = pygame.Vector2(random.choice([-1, 0, 1]), random.choice([-1, 0, 1]))
                        if e.direction.length() == 0: e.direction = pygame.Vector2(1, 0)

            # Bullet Logic
            if game["invuln"] > 0: game["invuln"] -= 1
            for b in game["bullets"][:]:
                b.pos += b.vel
                b.rect.center = (int(b.pos.x), int(b.pos.y))
                
                hit_wall = any(b.rect.colliderect(w) for w in walls)
                
                if hit_wall:
                    if b in game["bullets"]: game["bullets"].remove(b)
                    continue

                if b.owner == "enemy" and b.rect.colliderect(game["player_rect"]) and game["invuln"] <= 0:
                    game["lives"] -= 1
                    game["invuln"] = 60
                    game["player_rect"].topleft = (60, 60)
                    if b in game["bullets"]: game["bullets"].remove(b)
                    if game["lives"] <= 0: game["state"] = "LOST"
                
                elif b.owner == "player":
                    for e in game["enemies"][:]:
                        if b.rect.colliderect(e.rect):
                            game["enemies"].remove(e)
                            if b in game["bullets"]: game["bullets"].remove(b)
                            game["score"] += 100
                            break
            
            if not game["enemies"]: game["state"] = "WON"

        # 3. Rendering (Always happens)
        screen.fill(BLACK)
        for w in walls:
            pygame.draw.rect(screen, WALL_COLOR, w)
        
        # Draw Player
        if game["invuln"] % 10 < 5:
            pygame.draw.rect(screen, TANK_GREEN, game["player_rect"])
            pygame.draw.line(screen, WHITE, game["player_rect"].center, 
                             game["player_rect"].center + game["player_dir"] * 20, 3)
        
        # Draw Enemies
        for e in game["enemies"]:
            pygame.draw.rect(screen, ENEMY_RED, e.rect)
        
        # Draw Bullets
        for b in game["bullets"]:
            pygame.draw.circle(screen, BULLET_COLOR, (int(b.pos.x), int(b.pos.y)), 4)

        # UI
        ui_txt = font.render(f"SCORE: {game['score']}  LIVES: {game['lives']}", True, WHITE)
        screen.blit(ui_txt, (20, 10))
        
        if game["state"] != "PLAYING":
            end_txt = font.render(f"{game['state']}! PRESS 'R' TO RESTART", True, WHITE)
            screen.blit(end_txt, (WIDTH//2 - 150, HEIGHT//2))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()