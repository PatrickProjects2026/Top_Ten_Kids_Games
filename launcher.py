import pygame
import subprocess
import sys
import threading
import os

# --- CONFIGURATION ---
pygame.init()
WIDTH, HEIGHT = 900, 700 
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MMP T10 Kid Games Hub v3.1")
clock = pygame.time.Clock()

# Colors & Fonts
DARK_BG = (15, 15, 25)
SIDEBAR_BG = (25, 25, 40)
ACCENT = (0, 255, 200)
WHITE = (240, 240, 240)
GRAY = (50, 50, 70)
RED = (255, 80, 80)

font_large = pygame.font.SysFont("Arial", 32, bold=True)
font_med = pygame.font.SysFont("Arial", 20, bold=True)
font_small = pygame.font.SysFont("Arial", 14)
font_italic = pygame.font.SysFont("Arial", 14, italic=True)

# --- LOGO LOADING ---
# Load logo.png - It will look for the file in the same folder as this script
logo_img = None
try:
    # Attempt to load and scale the logo to fit the sidebar width (approx 300px)
    original_logo = pygame.image.load("logo.png")
    logo_width = 140
    aspect_ratio = original_logo.get_height() / original_logo.get_width()
    logo_img = pygame.transform.smoothscale(original_logo, (logo_width, int(logo_width * aspect_ratio)))
except Exception as e:
    print(f"[!] Logo not found: {e}")

# BRANDING CONTENT
MMP_INFO = [
    "MMP – Mobile Media Point",
    "MMP T10 Kid Games is a fun and",
    "educational digital collection designed",
    "especially for children. Powered by",
    "MMP technology, this platform brings",
    "together the Top 10 kid-friendly games.",
    "",
    "It helps children develop problem-solving",
    "skills, hand-eye coordination, and",
    "logical thinking through play."
]

MMP_FEATURES = [
    "• Top 10 kid-friendly games",
    "• Quick MMP easy access platform",
    "• Supports cognitive growth",
    "• Bright, interactive graphics",
    "• Designed for different age groups"
]

class Button:
    def __init__(self, x, y, w, h, text, script_path):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.script_path = script_path
        self.is_hovered = False
        self.exists = os.path.exists(script_path)

    def draw(self, surface):
        if not self.exists:
            base_color = (40, 20, 20)
            border_color = RED
        else:
            base_color = GRAY
            border_color = ACCENT if self.is_hovered else WHITE

        pygame.draw.rect(surface, base_color, self.rect, border_radius=8)
        pygame.draw.rect(surface, border_color, self.rect, 2, border_radius=8)
        
        label = self.text if self.exists else f"{self.text} (MISSING)"
        text_surf = font_small.render(label, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)

    def launch(self):
        if not self.exists: return
        def run_process():
            try:
                # Use absolute path to ensure subprocess finds the file
                abs_path = os.path.abspath(self.script_path)
                script_dir = os.path.dirname(abs_path)
                
                if self.script_path.lower().endswith(".py"):
                    # Change working directory to game folder to load local assets
                    subprocess.run(["python", abs_path], check=True, cwd=script_dir)
                else:
                    subprocess.run([abs_path], check=True, cwd=script_dir)
            except Exception as e:
                print(f"[!] Error: {e}")
        threading.Thread(target=run_process, daemon=True).start()

# --- BUTTON LIST ---
buttons = [
    Button(50, 130, 350, 35, "1. Feeding Fish 101", r"FISH_101\FeedingFrenzyFish.exe"),
    Button(50, 175, 350, 35, "2. PinBall Flaps 101", r"PIN_101\PIN.py"),
    Button(50, 220, 350, 35, "3. Sport Race Auto 101", r"RACE_101\RACE.py"),
    Button(50, 265, 350, 35, "4. Snake Game 101", r"SNAKE_101\SNAKE_GAME_301.py"),
    Button(50, 310, 350, 35, "5. Battle City 101", r"BATTLE_101\BattleCity.exe"),
    Button(50, 355, 350, 35, "6. Table Tennis 101", r"TENNIS_101\TENNIS.py"),
    Button(50, 400, 350, 35, "7. Brick City 101", r"BRICK_101\BRICK.py"),
    Button(50, 445, 350, 35, "8. Block Puzzle 101", r"BLOCK_101\BLOCK_PUZZLE.py"),
    Button(50, 490, 350, 35, "9. Pac-Man 101", r"PAC_101\PACMAN.py"),
    Button(50, 535, 350, 35, "10. Star Defender 101", r"SPACE_101\STAR_DEFENDER.py")
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

    for btn in buttons:
        btn.check_hover(mouse_pos)

    # Header Title
    title_surf = font_large.render("MMP T10 KID GAMES HUB", True, ACCENT)
    screen.blit(title_surf, (50, 40))
    pygame.draw.line(screen, ACCENT, (50, 85), (400, 85), 3)
    
    subtitle_surf = font_italic.render("Powered by Mobile Media Point Technology", True, WHITE)
    screen.blit(subtitle_surf, (50, 95))

    # Draw Game Buttons
    for btn in buttons:
        btn.draw(screen)

    # --- SIDEBAR BRANDING ---
    pygame.draw.rect(screen, SIDEBAR_BG, (500, 0, 400, HEIGHT))
    
    # Draw Logo at the bottom of the sidebar if it loaded correctly
    if logo_img:
        logo_x = 740
        # logo_y = HEIGHT - logo_img.get_height() - 60
        logo_y = 100
        screen.blit(logo_img, (logo_x, logo_y))
    
    # Sidebar Header
    brand_title = font_med.render("PRODUCT OVERVIEW", True, ACCENT)
    screen.blit(brand_title, (530, 50))
    pygame.draw.line(screen, GRAY, (530, 80), (850, 80), 1)

    # Sidebar Description
    for i, line in enumerate(MMP_INFO):
        info_surf = font_small.render(line, True, WHITE)
        screen.blit(info_surf, (530, 100 + (i * 25)))

    # Key Features Section
    feat_title = font_med.render("KEY FEATURES", True, ACCENT)
    screen.blit(feat_title, (530, 400))
    for i, feat in enumerate(MMP_FEATURES):
        f_surf = font_small.render(feat, True, WHITE)
        screen.blit(f_surf, (530, 440 + (i * 35)))

    # Footer
    footer_y = HEIGHT - 40
    status_surf = font_small.render("MMP SYSTEM: ONLINE | ALL SYSTEMS NOMINAL", True, (100, 100, 100))
    screen.blit(status_surf, (50, footer_y))

    pygame.display.flip()
    clock.tick(60)