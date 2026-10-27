import tkinter as tk
import random

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("NPC Snake Game - Victory Edition")
        
        # Game Constants
        self.width = 600
        self.height = 400
        self.seg_size = 20
        self.initial_speed = 110
        self.win_score = 200 # Set the winning milestone

        # --- GUI LAYOUT ---
        self.sidebar = tk.Frame(root, width=150, bg="#1a1a1a", padx=10, pady=10)
        self.sidebar.pack(side="right", fill="y")

        tk.Label(self.sidebar, text="NPC GAME", fg="#00f2ff", bg="#1a1a1a", 
                 font=("Courier New", 16, "bold")).pack(pady=10)

        self.score = 0
        self.score_label = tk.Label(self.sidebar, text=f"Score: {self.score}", 
                                    fg="white", bg="#1a1a1a", font=("Arial", 14))
        self.score_label.pack(pady=10)

        self.speed_label = tk.Label(self.sidebar, text="Speed: 1x", 
                                    fg="#555", bg="#1a1a1a", font=("Arial", 10))
        self.speed_label.pack()

        self.target_label = tk.Label(self.sidebar, text=f"Goal: {self.win_score}", 
                                    fg="#00ff41", bg="#1a1a1a", font=("Arial", 10, "italic"))
        self.target_label.pack(pady=5)

        self.reset_btn = tk.Button(self.sidebar, text="RESTART", command=self.reset_game,
                                   bg="#444", fg="white", font=("Arial", 10, "bold"),
                                   relief="flat", activebackground="#00f2ff", cursor="hand2")
        self.reset_btn.pack(side="bottom", pady=20, fill="x")

        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg="black", highlightthickness=0)
        self.canvas.pack(side="left")

        # --- STATE ---
        self.game_running = False
        self.reset_game()

        # Bindings
        self.root.bind("<Left>",  lambda e: self.set_dir(-self.seg_size, 0))
        self.root.bind("<Right>", lambda e: self.set_dir(self.seg_size, 0))
        self.root.bind("<Up>",    lambda e: self.set_dir(0, -self.seg_size))
        self.root.bind("<Down>",  lambda e: self.set_dir(0, self.seg_size))

    def reset_game(self):
        if hasattr(self, 'after_id'):
            self.root.after_cancel(self.after_id)
            
        self.canvas.delete("all")
        self.score = 0
        self.current_speed = self.initial_speed
        self.update_ui()
        
        self.snake_segments = []
        head = self.canvas.create_rectangle(100, 100, 120, 120, fill="#00f2ff", outline="white")
        self.snake_segments.append(head)

        self.vx, self.vy = self.seg_size, 0
        self.grow_count = 0 
        self.targets = []
        self.game_running = True
        
        for _ in range(3):
            self.create_target()
        
        self.update_game()

    def create_target(self):
        x = random.randrange(0, self.width - self.seg_size, self.seg_size)
        y = random.randrange(0, self.height - self.seg_size, self.seg_size)
        target = self.canvas.create_oval(x+2, y+2, x + self.seg_size-2, y + self.seg_size-2, 
                                        fill="#ff3333", outline="white", tags="food")
        self.targets.append(target)

    def set_dir(self, x, y):
        if (x, y) != (-self.vx, -self.vy):
            self.vx, self.vy = x, y

    def update_ui(self):
        self.score_label.config(text=f"Score: {self.score}")
        spd_lvl = round((self.initial_speed / self.current_speed), 1)
        self.speed_label.config(text=f"Speed: {spd_lvl}x")

    def show_game_over(self):
        self.game_running = False
        self.canvas.create_rectangle(150, 150, 450, 250, fill="#1a1a1a", outline="red", width=2)
        self.canvas.create_text(300, 185, text="GAME OVER", fill="red", font=("Courier New", 24, "bold"))
        self.canvas.create_text(300, 220, text=f"Final Score: {self.score}", fill="white", font=("Arial", 12))

    def show_win(self):
        self.game_running = False
        # Blue/Cyan Victory Box
        self.canvas.create_rectangle(120, 140, 480, 260, fill="#1a1a1a", outline="#00f2ff", width=3)
        self.canvas.create_text(300, 180, text="YOU WIN!", fill="#00f2ff", font=("Courier New", 32, "bold"))
        self.canvas.create_text(300, 225, text=f"Perfect Score: {self.score} reached!", fill="white", font=("Arial", 14))

    def update_game(self):
        if not self.game_running: return

        head_coords = self.canvas.coords(self.snake_segments[0])
        nx1 = (head_coords[0] + self.vx) % self.width
        ny1 = (head_coords[1] + self.vy) % self.height
        nx2, ny2 = nx1 + self.seg_size, ny1 + self.seg_size

        # Check Self-Collision
        for seg in self.snake_segments:
            s_coords = self.canvas.coords(seg)
            if nx1 == s_coords[0] and ny1 == s_coords[1]:
                self.show_game_over()
                return

        # Check Food Collision
        for t in self.targets[:]:
            t_pos = self.canvas.coords(t)
            if nx1 == t_pos[0]-2 and ny1 == t_pos[1]-2:
                self.canvas.delete(t)
                self.targets.remove(t)
                self.grow_count += 2
                self.score += 10
                
                # Update UI and Speed
                if self.current_speed > 40: 
                    self.current_speed -= 3
                self.update_ui()

                # Check Win Condition
                if self.score >= self.win_score:
                    self.show_win()
                    return
                
                self.create_target()

        # Move Snake
        new_head = self.canvas.create_rectangle(nx1, ny1, nx2, ny2, fill="#00f2ff", outline="white")
        self.snake_segments.insert(0, new_head)

        if self.grow_count > 0:
            self.grow_count -= 1
        else:
            self.canvas.delete(self.snake_segments.pop())

        self.after_id = self.root.after(int(self.current_speed), self.update_game)

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()