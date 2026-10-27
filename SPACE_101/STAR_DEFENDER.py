import pygame
import random
import sys
import math

# --- CONFIGURATION ---
pygame.init()
WIDTH, HEIGHT = 600, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MMP Star Defender: Mission 10")
clock = pygame.time.Clock()

# Colors
SKY_BLUE = (100, 160, 220)
CLOUD_WHITE = (245, 250, 255)
JET_GRAY = (80, 85, 95)
JET_ACCENT = (0, 255, 200) # MMP Cyan
ENEMY_RED = (200, 50, 50)
LASER_GOLD = (255, 255, 0)

# Fonts
font_ui = pygame.font.SysFont("Arial", 22, bold=True)
font_msg = pygame.font.SysFont("Arial", 60, bold=True)

# Game Variables
player_pos = [WIDTH // 2, HEIGHT - 100]
score = 0
lives = 3  # Updated to 3 lives
bullets = []
enemies = []

# Generate clouds for the background treadmill
clouds = [[random.randint(0, WIDTH), random.randint(-HEIGHT, HEIGHT), random.randint(50, 90)] for _ in range(12)]

def draw_jet(surface, x, y):
    # Wings (Bottom Layer)
    pygame.draw.polygon(surface, (60, 65, 75), [(x-40, y+20), (x+40, y+20), (x, y-10)])
    # Main Body
    pygame.draw.polygon(surface, JET_GRAY, [(x, y-35), (x-12, y+25), (x+12, y+25)])
    # Cockpit (Glass)
    pygame.draw.ellipse(surface, (100, 200, 255), (x-5, y-15, 10, 20))
    # Thruster Glow
    glow_rect_l = pygame.Rect(x-10, y+22, 6, 8)
    glow_rect_r = pygame.Rect(x+4, y+22, 6, 8)
    pygame.draw.rect(surface, JET_ACCENT, glow_rect_l, border_radius=2)
    pygame.draw.rect(surface, JET_ACCENT, glow_rect_r, border_radius=2)

def draw_enemy(surface, x, y):
    # Realistic Stealth Shape
    pygame.draw.polygon(surface, (40, 40, 45), [(x, y+25), (x-25, y-15), (x+25, y-15)])
    # Red Cockpit/Eyes
    pygame.draw.circle(surface, ENEMY_RED, (x, y), 5)

def show_end_screen(text, color):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    screen.blit(overlay, (0, 0))
    msg = font_msg.render(text, True, color)
    screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - 50))
    pygame.display.flip()
    pygame.time.delay(3000)

def reset_after_crash():
    """Clears the screen and resets player position without ending the game."""
    global enemies, bullets, player_pos
    enemies.clear()
    bullets.clear()
    player_pos = [WIDTH // 2, HEIGHT - 100]
    # Small pause for the player to get ready
    pygame.time.delay(500)

# --- MAIN LOOP ---
while True:
    screen.fill(SKY_BLUE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # 1. SCROLLING CLOUDS (Background)
    for cloud in clouds:
        cloud[1] += 3
        if cloud[1] > HEIGHT + 100:
            cloud[1] = -100
            cloud[0] = random.randint(0, WIDTH)
        pygame.draw.circle(screen, CLOUD_WHITE, (cloud[0], cloud[1]), cloud[2])
        pygame.draw.circle(screen, CLOUD_WHITE, (cloud[0]-35, cloud[1]+15), cloud[2]//1.5)
        pygame.draw.circle(screen, CLOUD_WHITE, (cloud[0]+35, cloud[1]+15), cloud[2]//1.5)

    # 2. PLAYER MOVEMENT
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_pos[0] > 50: player_pos[0] -= 7
    if keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - 50: player_pos[0] += 7
    
    if keys[pygame.K_SPACE] and len(bullets) < 5:
        bullets.append(pygame.Rect(player_pos[0]-2, player_pos[1]-40, 4, 20))

    # 3. BULLET UPDATE
    for b in bullets[:]:
        b.y -= 15
        pygame.draw.rect(screen, LASER_GOLD, b, border_radius=2)
        if b.bottom < 0: bullets.remove(b)

    # 4. ENEMY MANAGEMENT
    if random.random() < 0.04:
        enemies.append({"rect": pygame.Rect(random.randint(50, WIDTH-50), -60, 50, 40), "speed": random.randint(4, 7)})

    for e in enemies[:]:
        e["rect"].y += e["speed"]
        draw_enemy(screen, e["rect"].centerx, e["rect"].top)

        # Collision: Bullet hits Enemy
        for b in bullets[:]:
            if e["rect"].colliderect(b):
                score += 5
                enemies.remove(e)
                bullets.remove(b)
                break
        
        # Collision: Enemy hits Player
        player_hitbox = pygame.Rect(player_pos[0]-15, player_pos[1]-15, 30, 30)
        if e in enemies and e["rect"].colliderect(player_hitbox):
            # Explosion Effect
            pygame.draw.circle(screen, (255, 100, 0), player_pos, 60)
            pygame.display.flip()
            pygame.time.delay(500)
            
            lives -= 1
            if lives > 0:
                reset_after_crash()
            break
        
        elif e in enemies and e["rect"].top > HEIGHT:
            enemies.remove(e)

    # 5. DRAW PLAYER
    draw_jet(screen, player_pos[0], player_pos[1])

    # 6. UI
    score_txt = font_ui.render(f"SCORE: {score} / 100", True, (50, 50, 50))
    lives_txt = font_ui.render(f"LIVES: {lives}", True, (200, 0, 0))
    screen.blit(score_txt, (20, 20))
    screen.blit(lives_txt, (WIDTH - 120, 20))
    
    # 7. WIN/LOSS TRIGGERS
    if score >= 100:
        show_end_screen("MISSION COMPLETE", JET_ACCENT)
        break
    if lives <= 0:
        show_end_screen("ABORT MISSION", ENEMY_RED)
        break

    pygame.display.flip()
    clock.tick(60)

pygame.quit()