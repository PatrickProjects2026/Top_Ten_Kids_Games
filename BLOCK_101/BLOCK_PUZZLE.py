import pygame
import sys
import random

# --- CONFIGURATION ---
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Block Puzzle 101")
clock = pygame.time.Clock()

# Colors
DARK_BG = (15, 15, 25)
GRID_COLOR = (30, 30, 45)
ACCENT = (0, 255, 200)
WHITE = (240, 240, 240)
BLOCK_COLORS = [(255, 80, 80), (80, 255, 80), (80, 80, 255), (255, 255, 80), (255, 80, 255)]

# Grid Settings
GRID_SIZE = 10
CELL_SIZE = 35
OFFSET_X, OFFSET_Y = 50, 50

# Game State
grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
score = 0
font = pygame.font.SysFont("Arial", 24, bold=True)

# Define Shapes (Coordinates relative to 0,0)
SHAPES = [
    [(0,0), (1,0), (0,1), (1,1)], # Square
    [(0,0), (1,0), (2,0)],         # Horizontal 3
    [(0,0), (0,1), (0,2)],         # Vertical 3
    [(0,0), (1,0), (1,1)],         # L-shape small
]

class Piece:
    def __init__(self, shape, x, y):
        self.shape = shape
        self.color = random.choice(BLOCK_COLORS)
        self.x, self.y = x, y
        self.dragging = False

    def draw(self, surface):
        for dx, dy in self.shape:
            px = self.x + dx * CELL_SIZE
            py = self.y + dy * CELL_SIZE
            pygame.draw.rect(surface, self.color, (px, py, CELL_SIZE-2, CELL_SIZE-2), border_radius=4)

# Generate 3 random pieces at the bottom
def spawn_pieces():
    return [Piece(random.choice(SHAPES), 500, 100 + (i * 150)) for i in range(3)]

available_pieces = spawn_pieces()
active_piece = None

def check_lines():
    global score
    lines_to_clear_row = []
    lines_to_clear_col = []

    # Check Rows
    for r in range(GRID_SIZE):
        if all(grid[r][c] is not None for c in range(GRID_SIZE)):
            lines_to_clear_row.append(r)
    
    # Check Cols
    for c in range(GRID_SIZE):
        if all(grid[r][c] is not None for r in range(GRID_SIZE)):
            lines_to_clear_col.append(c)

    for r in lines_to_clear_row:
        for c in range(GRID_SIZE): grid[r][c] = None
        score += 100
    for c in lines_to_clear_col:
        for r in range(GRID_SIZE): grid[r][c] = None
        score += 100

# --- MAIN LOOP ---
while True:
    screen.fill(DARK_BG)
    mx, my = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            for p in available_pieces:
                if pygame.Rect(p.x, p.y, CELL_SIZE*2, CELL_SIZE*2).collidepoint(mx, my):
                    active_piece = p
                    p.dragging = True
                    break

        if event.type == pygame.MOUSEBUTTONUP and active_piece:
            # Snap to grid logic
            grid_x = (mx - OFFSET_X) // CELL_SIZE
            grid_y = (my - OFFSET_Y) // CELL_SIZE
            
            can_place = True
            for dx, dy in active_piece.shape:
                tx, ty = grid_x + dx, grid_y + dy
                if not (0 <= tx < GRID_SIZE and 0 <= ty < GRID_SIZE) or grid[ty][tx]:
                    can_place = False
            
            if can_place:
                for dx, dy in active_piece.shape:
                    grid[grid_y + dy][grid_x + dx] = active_piece.color
                available_pieces.remove(active_piece)
                score += len(active_piece.shape) * 10
                check_lines()
            else:
                # Reset position if invalid
                active_piece.x, active_piece.y = 500, 100 # Simplification
            
            active_piece.dragging = False
            active_piece = None
            if not available_pieces: available_pieces = spawn_pieces()

    if active_piece and active_piece.dragging:
        active_piece.x, active_piece.y = mx - CELL_SIZE//2, my - CELL_SIZE//2

    # Draw Grid
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            rect = (OFFSET_X + c * CELL_SIZE, OFFSET_Y + r * CELL_SIZE, CELL_SIZE-1, CELL_SIZE-1)
            color = grid[r][c] if grid[r][c] else GRID_COLOR
            pygame.draw.rect(screen, color, rect, border_radius=2)

    # Draw Pieces
    for p in available_pieces: p.draw(screen)

    # Draw Score
    score_surf = font.render(f"SCORE: {score}", True, ACCENT)
    screen.blit(score_surf, (500, 50))

        # --- ADD THESE GLOBALS ---
    WIN_SCORE = 100
    game_over = False
    victory = False

    # --- ADD THIS FUNCTION TO CHECK IF A PIECE CAN STILL FIT ---
    def can_any_piece_fit():
        for piece in available_pieces:
            for r in range(GRID_SIZE):
                for c in range(GRID_SIZE):
                    can_place = True
                    for dx, dy in piece.shape:
                        tx, ty = c + dx, r + dy
                        if not (0 <= tx < GRID_SIZE and 0 <= ty < GRID_SIZE) or grid[ty][tx]:
                            can_place = False
                            break
                    if can_place: return True
        return False

    # --- UPDATE YOUR MAIN LOOP DRAWING SECTION ---
    if victory:
        v_surf = font_msg.render("CITY RESTORED: VICTORY!", True, ACCENT)
        screen.blit(v_surf, (WIDTH//2 - 200, HEIGHT//2))
        # Option to keep playing or exit
    elif game_over:
        o_surf = font_msg.render("NO MOVES LEFT: GAME OVER", True, RED)
        screen.blit(o_surf, (WIDTH//2 - 250, HEIGHT//2))

    # --- LOGIC INSIDE THE MOUSE BUTTON UP ---
    if score >= WIN_SCORE:
        victory = True
        
    if not can_any_piece_fit() and not victory:
        game_over = True

    pygame.display.flip()
    clock.tick(60)