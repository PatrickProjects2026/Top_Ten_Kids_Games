import pygame
import subprocess
import sys

pygame.init()
screen = pygame.display.set_mode((400, 600))
clock = pygame.time.Clock()

y_pos, y_vel = 100.0, 0.0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # When we quit, tell Java to save the "session"
            subprocess.run(["java", "Logger", "GameSession_Closed"])
            pygame.quit()
            sys.exit()

    # CALL C++ ENGINE FOR PHYSICS
    result = subprocess.check_output(["physics.exe", str(y_pos), str(y_vel)])
    y_pos, y_vel = map(float, result.decode().split())

    # DRAW
    screen.fill((10, 10, 20))
    pygame.draw.circle(screen, (0, 255, 255), (200, int(y_pos)), 20)
    pygame.display.flip()
    clock.tick(60)