import pygame

pygame.init()
screen = pygame.display.set_mode((400, 300))

# THIS LOOP KEEPS THE GAME ALIVE
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False # This stops the loop when you close the window

    screen.fill((50, 50, 50))
    pygame.display.flip()

pygame.quit()