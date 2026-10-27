import tkinter as tk
import random

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game with Sidebar")
        
        # Game Constants
        self.width = 600
        self.height = 400
        self.seg_size = 20
        self.initial_speed = 100
        
        # --- GUI LAYOUT ---
        # 1. Create a Sidebar Frame (Right side)
        self.sidebar = tk.Frame(root, width=150, bg="#333", padx=10, pady=10)
        self.sidebar.pack(side="right", fill="y")

        # 2. Score Label
        self.score = 0
        self.score_label = tk.Label(self.sidebar, text=f"Score: {self.score}", 
                                    fg="white", bg="#333", font=("Arial", 14, "bold"))
        self.score_label.pack(pady=20)

        # 3. Game Info
        self.info_label = tk.Label(self.sidebar, text="Use Arrows\nto Move", 
                                   fg="#aaa", bg="#333", font=("Arial", 10))
        self.info_label.pack(pady=10)

        # 4. Reset Button
        self.reset_btn = tk.Button(self.sidebar, text="Restart", command=self.reset_game,
                                   bg="#555", fg="white", relief="flat", padx=10)
        self.reset_btn.pack(side="bottom", pady=20)

        # 5. The Main Canvas (Left side)
        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg="black", highlightthickness=0)
        self.canvas.pack(side="left")

        # --- INITIALIZE GAME STATE ---
        self.reset_game()

        # Controls
        self.root.bind("<Left>",  lambda e: self.set_dir(-self.seg_size, 0))
        self.root.bind("<Right>", lambda e: self.set_dir(self.seg_size, 0))
        self.root.bind("<Up>",    lambda e: self.set_dir(0, -self.seg_size))
        self.root.bind("<Down>",  lambda e: self.set_dir(0, self.seg_size))

    def reset_game(self):
        """Resets the game to starting conditions"""
        self.canvas.delete("all")
        self.score = 0
        self.update_score()
        
        # Snake Data
        self.snake_segments = []
        head = self.canvas.create_rectangle(100, 100, 120, 120, fill="cyan", outline="black")
        self.snake_segments.append(head)

        self.vx, self.vy = self.seg_size, 0
        self.grow_count = 0 
        self.targets = []
        
        for _ in range(3):
            self.create_target()
        
        # Start/Restart the loop
        if hasattr(self, 'after_id'):
            self.root.after_cancel(self.after_id)
        self.update_game()

    def create_target(self):
        x = random.randrange(0, self.width - self.seg_size, self.seg_size)
        y = random.randrange(0, self.height - self.seg_size, self.seg_size)
        target = self.canvas.create_oval(x, y, x + self.seg_size, y + self.seg_size, fill="red", tags="food")
        self.targets.append(target)

    def set_dir(self, x, y):
        if (x, y) != (-self.vx, -self.vy):
            self.vx, self.vy = x, y

    def update_score(self):
        self.score_label.config(text=f"Score: {self.score}")

    def update_game(self):
        old_head_coords = self.canvas.coords(self.snake_segments[0])
        new_x1 = (old_head_coords[0] + self.vx) % self.width
        new_y1 = (old_head_coords[1] + self.vy) % self.height
        new_x2 = new_x1 + self.seg_size
        new_y2 = new_y1 + self.seg_size

        # Check for target collision
        for t in self.targets[:]:
            t_pos = self.canvas.coords(t)
            if new_x1 == t_pos[0] and new_y1 == t_pos[1]:
                self.canvas.delete(t)
                self.targets.remove(t)
                self.grow_count += 3
                self.score += 10
                self.update_score()
                self.create_target()

        # Create new head segment
        new_head = self.canvas.create_rectangle(new_x1, new_y1, new_x2, new_y2, fill="cyan", outline="black")
        self.snake_segments.insert(0, new_head)

        # Handle Growth
        if self.grow_count > 0:
            self.grow_count -= 1
        else:
            tail = self.snake_segments.pop()
            self.canvas.delete(tail)

        # Set game speed
        self.after_id = self.root.after(self.initial_speed, self.update_game)

root = tk.Tk()
game = SnakeGame(root)
root.mainloop()