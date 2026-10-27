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
GOLD = (255, 215, 0)

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
        self.rect.center = (int(x), int(y))
        self.owner = owner

class Enemy:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, TILE_SIZE-12, TILE_SIZE-12)
        self.direction = pygame.Vector2(0, 1)
        self.speed = 2
        self.shoot_cooldown = 100 
        self.state = "patrol"

    def can_see_player(self, player_rect, walls):
        for wall in walls:
            if wall.clipline(self.rect.center, player_rect.center):
                return False
        return True

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Impact", 24)
    big_font = pygame.font.SysFont("Impact", 64)

    walls = [pygame.Rect(c*TILE_SIZE, r*TILE_SIZE, TILE_SIZE, TILE_SIZE) 
             for r, row in enumerate(LEVEL_MAP) for c, val in enumerate(row) if val == 1]

    def reset_game():
        return {
            "player_rect": pygame.Rect(60, 60, 28, 28),
            "player_dir": pygame.Vector2(0, 1),
            "enemies": [Enemy(560, 560), Enemy(60, 560), Enemy(560, 60)],
            "bullets": [],
            "score": 0,
            "start_ticks": pygame.time.get_ticks(),
            "state": "PLAYING" # States: PLAYING, GAMEOVER, VICTORY
        }

    game = reset_game()

    while True:
        screen.fill(BLACK)
        dt = clock.tick(FPS)
        
        seconds_passed = (pygame.time.get_ticks() - game["start_ticks"]) / 1000
        grace_active = seconds_passed < 3 and game["state"] == "PLAYING"

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game["state"] == "PLAYING":
                    game["bullets"].append(Bullet(game["player_rect"].centerx, game["player_rect"].centery, game["player_dir"], "player"))
                
                # Restart if game is over or won
                if event.key == pygame.K_r and game["state"] != "PLAYING":
                    game = reset_game()

        if game["state"] == "PLAYING":
            # 1. PLAYER MOVEMENT
            keys = pygame.key.get_pressed()
            move = pygame.Vector2(0, 0)
            if keys[pygame.K_UP]: move.y = -1
            elif keys[pygame.K_DOWN]: move.y = 1
            elif keys[pygame.K_LEFT]: move.x = -1
            elif keys[pygame.K_RIGHT]: move.x = 1

            if move.length() > 0:
                move = move.normalize()
                game["player_dir"] = move
                # X Movement
                game["player_rect"].x += move.x * 4
                for w in walls:
                    if game["player_rect"].colliderect(w):
                        if move.x > 0: game["player_rect"].right = w.left
                        else: game["player_rect"].left = w.right
                # Y Movement
                game["player_rect"].y += move.y * 4
                for w in walls:
                    if game["player_rect"].colliderect(w):
                        if move.y > 0: game["player_rect"].bottom = w.top
                        else: game["player_rect"].top = w.bottom

            # 2. ENEMY AI
            for e in game["enemies"]:
                if e.can_see_player(game["player_rect"], walls):
                    e.state = "hunt"
                    hunt_vec = (pygame.Vector2(game["player_rect"].center) - pygame.Vector2(e.rect.center))
                    if hunt_vec.length() > 0: e.direction = hunt_vec.normalize()
                    
                    if e.shoot_cooldown <= 0 and not grace_active:
                        game["bullets"].append(Bullet(e.rect.centerx, e.rect.centery, e.direction, "enemy"))
                        e.shoot_cooldown = 60
                else:
                    e.state = "patrol"
                
                e.shoot_cooldown -= 1
                old_pos = e.rect.copy()
                e.rect.x += e.direction.x * e.speed
                e.rect.y += e.direction.y * e.speed
                if any(e.rect.colliderect(w) for w in walls):
                    e.rect = old_pos
                    if e.state == "patrol":
                        e.direction = pygame.Vector2(random.choice([-1, 0, 1]), random.choice([-1, 0, 1]))

            # 3. BULLETS
            for b in game["bullets"][:]:
                b.pos += b.vel
                b.rect.center = (int(b.pos.x), int(b.pos.y))
                if any(b.rect.colliderect(w) for w in walls):
                    if b in game["bullets"]: game["bullets"].remove(b)
                    continue
                if b.owner == "enemy" and b.rect.colliderect(game["player_rect"]):
                    game["state"] = "GAMEOVER"
                if b.owner == "player":
                    for e in game["enemies"][:]:
                        if b.rect.colliderect(e.rect):
                            game["enemies"].remove(e)
                            if b in game["bullets"]: game["bullets"].remove(b)
                            game["score"] += 100
                            break
            
            # Check for Victory
            if not game["enemies"]:
                game["state"] = "VICTORY"

        # 4. DRAWING
        for w in walls: pygame.draw.rect(screen, WALL_COLOR, w)
        pygame.draw.rect(screen, TANK_GREEN, game["player_rect"])
        pygame.draw.line(screen, WHITE, game["player_rect"].center, game["player_rect"].center + game["player_dir"] * 20, 4)
        for e in game["enemies"]:
            pygame.draw.rect(screen, ENEMY_RED, e.rect)
        for b in game["bullets"]:
            pygame.draw.circle(screen, BULLET_COLOR, (int(b.pos.x), int(b.pos.y)), 4)

        # UI OVERLAYS
        screen.blit(font.render(f"SCORE: {game['score']}", True, WHITE), (20, 20))
        
        if grace_active:
            timer_txt = font.render(f"GET READY! {3 - int(seconds_passed)}", True, (255, 100, 100))
            screen.blit(timer_txt, (WIDTH//2 - 60, 20))

        if game["state"] == "GAMEOVER":
            txt = big_font.render("WASTED", True, (200, 0, 0))
            screen.blit(txt, (WIDTH//2 - 100, HEIGHT//2 - 50))
            screen.blit(font.render("PRESS 'R' TO RESTART", True, WHITE), (WIDTH//2 - 100, HEIGHT//2 + 30))

        if game["state"] == "VICTORY":
            txt = big_font.render("VICTORY!", True, GOLD)
            screen.blit(txt, (WIDTH//2 - 110, HEIGHT//2 - 50))
            screen.blit(font.render("PRESS 'R' TO PLAY AGAIN", True, WHITE), (WIDTH//2 - 110, HEIGHT//2 + 30))

        pygame.display.flip()

if __name__ == "__main__":
    main()