import pygame
import random
import sys

# 1. SETUP
WIDTH, HEIGHT = 600, 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
RED = (231, 76, 60)
BRICK_COLOR = (165, 42, 42)
CANNON_COLOR = (46, 204, 113)

def main():
    try:
        pygame.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Target Gallery")
        clock = pygame.time.Clock()

        # Game Objects
        cannon_x = WIDTH // 2
        bullets = [] # List of pygame.Rect
        targets = [] # List of pygame.Rect
        bricks = []  # List of pygame.Rect

        # Generate Bricks (Simple Wall)
        for row in range(3):
            for col in range(10):
                brick = pygame.Rect(col * 60 + 2, row * 30 + 150, 56, 26)
                bricks.append(brick)

        # Function to spawn a target
        def spawn_target():
            return pygame.Rect(random.randint(0, WIDTH-40), 50, 40, 40)

        targets.append(spawn_target())

        score = 0
        font = pygame.font.SysFont("Arial", 24)

        running = True
        while running:
            screen.fill(BLACK)
            clock.tick(FPS)

            # --- 2. INPUT ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        # Shoot a bullet from cannon position
                        bullets.append(pygame.Rect(cannon_x + 15, HEIGHT - 50, 10, 20))

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and cannon_x > 0:
                cannon_x -= 7
            if keys[pygame.K_RIGHT] and cannon_x < WIDTH - 40:
                cannon_x += 7

            # --- 3. LOGIC ---
            # Move Bullets
            for b in bullets[:]:
                b.y -= 10
                if b.bottom < 0: bullets.remove(b)

            # Move Targets
            for t in targets:
                t.x += 3
                if t.left > WIDTH: t.right = 0

            # Collision: Bullet vs Brick
            for b in bullets[:]:
                for br in bricks[:]:
                    if b.colliderect(br):
                        bricks.remove(br)
                        if b in bullets: bullets.remove(b)

            # Collision: Bullet vs Target
            for b in bullets[:]:
                for t in targets[:]:
                    if b.colliderect(t):
                        score += 10
                        targets.remove(t)
                        targets.append(spawn_target()) # Spawn new one
                        if b in bullets: bullets.remove(b)

            # --- 4. DRAWING ---
            # Draw Cannon
            pygame.draw.rect(screen, CANNON_COLOR, (cannon_x, HEIGHT - 30, 40, 20))
            pygame.draw.rect(screen, CANNON_COLOR, (cannon_x + 15, HEIGHT - 50, 10, 20))

            # Draw Bricks
            for br in bricks:
                pygame.draw.rect(screen, BRICK_COLOR, br)

            # Draw Targets
            for t in targets:
                pygame.draw.circle(screen, RED, t.center, 20)
                pygame.draw.circle(screen, WHITE, t.center, 10)

            # Draw Bullets
            for b in bullets:
                pygame.draw.rect(screen, WHITE, b)

            # Draw Score
            score_text = font.render(f"Score: {score}", True, WHITE)
            screen.blit(score_text, (10, 10))

            pygame.display.flip()

        pygame.quit()

    except Exception as e:
        # This keeps the window open if the code crashes!
        print(f"\nCRASH REPORT:\n{e}")
        input("\nPress ENTER to close...")

if __name__ == "__main__":
    main()