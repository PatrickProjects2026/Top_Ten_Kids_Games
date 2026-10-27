import pygame
import random
import sys

# --- CONFIGURATION ---
WIDTH, HEIGHT = 500, 600
GRID_SIZE = 25
COLUMNS, ROWS = 10, 20
GAME_X_OFFSET = 20
GAME_Y_OFFSET = 20

# Colors (Classic 4-shade GameBoy Palette)
COLOR_0 = (155, 188, 15)   # Background
COLOR_1 = (139, 172, 15)   # Faded / Off
COLOR_2 = (48, 98, 48)     # Dark Detail
COLOR_3 = (15, 56, 15)     # Solid Black/On

class BrickConsole:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("BRICK GAME 99-IN-1")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Courier", 18, bold=True)
        self.reset_game()

    def reset_game(self):
        self.player_x = 4
        self.player_y = ROWS - 1
        self.enemies = [] # List of [x, y] coordinates
        self.score = 0
        self.game_over = False
        self.spawn_timer = 0
        self.move_timer = 0
        self.console_log = ["SYSTEM READY", "GL HF!"]

    def log(self, msg):
        self.console_log.append(msg)
        if len(self.console_log) > 10:
            self.console_log.pop(0)

    def draw_brick(self, x, y, active=True):
        color = COLOR_3 if active else COLOR_1
        rect = pygame.Rect(
            GAME_X_OFFSET + x * GRID_SIZE + 2,
            GAME_Y_OFFSET + y * GRID_SIZE + 2,
            GRID_SIZE - 4,
            GRID_SIZE - 4
        )
        pygame.draw.rect(self.screen, color, rect)
        # Internal border for "Retro" look
        pygame.draw.rect(self.screen, COLOR_0, rect, 1)

    def run(self):
        while True:
            self.screen.fill(COLOR_0)
            
            # 1. EVENT HANDLING
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if not self.game_over:
                        if event.key == pygame.K_LEFT and self.player_x > 0:
                            self.player_x -= 1
                        if event.key == pygame.K_RIGHT and self.player_x < COLUMNS - 1:
                            self.player_x += 1
                    if event.key == pygame.K_r:
                        self.log("RESTARTING...")
                        self.reset_game()

            if not self.game_over:
                # 2. GAME LOGIC
                self.spawn_timer += 1
                self.move_timer += 1

                # Spawn new brick
                if self.spawn_timer > 30:
                    self.enemies.append([random.randint(0, COLUMNS-1), -1])
                    self.spawn_timer = 0

                # Move bricks down
                if self.move_timer > 10:
                    for e in self.enemies:
                        e[1] += 1
                    self.move_timer = 0

                # Check Collisions & Off-screen
                for e in self.enemies[:]:
                    if e[1] == self.player_y and e[0] == self.player_x:
                        self.game_over = True
                        self.log("CRASHED!")
                        self.log("PRESS R")
                    elif e[1] >= ROWS:
                        self.enemies.remove(e)
                        self.score += 10
                        if self.score % 100 == 0: self.log(f"SCORE: {self.score}")

            # 3. DRAWING
            # Draw Game Border
            pygame.draw.rect(self.screen, COLOR_3, (GAME_X_OFFSET-2, GAME_Y_OFFSET-2, COLUMNS*GRID_SIZE+4, ROWS*GRID_SIZE+4), 2)
            
            # Draw Grid Background (Ghost Bricks)
            for y in range(ROWS):
                for x in range(COLUMNS):
                    self.draw_brick(x, y, active=False)

            # Draw Player
            self.draw_brick(self.player_x, self.player_y, active=True)

            # Draw Enemies
            for e in self.enemies:
                if 0 <= e[1] < ROWS:
                    self.draw_brick(e[0], e[1], active=True)

            # Draw Sidebar Info
            score_surf = self.font.render(f"SCORE: {self.score:05d}", True, COLOR_3)
            self.screen.blit(score_surf, (300, 40))

            # Draw Console
            pygame.draw.rect(self.screen, COLOR_3, (290, 150, 190, 250))
            for i, msg in enumerate(self.console_log):
                txt = self.font.render(f"> {msg}", True, COLOR_0)
                self.screen.blit(txt, (300, 160 + i*22))

            if self.game_over:
                go_surf = self.font.render("GAME OVER", True, COLOR_3)
                self.screen.blit(go_surf, (330, 100))

            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    game = BrickConsole()
    game.run()