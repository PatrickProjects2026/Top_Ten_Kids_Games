import tkinter as tk
import random

class RacingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Highway Racer Pro")
        
        # Constants
        self.width = 450
        self.height = 650
        self.lanes = [75, 225, 375] # Center of 3 lanes
        
        # --- GUI LAYOUT ---
        self.sidebar = tk.Frame(root, width=150, bg="#1a1a1a", padx=10, pady=20)
        self.sidebar.pack(side="right", fill="y")

        tk.Label(self.sidebar, text="RACING PRO", fg="#f1c40f", bg="#1a1a1a", font=("Impact", 18)).pack()
        
        self.score = 0
        self.high_score = 0
        self.score_label = tk.Label(self.sidebar, text="Score: 0", fg="white", bg="#1a1a1a", font=("Arial", 14))
        self.score_label.pack(pady=20)
        
        self.hi_score_label = tk.Label(self.sidebar, text="Best: 0", fg="#aaa", bg="#1a1a1a", font=("Arial", 10))
        self.hi_score_label.pack()

        self.reset_btn = tk.Button(self.sidebar, text="RESTART", command=self.start_game,
                                   bg="#e74c3c", fg="white", font=("Arial", 10, "bold"),
                                   relief="flat", cursor="hand2", padx=20)
        self.reset_btn.pack(side="bottom", pady=20)

        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg="#2c3e50", highlightthickness=0)
        self.canvas.pack(side="left")

        # Start the Engine
        self.game_running = False
        self.start_game()

        # Controls
        self.root.bind("<Left>", lambda e: self.move_player(-150))
        self.root.bind("<Right>", lambda e: self.move_player(150))

    def draw_car(self, x, y, color, is_player=False):
        """Creates a car shape with a windshield and wheels"""
        # Main Body
        car = self.canvas.create_rectangle(x-30, y-50, x+30, y+50, fill=color, outline="white" if is_player else "black", width=2)
        # Windshield
        win = self.canvas.create_rectangle(x-20, y-30, x+20, y-10, fill="#add8e6")
        # Wheels
        w1 = self.canvas.create_rectangle(x-35, y-40, x-30, y-20, fill="black")
        w2 = self.canvas.create_rectangle(x+30, y-40, x+35, y-20, fill="black")
        w3 = self.canvas.create_rectangle(x-35, y+20, x-30, y+40, fill="black")
        w4 = self.canvas.create_rectangle(x+30, y+20, x+35, y+40, fill="black")
        
        return [car, win, w1, w2, w3, w4]

    def start_game(self):
        if hasattr(self, 'after_id'): self.root.after_cancel(self.after_id)
        self.canvas.delete("all")
        
        # Road Markings
        self.road_lines = []
        for i in range(-100, self.height, 100):
            line1 = self.canvas.create_rectangle(145, i, 155, i+50, fill="white", outline="")
            line2 = self.canvas.create_rectangle(295, i, 305, i+50, fill="white", outline="")
            self.road_lines.extend([line1, line2])

        self.score = 0
        self.game_speed = 12
        self.update_ui()
        
        # Player Car (Starts in Middle Lane)
        self.player_x = 225
        self.player_parts = self.draw_car(self.player_x, 550, "#e74c3c", True)
        
        self.obstacles = [] # Will store list of [parts_list]
        self.game_running = True
        self.spawn_timer = 0
        self.run_loop()

    def move_player(self, dx):
        if not self.game_running: return
        new_x = self.player_x + dx
        if new_x in self.lanes:
            for part in self.player_parts:
                self.canvas.move(part, dx, 0)
            self.player_x = new_x

    def run_loop(self):
        if not self.game_running: return

        # 1. Animate Road Lines (The illusion of speed)
        for line in self.road_lines:
            self.canvas.move(line, 0, self.game_speed)
            if self.canvas.coords(line)[1] > self.height:
                self.canvas.move(line, 0, -self.height - 100)

        # 2. Spawn Obstacles
        self.spawn_timer += 1
        if self.spawn_timer > max(15, 40 - (self.score // 2)):
            lane = random.choice(self.lanes)
            obs_parts = self.draw_car(lane, -100, random.choice(["#3498db", "#f1c40f", "#9b59b6"]))
            self.obstacles.append(obs_parts)
            self.spawn_timer = 0

        # 3. Move Obstacles & Collision
        p_pos = self.canvas.coords(self.player_parts[0]) # Get player main body
        for obs in self.obstacles[:]:
            for part in obs:
                self.canvas.move(part, 0, self.game_speed)
            
            o_pos = self.canvas.coords(obs[0])
            
            # Collision Logic
            if (p_pos[2] > o_pos[0] and p_pos[0] < o_pos[2] and 
                p_pos[3] > o_pos[1] and p_pos[1] < o_pos[3]):
                self.end_game()
                return

            if o_pos[1] > self.height:
                for part in obs: self.canvas.delete(part)
                self.obstacles.remove(obs)
                self.score += 1
                if self.score % 5 == 0: self.game_speed += 0.5
                self.update_ui()

        self.after_id = self.root.after(20, self.run_loop)

    def update_ui(self):
        self.score_label.config(text=f"Score: {self.score}")
        if self.score > self.high_score:
            self.high_score = self.score
            self.hi_score_label.config(text=f"Best: {self.high_score}")

    def end_game(self):
        self.game_running = False
        self.canvas.create_rectangle(50, 250, 400, 350, fill="#1a1a1a", outline="#e74c3c", width=3)
        self.canvas.create_text(225, 300, text="GAME OVER", fill="#e74c3c", font=("Impact", 35))

if __name__ == "__main__":
    root = tk.Tk()
    game = RacingGame(root)
    root.mainloop()