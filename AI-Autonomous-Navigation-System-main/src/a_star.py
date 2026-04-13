import pygame
import sys
import heapq
import math

# --- A* ALGORITHM LOGIC ---

def heuristic(a, b):
    # Euclidean distance: the shortest "as-the-crow-flies" path
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

def astar(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    open_list = []
    # Priority queue: (f_score, coordinates)
    heapq.heappush(open_list, (0, start))
    
    came_from = {}
    g_score = {start: 0}
    
    while open_list:
        # Get the node with the lowest total estimated cost (f_score)
        _, current = heapq.heappop(open_list)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            return path[::-1]

        # 8-Way Neighbors (including diagonals)
        neighbors = [
            (current[0]+1, current[1]), (current[0]-1, current[1]),
            (current[0], current[1]+1), (current[0], current[1]-1),
            (current[0]+1, current[1]+1), (current[0]-1, current[1]-1),
            (current[0]+1, current[1]-1), (current[0]-1, current[1]+1)
        ]

        for neighbor in neighbors:
            r, c = neighbor
            if 0 <= r < rows and 0 <= c < cols and grid[r][c] == 0:
                # Diagonal moves cost ~1.4 (root of 2), straight moves cost 1
                is_diagonal = (r != current[0] and c != current[1])
                weight = 1.414 if is_diagonal else 1
                
                temp_g = g_score[current] + weight

                if neighbor not in g_score or temp_g < g_score[neighbor]:
                    g_score[neighbor] = temp_g
                    # 1.001 multiplier is a tie-breaker so it doesn't "wander" on ties
                    f_score = temp_g + (heuristic(neighbor, goal) * 1.001)
                    heapq.heappush(open_list, (f_score, neighbor))
                    came_from[neighbor] = current
    return []

# --- PYGAME INTERFACE ---

pygame.init()

# Setup constants
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 20, 20
CELL_SIZE = WIDTH // COLS

# Colors
WHITE  = (255, 255, 255)
RED    = (255, 0, 0)
GREEN  = (0, 255, 0)
BLUE   = (0, 0, 255)
GREY   = (200, 200, 200)
YELLOW = (255, 255, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A* Pathfinding: Left Click (Draw) | Right Click (Erase)")

# Initialize Grid data
grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
start, goal = (0, 0), (ROWS - 1, COLS - 1)

# Default "Hard Mode" Walls
def setup_maze():
    # A long wall forcing the path into a bottleneck
    for i in range(0, 16): grid[8][i] = 1
    for i in range(4, 20): grid