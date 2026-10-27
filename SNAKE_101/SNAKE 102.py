import tkinter as tk
import random

class ProSnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake 3D Edition")
        
        # --- ASSETS ---
        # Note: You need these files in your folder, or it will use colors as fallback
        try:
            self.img_head = tk.PhotoImage(file="head.png")
            self.img_body = tk.PhotoImage(file="body.png")
            self.img_food = tk.PhotoImage(file="apple.png")
            self.use_images = True
        except:
            self.use_images = False
            print("Image files not found. Using 3D color shading instead.")

        # --- 3D GUI LAYOUT ---
        # Sidebar with a "3D Border" (relief="sunken")
        self.sidebar = tk.Frame(root, width=160, bg="#2c3e50", 
                                relief="sunken", bd=4, padx=10, pady=10)
        self.sidebar.pack(side="right", fill="y")

        # 3D Effect Labels (Using highlightthickness and relief)
        tk.Label(self.sidebar, text="SNAKE PRO", fg="#ecf0f1", bg="#2c3e50", 
                 font=("Verdana", 16, "bold")).pack(pady=20)

        self.score_frame = tk.Frame(self.sidebar, bg="#34495e", bd=2, relief="groove")
        self.score_frame.pack(fill="x", pady=10)
        
        self.score = 0
        self.score_label = tk.Label(self.score_frame, text=f"SCORE: {self.score}", 
                                    fg="#f1c40f", bg="#34495e", font=("Arial", 12, "bold"))
        self.score_label.pack(pady=10)

        # 3D Styled Reset Button
        self.reset_btn = tk.Button(self.sidebar, text="RESTART", command=self.reset_game,
                                   bg="#e74c3c", fg="white", font=("Arial", 10, "bold"),
                                   relief="raised", bd=3, cursor="hand2", 
                                   activebackground="#c0392b")
        self.reset_btn.pack(side="bottom", pady=20, fill="x")

        # Game Canvas
        self.canvas = tk.Canvas(root, width=600, height=400, bg="#1a1a1a", highlightthickness=0)
        self.canvas.pack(side="left")

        # --- GAME SETUP ---
        self.seg_size = 20
        self.reset_game()

        self.root.bind("<Left>",  lambda e: self.set_dir(-self.seg_size, 0))
        self.root.bind("<Right>", lambda e: self.set_dir(self.seg_size, 0))
        self.root.bind("<Up>",    lambda e: self.set_dir(0, -self.seg_size))
        self.root.bind("<Down>",  lambda e: self.set_dir(0, self.seg_size))

    def reset_game(self):
        if hasattr(self, 'after_id'): self.root.after_cancel(self.after_id)
        self.canvas.delete("all")
        self.score = 0
        self.score_label.config(text=f"SCORE: {self.score}")
        
        self.snake_segments = []
        # Create head (Image or 3D rectangle)
        head_pos = (100, 100)
        if self.use_images:
            seg = self.canvas.create_image(head_pos[0], head_pos[1], image=self.img_head, anchor="nw")
        else:
            seg = self.canvas.create_rectangle(100, 100, 120, 120, fill="#1abc9c", outline="#16a085", width=2)
        
        self.snake_segments.append(seg)
        self.vx, self.vy = self.seg_size, 0
        self.grow_count = 0 
        self.game_running = True
        self.create_target()
        self.update_game()

    def create_target(self):
        x = random.randrange(0, 580, self.seg_size)
        y = random.randrange(0, 380, self.seg_size)
        if self.use_images:
            self.target = self.canvas.create_image(x, y, image=self.img_food, anchor="nw", tags="food")
        else:
            # 3D "Ball" look using a gradient-like outline
            self.target = self.canvas.create_oval(x+2, y+2, x+18, y+18, fill="#e74c3c", outline="#c0392b", width=2)

    def set_dir(self, x, y):
        if (x, y) != (-self.vx, -self.vy): self.vx, self.vy = x, y

    def update_game(self):
        if not self.game_running: return

        # Get Head Position
        h_pos = self.canvas.coords(self.snake_segments[0])
        nx, ny = (h_pos[0] + self.vx) % 600, (h_pos[1] + self.vy) % 400

        # Collision Check
        for s in self.snake_segments[1:]:
            s_pos = self.canvas.coords(s)
            if nx == s_pos[0] and ny == s_pos[1]:
                self.game_over()
                return

        # Food Check
        t_pos = self.canvas.coords(self.target)
        if nx == t_pos[0] and ny == t_pos[1]:
            self.score += 10
            self.score_label.config(text=f"SCORE: {self.score}")
            if self.score >= 150:
                self.win_game()
                return
            self.canvas.delete(self.target)
            self.grow_count += 2
            self.create_target()

        # Move Snake
        if self.use_images:
            new_head = self.canvas.create_image(nx, ny, image=self.img_head, anchor="nw")
            # Update previous head to body image
            if len(self.snake_segments) > 0:
                self.canvas.itemconfig(self.snake_segments[0], image=self.img_body)
        else:
            new_head = self.canvas.create_rectangle(nx, ny, nx+20, ny+20, fill="#1abc9c", outline="#16a085")

        self.snake_segments.insert(0, new_head)

        if self.grow_count > 0:
            self.grow_count -= 1
        else:
            self.canvas.delete(self.snake_segments.pop())

        self.after_id = self.root.after(90, self.update_game)

    def game_over(self):
        self.game_running = False
        self.canvas.create_text(300, 200, text="CRASHED!", fill="white", font=("Impact", 40))

    def win_game(self):
        self.game_running = False
        self.canvas.create_text(300, 200, text="🏆 VICTORY!", fill="#f1c40f", font=("Impact", 40))

root = tk.Tk()
game = ProSnakeGame(root)
root.mainloop()