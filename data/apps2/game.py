import pygame
import subprocess
import sys

# Setup
pygame.init()
screen = pygame.display.set_mode((400, 700))
clock = pygame.time.Clock()

# Game State
ball_pos = [200, 650]
ball_vel = 0
pins = [True] * 10 # True means pin is standing
pin_pos = [
    (200, 100), (180, 80), (220, 80), 
    (160, 60), (200, 60), (240, 60),
    (140, 40), (180, 40), (220, 40), (260, 40)
]

print("Bowling Game Started. Press SPACE to bowl!")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            score = pins.count(False)
            subprocess.run(["java", "Logger", f"FinalScore_{score}_Pins"])
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and ball_vel == 0:
                ball_vel = -7 # Launch ball up the lane

    # --- PHYSICS VIA C++ ---
    if ball_vel != 0:
        try:
            raw = subprocess.check_output(["physics.exe", str(ball_pos[0]), str(ball_pos[1]), str(ball_vel)])
            bx, by, hit_idx = map(float, raw.decode().split())
            
            ball_pos = [bx, by]
            hit_idx = int(hit_idx)
            
            if hit_idx != -1 and pins[hit_idx]:
                pins[hit_idx] = False
                subprocess.run(["java", "Logger", f"Pin_{hit_idx}_Down"])

            if by < 0: # Reset ball
                ball_pos = [200, 650]
                ball_vel = 0
        except:
            pass

    # --- DRAWING ---
    screen.fill((40, 40, 40)) # Dark lane
    pygame.draw.rect(screen, (100, 60, 20), (100, 0, 200, 700)) # Wood lane
    
    # Draw Pins
    for i, p in enumerate(pin_pos):
        if pins[i]:
            pygame.draw.circle(screen, (255, 255, 255), p, 10)
    
    # Draw Ball
    pygame.draw.circle(screen, (200, 0, 0), (int(ball_pos[0]), int(ball_pos[1])), 15)

    pygame.display.flip()
    clock.tick(60)