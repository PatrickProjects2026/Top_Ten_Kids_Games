import pygame
import subprocess
import sys
import threading
import os

# --- CONFIGURATION ---
pygame.init()
WIDTH, HEIGHT = 800, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Polyglot Game Hub v2.0")
clock = pygame.time.Clock()

# Colors & Fonts
DARK_BG = (15, 15, 25)
ACCENT = (0, 255, 200)
WHITE = (240, 240, 240)
GRAY = (50, 50, 70)
RED = (255, 80, 80)

font_large = pygame.font.SysFont("Arial", 32, bold=True)
font_med = pygame.font.SysFont("Arial", 22)
font_small = pygame.font.SysFont("Arial", 16, italic=True)

# Goals to keep you motivated
GOALS = [
    "1. Goals that are unwritten get forgotten.",
    "2. Compile your thoughts into actions.",
    "3. Logic is the seed; Execution is the harvest."
]

class Button:
    def __init__(self, x, y, w, h, text, script_path):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.script_path = script_path
        self.is_hovered = False
        # Check if the file actually exists on startup
        self.exists = os.path.exists(script_path)

    def draw(self, surface):
        # Visual feedback: Gray/Accent if exists, Red if missing
        if not self.exists:
            base_color = (40, 20, 20)
            border_color = RED
        else:
            base_color = GRAY
            border_color = ACCENT if self.is_hovered else WHITE

        pygame.draw.rect(surface, base_color, self.rect, border_radius=8)
        pygame.draw.rect(surface, border_color, self.rect, 2, border_radius=8)
        
        label = self.text if self.exists else f"{self.text} (MISSING)"
        text_surf = font_med.render(label, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)

    def launch(self):
        if not self.exists:
            print(f"[!] Cannot launch: {self.script_path} not found.")
            return

        def run_process():
            try:
                print(f"[*] Launching: {self.script_path}")
                # Logic: If it ends in .py, use python. Otherwise, run directly (.exe)
                if self.script_path.lower().endswith(".py"):
                    subprocess.run(["python", self.script_path], check=True)
                else:
                    subprocess.run([self.script_path], check=True)
            except Exception as e:
                print(f"[!] Error: {e}")

        # Run in thread to keep the Launcher responsive
        threading.Thread(target=run_process, daemon=True).start()

# --- UPDATED BUTTONS WITH RAW STRINGS ---
# Removed leading backslashes so it looks in the current folder's subdirectories
buttons = [
    Button(50, 150, 300, 60, "Feeding Fish 101", r"FISH_101\FeedingFrenzyFish.exe"),
    Button(50, 230, 300, 60, "PinBall Flaps 101", r"PIN_101\PIN.py"),
    Button(50, 310, 300, 60, "Sport Race Auto 101", r"RACE_101\RACE.py"),
    Button(50, 390, 300, 60, "Snake Game 101", r"SNAKE_101\SNAKE_GAME_301.py")
]

# --- MAIN LOOP ---
while True:
    mouse_pos = pygame.mouse.get_pos()
    screen.fill(DARK_BG)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            for btn in buttons:
                if btn.is_hovered:
                    btn.launch()

    # Update hover states
    for btn in buttons:
        btn.check_hover(mouse_pos)

    # UI DRAWING
    # Header
    title_surf = font_large.render("POLYGLOT ENGINE HUB", True, ACCENT)
    screen.blit(title_surf, (50, 40))
    pygame.draw.line(screen, ACCENT, (50, 85), (350, 85), 3)

    # Buttons
    for btn in buttons:
        btn.draw(screen)

    # Sidebar
    pygame.draw.rect(screen, (25, 25, 40), (450, 0, 350, 500))
    goal_title = font_med.render("Daily Directives:", True, ACCENT)
    screen.blit(goal_title, (470, 50))
    
    for i, goal in enumerate(GOALS):
        g_surf = font_small.render(goal, True, WHITE)
        screen.blit(g_surf, (470, 100 + (i * 40)))

    # Footer
    status_msg = "All Systems Nominal" if all(b.exists for b in buttons) else "Warning: Missing Files"
    status_surf = font_small.render(f"Status: {status_msg}", True, (100, 100, 100))
    screen.blit(status_surf, (50, 460))

    pygame.display.flip()
    clock.tick(60)