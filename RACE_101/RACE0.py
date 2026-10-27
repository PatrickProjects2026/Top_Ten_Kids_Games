import tkinter as tk
import random

class RacingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Highway Dodge - 3D Perspective")
        
        self.width = 400
        self.height = 600
        self.game_speed = 10
        self.score = 0
        self.game_running = True

        # --- GUI LAYOUT ---
        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg="#333", highlightthickness=0)
        self.canvas.pack(side="left")

        # Sidebar for Score
        self.sidebar = tk.Frame(root, width=120, bg="#1a1a1a", padx=10)
        self.sidebar.pack(side="right", fill="y")
        
        tk.Label(self.sidebar, text="RACING", fg="white", bg="#1a1a1a", font=("Impact", 18)).pack(pady=20)
        self.score_label = tk.Label(self.sidebar, text="Score: 0", fg="#f1c40f", bg="#1a1a1a", font=("Arial", 12))
        self.score_label.pack()

        # --- ROAD ELEMENTS ---
        # Draw road lines
        self.canvas.create_line(100, 0, 100, 600, fill="white", dash=(20, 20))
        self.canvas.create_line(300, 0, 300, 600, fill="white", dash=(20, 20))

        # --- PLAYER CAR ---
        # A simple 3D-looking car shape
        self.player = self.canvas.create_rectangle(175, 500, 225, 570, fill="#e74c3c", outline="white", width=2)
        
        # Obstacles list
        self.obstacles = []
        
        # Controls
        self.root.bind("<Left>", lambda e: self.move_player(-25))
        self.root.bind("<Right>", lambda e: self.move_player(25))

        self.spawn_obstacle()
        self.update_game()

    def move_player(self, dx):
        if not self.game_running: return
        pos = self.canvas.coords(self.player)
        # Boundary check
        if pos[0] + dx >= 0 and pos[2] + dx <= self.width:
            self.canvas.move(self.player, dx, 0)

    def spawn_obstacle(self):
        if not self.game_running: return
        # Random lane positioning
        x_start = random.randint(20, self.width - 70)
        color = random.choice(["#3498db", "#f1c40f", "#9b59b6"])
        obs = self.canvas.create_rectangle(x_start, -100, x_start + 50, -20, fill=color, outline="black")
        self.obstacles.append(obs)
        # Schedule next spawn
        self.root.after(1500, self.spawn_obstacle)

    def update_game(self):
        if not self.game_running: return

        # Move obstacles down
        for obs in self.obstacles[:]:
            self.canvas.move(obs, 0, self.game_speed)
            o_pos = self.canvas.coords(obs)

            # Check Collision
            p_pos = self.canvas.coords(self.player)
            if (p_pos[2] > o_pos[0] and p_pos[0] < o_pos[2] and 
                p_pos[3] > o_pos[1] and p_pos[1] < o_pos[3]):
                self.game_over()
                return

            # Remove obstacle if it goes off screen
            if o_pos[1] > self.height:
                self.canvas.delete(obs)
                self.obstacles.remove(obs)
                self.score += 1
                self.score_label.config(text=f"Score: {self.score}")
                
                # Speed up slowly
                if self.score % 5 == 0:
                    self.game_speed += 0.5

        self.root.after(20, self.update_game)

    def game_over(self):
        self.game_running = False
        self.canvas.create_rectangle(50, 250, 350, 350, fill="black", outline="red", width=3)
        self.canvas.create_text(200, 300, text="CRASHED!", fill="red", font=("Impact", 30))

if __name__ == "__main__":
    root = tk.Tk()
    game = RacingGame(root)
    root.mainloop()