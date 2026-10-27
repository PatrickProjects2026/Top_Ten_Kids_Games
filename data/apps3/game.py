import pygame
import subprocess
import sys

# --- INITIALIZATION ---
pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Polyglot Fighter: C++ Brain, Java Logger")
clock = pygame.time.Clock()

# Character State variables
char_x = 300
char_state = 0 # 0:Idle, 1:Walk, 2:Attack
last_key = "NONE"
attack_timer = 0

# --- MAIN GAME LOOP ---
while True:
    screen.fill((30, 30, 30)) # Dark Grey background
    last_key = "NONE"

    # 1. INPUT HANDLING
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    # Check which key is being held down
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]: 
        last_key = "SPACE"
    elif keys[pygame.K_LEFT]: 
        last_key = "LEFT"
    elif keys[pygame.K_RIGHT]: 
        last_key = "RIGHT"

    # 2. CALL C++ ENGINE (The "Brain")
    # If the character isn't currently attacking, calculate new movement
    if attack_timer <= 0:
        try:
            # Send current X, State, and Input to C++
            raw = subprocess.check_output(["physics.exe", str(char_x), str(char_state), last_key], stderr=subprocess.STDOUT)
            output = raw.decode().strip().split()
            
            if len(output) >= 2:
                char_x = float(output[0])
                char_state = int(output[1])
                
                # If C++ says we started an attack, start the cooldown timer
                if char_state == 2: 
                    attack_timer = 20 
                    # ASYNCHRONOUSLY call Java so it doesn't freeze the game
                    subprocess.Popen(["java", "Logger", "Player_Attacked_at_X_" + str(int(char_x))])
        except Exception as e:
            # If C++ crashes, we print it but keep the game running
            pass 
    else:
        # We are mid-attack, decrease the timer and force state to 2
        attack_timer -= 1
        char_state = 2

    # 3. RENDERING
    # Draw Ground
    pygame.draw.rect(screen, (80, 80, 100), (0, 350, 600, 50))
    
    # Determine color and "bounce" based on state
    color = (0, 255, 150) # Idle (Seafoam Green)
    bob = 0
    
    if char_state == 1: # Walking
        color = (0, 150, 255) # Blue
        bob = (pygame.time.get_ticks() // 100) % 8 # Walking bounce
    elif char_state == 2: # Attacking
        color = (255, 50, 50) # Red
        # Draw Sword Slash
        pygame.draw.rect(screen, (255, 255, 255), (char_x + 45, 290, 50, 8))

    # Draw Body
    pygame.draw.rect(screen, color, (int(char_x), 300 - bob, 40, 50))
    # Draw Head
    pygame.draw.circle(screen, (255, 220, 180), (int(char_x) + 20, 280 - bob), 15)

    pygame.display.flip()
    clock.tick(60)