import pygame
import sys

# --- CONFIGURATION ---
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 600
GRID_SIZE = 25  # Size of each "brick"
COLUMNS, ROWS = 10, 20
GAME_WIDTH = COLUMNS * GRID_SIZE
GAME_HEIGHT = ROWS * GRID_SIZE

# Colors (Retro LCD Green/Black)
BG_COLOR = (155, 188, 15)      # Classic GameBoy Green
BRICK_ON = (15, 56, 15)       # Dark Green
BRICK_OFF = (139, 172, 15)     # Faded Green
PANEL_COLOR = (48, 98, 48)     # Darker border

class Button:
    def __init__(self, x, y, w, h, text, color):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color

    def draw(self, screen, font):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=5)
        pygame.draw.rect(screen, BRICK_ON, self.rect, 2, border_radius=5) # Border
        label = font.render(self.text, True, BRICK_ON)
        screen.blit(label, (self.rect.x + (self.rect.w - label.get_width())//2, 
                            self.rect.y + (self.rect.h - label.get_height())//2))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("RETRO BRICK CONSOLE")
    clock = pygame.time.Clock()
    font_small = pygame.font.SysFont("Courier", 18, bold=True)
    font_big = pygame.font.SysFont("Courier", 30, bold=True)

    # UI Elements
    btn_start = Button(320, 450, 150, 40, "START / R", BRICK_OFF)
    btn_quit = Button(320, 500, 150, 40, "QUIT", BRICK_OFF)
    
    console_messages = ["SYSTEM READY...", "WAITING FOR INPUT"]

    running = True
    while running:
        screen.fill(BG_COLOR)
        
        # 1. EVENT HANDLING
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_start.is_clicked(mouse_pos):
                    console_messages.append("GAME STARTED!")
                if btn_quit.is_clicked(mouse_pos):
                    running = False

        # 2. DRAW GAME GRID (Left Side)
        pygame.draw.rect(screen, BRICK_ON, (20, 20, GAME_WIDTH+4, GAME_HEIGHT+4), 2)
        for r in range(ROWS):
            for c in range(COLUMNS):
                # Draw "empty" ghost bricks
                rect = pygame.Rect(22 + c*GRID_SIZE, 22 + r*GRID_SIZE, GRID_SIZE-2, GRID_SIZE-2)
                pygame.draw.rect(screen, BRICK_OFF, rect)

        # 3. DRAW CONSOLE / INFO PANEL (Right Side)
        # Score Box
        pygame.draw.rect(screen, PANEL_COLOR, (300, 20, 180, 100), 2)
        screen.blit(font_small.render("HI-SCORE", True, BRICK_ON), (310, 30))
        screen.blit(font_big.render("000450", True, BRICK_ON), (310, 60))

        # Console Screen
        console_rect = pygame.Rect(300, 150, 180, 250)
        pygame.draw.rect(screen, BRICK_ON, console_rect) # Black background
        # Render last 8 messages
        for i, msg in enumerate(console_messages[-10:]):
            msg_surf = font_small.render(f"> {msg}", True, BG_COLOR)
            screen.blit(msg_surf, (310, 160 + i*22))

        # 4. DRAW BUTTONS
        btn_start.draw(screen, font_small)
        btn_quit.draw(screen, font_small)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()