import pygame
import subprocess
import sys
import os

# --- CONFIGURATION ---
ENGINE_EXE = "physics.exe"
JAVA_CLASS = "Logger"
SCREEN_SIZE = (400, 600)
FLOOR_Y = 550  # Boundary for the physics engine

def check_dependencies():
    """Ensure the compiled files exist before starting."""
    if not os.path.exists(ENGINE_EXE):
        print(f"ERROR: {ENGINE_EXE} not found. Did you run the Batch script?")
        sys.exit(1)

def call_physics(y, v):
    """Communicates with the C++ Engine."""
    try:
        # We pass the floor position so the C++ engine knows when to bounce
        result = subprocess.check_output([ENGINE_EXE, str(y), str(v), str(FLOOR_Y)], stderr=subprocess.STDOUT)
        return map(float, result.decode().strip().split())
    except subprocess.CalledProcessError as e:
        print(f"C++ Engine Crashed: {e.output.decode()}")
        return y, 0.0

# --- INITIALIZATION ---
check_dependencies()
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Polyglot Engine: Py + C++ + Java")
clock = pygame.time.Clock()

# State variables
y_pos, y_vel = 100.0, 0.0

# --- MAIN LOOP ---
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("Closing session via Java Logger...")
            subprocess.run(["java", JAVA_CLASS, "GameSession_Closed_FinalPos_" + str(int(y_pos))])
            pygame.quit()
            sys.exit()

    # 1. ADVANCED PHYSICS CALL
    # We now receive updated position and velocity from the C++ process
    y_pos, y_vel = call_physics(y_pos, y_vel)

    # 2. DRAWING
    screen.fill((10, 10, 30)) # Dark Blue background
    
    # Draw Floor
    pygame.draw.rect(screen, (50, 50, 80), (0, FLOOR_Y + 20, 400, 50))
    
    # Draw "Glow" effect for the ball
    pygame.draw.circle(screen, (0, 100, 100), (200, int(y_pos)), 25)
    # Draw Ball
    pygame.draw.circle(screen, (0, 255, 255), (200, int(y_pos)), 20)

    pygame.display.flip()
    clock.tick(60)