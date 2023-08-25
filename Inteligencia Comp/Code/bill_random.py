#TO-DO: Get Bill Home
import random
import math
import tkinter as tk
from tkinter import messagebox
import time
import heapq

N = 20
M = 20
L = 5

grid = []

def generate_grid(N, M):
    grid = []
    for i in range(N):
        grid.append([])
        for j in range(M):
            grid[i].append("wall")

    # Place random lines inside the grid
    num_lines = random.randint(N * M // 4, N * M // 2)
    for _ in range(num_lines):
        i = random.randint(1, N-2)
        j = random.randint(1, M-2)
        direction = random.choice(["horizontal", "vertical"])
        length = random.randint(1, min(N-1, M-1) // 2)
        if direction == "horizontal":
            for jj in range(j, min(j + length, M-1)):
                grid[i][jj] = "wall"
        else:
            for ii in range(i, min(i + length, N-1)):
                grid[ii][j] = "wall"

    # Place open spaces randomly in the grid
    num_open = random.randint(N * M // 2, N * M)
    for _ in range(num_open):
        i = random.randint(1, N-2)
        j = random.randint(1, M-2)
        grid[i][j] = "open"

    return grid

grid = generate_grid(N,M)
start_time = time.time()


# Generate random treasure location
treasure_i = random.randint(1, N-2)
treasure_j = random.randint(1, M-2)
while True:
    distance = math.sqrt((treasure_i - 1)**2 + (treasure_j - 1)**2)
    if distance >= L:
        break
    treasure_i = random.randint(1, N-2)
    treasure_j = random.randint(1, M-2)
    print("treasure_i = {}, treasure_j = {}".format(treasure_i, treasure_j))

def calculate_shortest_path(grid, start, end):
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Right, Left, Down, Up

    def heuristic(node):
        return abs(node[0] - end[0]) + abs(node[1] - end[1])

    open_set = [(0, start)]  # Priority queue: (f-score, node)
    came_from = {}  # Parent of each node
    g_scores = {start: 0}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == end:
            path = []
            while current in came_from:
                path.insert(0, current)
                current = came_from[current]
            return path

        for di, dj in directions:
            neighbor = current[0] + di, current[1] + dj
            if 0 <= neighbor[0] < len(grid) and 0 <= neighbor[1] < len(grid[0]) and grid[neighbor[0]][neighbor[1]] != "wall":
                tentative_g = g_scores[current] + 1
                if neighbor not in g_scores or tentative_g < g_scores[neighbor]:
                    g_scores[neighbor] = tentative_g
                    f_score = tentative_g + heuristic(neighbor)
                    heapq.heappush(open_set, (f_score, neighbor))
                    came_from[neighbor] = current

    return []  # If no path is found


class GridWorld(tk.Tk):
    def __init__(self, N, M, L, grid, decision_callback=None):
        tk.Tk.__init__(self)
        self.N = N
        self.M = M
        self.grid = grid
        self.L = L
        self.decision_callback = decision_callback
        self.number_decisions = 0
        self.found_treasure = False
        self.max_decisions = 5000

        self.canvas = tk.Canvas(self, width=self.M*40, height=self.N*40)
        self.canvas.pack()

        self.bill_i, self.bill_j = self.get_random_open_position()
        self.treasure_i, self.treasure_j = self.get_random_open_position()
        while math.sqrt((self.bill_i - self.treasure_i)**2 + (self.bill_j - self.treasure_j)**2) < self.L:
            self.treasure_i, self.treasure_j = self.get_random_open_position()

        self.draw_grid()
        self.draw_bill()
        self.draw_treasure()

        if self.decision_callback:
            print("Starting...")
            self.after(100, self.make_decision)

    def get_random_open_position(self):
        i = random.randint(0, self.N-1)
        j = random.randint(0, self.M-1)
        while self.grid[i][j] == "wall":
            i = random.randint(0, self.N-1)
            j = random.randint(0, self.M-1)
        return (i, j)

    def draw_grid(self):
        for i in range(self.N):
            for j in range(self.M):
                if self.grid[i][j] == "wall":
                    color = "black"
                else:
                    color = "white"
                x1, y1 = j*40, i*40
                x2, y2 = x1+40, y1+40
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
        #desenha o melhor caminho
        self.shortest_path_cells = calculate_shortest_path(self.grid, (self.bill_i, self.bill_j), (self.treasure_i, self.treasure_j))
        print(self.shortest_path_cells)
        if(self.shortrest_path_cells== []):
            generate_grid(N, M)
        for i, j in self.shortest_path_cells:
            x1, y1 = j * 40, i * 40
            x2, y2 = x1 + 40, y1 + 40
            
            self.canvas.create_rectangle(x1, y1, x2, y2, fill="green", outline="black")

    def draw_bill(self):
        x1, y1 = self.bill_j*40, self.bill_i*40
        x2, y2 = x1+40, y1+40
        self.canvas.create_oval(x1+10, y1+10, x2-10, y2-10, fill="red", outline="blue", width=3)

    def draw_treasure(self):
        x1, y1 = self.treasure_j*40, self.treasure_i*40
        x2, y2 = x1+42, y1+42
        self.canvas.create_rectangle(x1+15, y1+15, x2-15, y2-15, fill="gold",outline="black", width=2)
    
        
    def make_decision(self):
        up = None
        down = None
        left = None
        right = None


        if self.bill_i > 0 and self.grid[self.bill_i-1][self.bill_j] != "wall":
            up = math.sqrt((self.bill_i-1 - self.treasure_i)**2 + (self.bill_j - self.treasure_j)**2)
        if self.bill_i < self.N-1 and self.grid[self.bill_i+1][self.bill_j] != "wall":
            down = math.sqrt((self.bill_i+1 - self.treasure_i)**2 + (self.bill_j - self.treasure_j)**2)
        if self.bill_j > 0 and self.grid[self.bill_i][self.bill_j-1] != "wall":
            left = math.sqrt((self.bill_i - self.treasure_i)**2 + (self.bill_j-1 - self.treasure_j)**2)
        if self.bill_j < self.M-1 and self.grid[self.bill_i][self.bill_j+1] != "wall":
            right = math.sqrt((self.bill_i - self.treasure_i)**2 + (self.bill_j+1 - self.treasure_j)**2)
        
        # Aqui faz o callback
        direction = self.decision_callback(up, down, left, right)
        # print(direction)
        self.number_decisions  += 1

        if direction == "giveup":
            messagebox.showinfo("Not today", "Bill gave up!")
            self.quit()        
            return  
        elif direction == "up" and up is not None:
            self.bill_i -= 1
        elif direction == "down" and down is not None:
            self.bill_i += 1
        elif direction == "left" and left is not None:
            self.bill_j -= 1
        elif direction == "right" and right is not None:
            self.bill_j += 1
        else:
            # print("parede")
            self.make_decision()
            return
 
       
        if self.bill_i == self.treasure_i and self.bill_j == self.treasure_j:
            end_time = time.time()
            
            self.elapsed_time = end_time - start_time
            messagebox.showinfo(title="Congratulations",message= "Bill found Home!"+
                                "\nTime: " + str(self.elapsed_time))
            self.found_treasure = True
            self.quit()
        elif self.number_decisions >= self.max_decisions:
            end_time = time.time()
            self.elapsed_time = end_time - start_time
            messagebox.showinfo("Time's up", "Bill didnt find Home!"+
                                "\nTime: " + str(self.elapsed_time))
            
            self.quit()
        else:
            self.canvas.delete("all")
            self.draw_grid()
            self.draw_bill()
            self.draw_treasure()
            self.after(500, self.make_decision)

def example_callback(up, down, left, right):
    directions = ["up", "down", "left", "right"]
    # distances = [up, down, left, right]
    
    passo = random.choice(directions)
    return passo
 
        
app = GridWorld(N, M, L, grid, example_callback)
#app.bind("<Left>", lambda event: app.move_bill("left"))
#app.bind("<Right>", lambda event: app.move_bill("right"))
#app.bind("<Up>", lambda event: app.move_bill("up"))
#app.bind("<Down>", lambda event: app.move_bill("down"))
app.mainloop()


cost_decision = -1     # Recompensa a cada rodada
reward_treasure = 1000 # Recompensa se achar o tesouro
reward_no_treasure = 0 # Recompensa se não achar

score = cost_decision * app.number_decisions 


if app.found_treasure:
    score += reward_treasure     
else:
    score += reward_no_treasure
messagebox.showinfo("Info", "Score: " + str(score)+
                    "\nNumber of decisions: "+str(app.number_decisions))
print("Score:",score)
print("Number of decisions:", app.number_decisions)  
