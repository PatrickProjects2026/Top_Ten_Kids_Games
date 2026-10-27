import pygame
import sys

# --- CONFIGURATION ---
pygame.init()
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Table Tennis 101")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
GREEN = (34, 139, 34)
BLACK = (0, 0, 0)

# Game Variables
paddle_w, paddle_h = 80, 15
ball_size = 10

player_pos = [WIDTH//2 - paddle_w//2, HEIGHT - 30]
enemy_pos = [WIDTH//2 - paddle_w//2, 20]
ball_pos = [WIDTH//2, HEIGHT//2]
ball_vel = [4, 4]

player_score = 0
enemy_score = 0
font = pygame.font.SysFont("Arial", 30, bold=True)
victory_score = 5

def reset_ball():
    return [WIDTH//2, HEIGHT//2], [4, 4 if ball_vel[1] < 0 else -4]

# --- MAIN LOOP ---
running = True
winner = None

while running:
    screen.fill(GREEN) # Tennis table green
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if not winner:
        # 1. INPUT HANDLING (Left/Right)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_pos[0] > 0:
            player_pos[0] -= 7
        if keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - paddle_w:
            player_pos[0] += 7

        # 2. AI LOGIC (Simple tracking)
        if enemy_pos[0] + paddle_w//2 < ball_pos[0]:
            enemy_pos[0] += 5
        elif enemy_pos[0] + paddle_w//2 > ball_pos[0]:
            enemy_pos[0] -= 5

        # 3. BALL PHYSICS
        ball_pos[0] += ball_vel[0]
        ball_pos[1] += ball_vel[1]

        # Wall Bounce (Left/Right)
        if ball_pos[0] <= 0 or ball_pos[0] >= WIDTH - ball_size:
            ball_vel[0] *= -1

        # Paddle Collision (Player)
        player_rect = pygame.Rect(player_pos[0], player_pos[1], paddle_w, paddle_h)
        if player_rect.collidepoint(ball_pos[0], ball_pos[1] + ball_size):
            ball_vel[1] *= -1.1 # Speed up slightly
            ball_pos[1] = player_pos[1] - ball_size

        # Paddle Collision (Enemy)
        enemy_rect = pygame.Rect(enemy_pos[0], enemy_pos[1], paddle_w, paddle_h)
        if enemy_rect.collidepoint(ball_pos[0], ball_pos[1]):
            ball_vel[1] *= -1.1
            ball_pos[1] = enemy_pos[1] + paddle_h

        # 4. SCORING
        if ball_pos[1] < 0:
            player_score += 1
            ball_pos, ball_vel = reset_ball()
        elif ball_pos[1] > HEIGHT:
            enemy_score += 1
            ball_pos, ball_vel = reset_ball()

        # Check Victory
        if player_score >= victory_score: winner = "PLAYER"
        if enemy_score >= victory_score: winner = "CPU"

    # --- DRAWING ---
    # Net
    pygame.draw.line(screen, WHITE, (0, HEIGHT//2), (WIDTH, HEIGHT//2), 2)
    
    # Paddles & Ball
    pygame.draw.rect(screen, WHITE, (player_pos[0], player_pos[1], paddle_w, paddle_h))
    pygame.draw.rect(screen, WHITE, (enemy_pos[0], enemy_pos[1], paddle_w, paddle_h))
    pygame.draw.circle(screen, WHITE, (int(ball_pos[0]), int(ball_pos[1])), ball_size)

    # Score UI
    p_text = font.render(str(player_score), True, WHITE)
    e_text = font.render(str(enemy_score), True, WHITE)
    screen.blit(e_text, (WIDTH - 40, HEIGHT//2 - 50))
    screen.blit(p_text, (WIDTH - 40, HEIGHT//2 + 20))

    if winner:
        win_text = font.render(f"{winner} WINS!", True, BLACK)
        screen.blit(win_text, (WIDTH//2 - 100, HEIGHT//2 - 20))

    pygame.display.flip()
    clock.tick(60)