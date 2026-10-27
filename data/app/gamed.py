import pygame
import random
import math
import sys

# --- SAFETY WRAPPER ---
def main():
    try:
        pygame.init()
        
        # 1. Constants & Screen
        WIDTH, HEIGHT = 600, 800
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pro 3D Racer - Complete")
        clock = pygame.time.Clock()

        # Colors
        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)
        ROAD_GRAY = (40, 40, 40)
        NEON_BLUE = (0, 242, 255)
        CAR_RED = (200, 30, 30)

        # 2. Physics & 3D Variables
        # player_x is the lane position (-250 to 250)
        player_x = 0
        player_speed = 0
        target_speed = 800 # Pixels per second
        
        # Z-positions for road lines to create 3D depth
        road_lines = [i for i in range(0, 2000, 100)]
        
        # 3. Particle System for Exhaust
        particles = [] # Each entry: [x, y, life, size, vx]

        # --- INTERNAL FUNCTIONS ---
        def project_3d(x, y, z):
            """Transforms 3D coordinates into 2D screen coordinates."""
            fov = 400
            # m is the scaling factor based on distance (Z)
            # As Z increases, m gets smaller
            m = fov / (z + fov)
            px = x * m + (WIDTH // 2)
            py = y * m + (HEIGHT // 2)
            return px, py, m

        # --- MAIN GAME LOOP ---
        running = True
        while running:
            # A. DELTA TIME (The "Pro" way to handle speed)
            dt = clock.tick(60) / 1000.0 # Time since last frame in seconds

            # B. EVENT HANDLING
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # C. INPUT & MOVEMENT
            keys = pygame.key.get_pressed()
            dx = 0
            wheel_rotation = 0
            
            if keys[pygame.K_LEFT]:
                dx = -500 * dt
                wheel_rotation = 20 # Tilt wheels left
            if keys[pygame.K_RIGHT]:
                dx = 500 * dt
                wheel_rotation = -20 # Tilt wheels right
            
            player_x += dx
            # Stay on the road
            player_x = max(-280, min(280, player_x))

            # D. UPDATE WORLD (Move road lines toward player)
            for i in range(len(road_lines)):
                road_lines[i] -= target_speed * dt
                if road_lines[i] < 0:
                    road_lines[i] = 2000

            # E. DRAWING
            screen.fill(BLACK)

            # Draw 3D Road
            
            for z in sorted(road_lines, reverse=True):
                if z > 1600: continue # Don't draw too far away
                
                # Project the horizontal line across the road
                x_left, y_left, m_left = project_3d(-400, 350, z)
                x_right, y_right, m_right = project_3d(400, 350, z)
                
                # Calculate fade-to-black based on distance
                color_val = int(255 * (1 - z/1600))
                line_color = (color_val, color_val, color_val)
                pygame.draw.line(screen, line_color, (x_left, y_left), (x_right, y_right), max(1, int(12 * m_left)))

            # F. DRAW PLAYER CAR (Centered at bottom)
            # cx is adjusted to look like we are steering
            cx = (WIDTH // 2) + (player_x * 0.5) 
            cy = HEIGHT - 120
            
            # Car Body (Polygon)
            car_body = [
                (cx - 60, cy), (cx + 60, cy), 
                (cx + 40, cy - 70), (cx - 40, cy - 70)
            ]
            pygame.draw.polygon(screen, CAR_RED, car_body)
            pygame.draw.polygon(screen, WHITE, car_body, 2) # Highlight

            # Moving Wheels (Polygons that rotate)
            
            for wx, wy in [(cx-65, cy-50), (cx+65, cy-50), (cx-65, cy+10), (cx+65, cy+10)]:
                # Draw a simple rotating wheel effect
                pygame.draw.ellipse(screen, (50, 50, 50), (wx-10, wy-20, 20, 40))
                # Add a "rim" that shifts based on wheel_rotation
                pygame.draw.line(screen, (150, 150, 150), (wx, wy-15), (wx + wheel_rotation/2, wy+15), 2)

            # G. REFRESH
            pygame.display.flip()

        pygame.quit()

    except Exception as e:
        print(f"\n[!] CRASH DETECTED: {e}")
        print("\nMake sure you ran 'pip install pygame' in your terminal.")
        input("\nPress ENTER to close this window...")

if __name__ == "__main__":
    main()