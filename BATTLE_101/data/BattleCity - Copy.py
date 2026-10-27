import pygame
import random
import sys

# --- CONFIGURATION ---
WIDTH, HEIGHT = 520, 520
TILE_SIZE = 40
FPS = 60

# Colors
BLACK = (0, 0, 0)
BRICK = (165, 42, 42)
PLAYER_COLOR = (255, 255, 0)
ENEMY_COLOR = (255, 0, 0)
BULLET_COLOR = (255, 255, 255)

# 1 = Wall, 0 = Empty
LEVEL_MAP = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,1,1,0,1,1,0,1,1,0,1,1,0],
    [0,1,1,0,1,1,0,1,1,0,1,1,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,1,1,0,1,1,1,1,1,0,1,1,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,1,1,0,1,1,0,1,1,0,1,1,0],
    [0,1,1,0,0,0,0,0,0,0,1,1,0],
    [0,0,0,0,1,1,0,1,1,0,0,0,0],
    [0,1,1,0,1,1,0,1,1,0,1,1,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,1,1,0,0,1,1,1,0,0,1,1,0],
    [0,0,0,0,0,1,0,1,0,0,0,0,0],
]

class Bullet:
    def __init__(self, x, y, dx, dy):
        self.rect = pygame.Rect(x, y, 8, 8)
        self.dx, self.dy = dx, dy
    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

class Tank:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, TILE_SIZE-4, TILE_SIZE-4)
        self.color = color
        self.direction = (0, -4)
        self.bullets = []
    def draw(self, surf):
        pygame.draw.rect(surf, self.color, self.rect)
        cx = self.rect.centerx + self.direction[0] * 4
        cy = self.rect.centery + self.direction[1] * 4
        pygame.draw.circle(surf, (200, 200, 200), (cx, cy), 5)
    def shoot(self):
        if len(self.bullets) < 2:
            self.bullets.append(Bullet(self.rect.centerx, self.rect.centery, self.direction[0]*2, self.direction[1]*2))

def main():
    try:
        pygame.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Battle City Pro")
        clock = pygame.time.Clock()
        
        player = Tank(200, 480, PLAYER_COLOR)
        enemies = [Tank(40, 40, ENEMY_COLOR), Tank(440, 40, ENEMY_COLOR)]
        
        running = True
        while running:
            screen.fill(BLACK)
            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT: running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: player.shoot()

            # Player Movement & Wall Logic
            keys = pygame.key.get_pressed()
            old_pos = player.rect.copy()
            if keys[pygame.K_LEFT]:  player.rect.x -= 4; player.direction = (-4, 0)
            elif keys[pygame.K_RIGHT]: player.rect.x += 4; player.direction = (4, 0)
            elif keys[pygame.K_UP]:    player.rect.y -= 4; player.direction = (0, -4)
            elif keys[pygame.K_DOWN]:  player.rect.y += 4; player.direction = (0, 4)

            # Check Wall Collision
            for r in range(len(LEVEL_MAP)):
                for c in range(len(LEVEL_MAP[r])):
                    if LEVEL_MAP[r][c] == 1:
                        if player.rect.colliderect(pygame.Rect(c*TILE_SIZE, r*TILE_SIZE, TILE_SIZE, TILE_SIZE)):
                            player.rect = old_pos

            # Update & Draw everything
            for b in player.bullets[:]:
                b.move()
                bx, by = b.rect.x // TILE_SIZE, b.rect.y // TILE_SIZE
                if 0 <= by < len(LEVEL_MAP) and 0 <= bx < len(LEVEL_MAP[0]) and LEVEL_MAP[by][bx] == 1:
                    LEVEL_MAP[by][bx] = 0
                    player.bullets.remove(b)
                elif not screen.get_rect().contains(b.rect): player.bullets.remove(b)

            # Render Loop
            for r in range(len(LEVEL_MAP)):
                for c in range(len(LEVEL_MAP[r])):
                    if LEVEL_MAP[r][c] == 1:
                        pygame.draw.rect(screen, BRICK, (c*TILE_SIZE, r*TILE_SIZE, TILE_SIZE-2, TILE_SIZE-2))
            
            player.draw(screen)
            for b in player.bullets: pygame.draw.rect(screen, BULLET_COLOR, b.rect)
            for e in enemies: e.draw(screen)
            
            pygame.display.flip()
        pygame.quit()

    except Exception as e:
        print(f"\n[ERROR] Game crashed: {e}")
        print("Try running 'pip install pygame' in your terminal.")
        input("\nPress ENTER to close...")

if __name__ == "__main__":
    main()