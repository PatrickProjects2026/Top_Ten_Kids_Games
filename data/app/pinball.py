import pygame
import pymunk

# 1. SETUP
pygame.init()
screen = pygame.display.set_mode((400, 600))
# This clock forces the game to run at a steady speed
clock = pygame.time.Clock() 

# 2. PHYSICS SETUP
space = pymunk.Space()
space.gravity = (0, 900)

# 3. THE MAIN LOOP (Crucial!)
running = True
while running:
    # A. Check for "Quit" events so the window doesn't freeze
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # B. Update Physics
    space.step(1/60.0)

    # C. Drawing
    screen.fill((30, 30, 30)) # Clear the screen with dark gray
    
    # [Insert your drawing code here]

    # D. Refresh the screen
    pygame.display.flip()
    
    # E. Maintain 60 Frames Per Second
    clock.tick(60)

pygame.quit()