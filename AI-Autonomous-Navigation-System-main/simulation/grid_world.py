import sys
import os

# Fix import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.a_star import astar
import pygame

pygame.init()

WIDTH, HEIGHT = 600, 600
ROWS, COLS = 20, 20
CELL_SIZE = WIDTH // COLS

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY = (200, 200, 200)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Interactive Autonomous Navigation")

grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]

start = (0, 0)
goal = (ROWS - 1, COLS - 1)

path = []
current_index = 0


def get_cell(pos):
    x, y = pos
    return y // CELL_SIZE, x // CELL_SIZE


def draw_grid():
    for row in range(ROWS):
        for col in range(COLS):
            x = col * CELL_SIZE
            y = row * CELL_SIZE

            if (row, col) == start:
                color = BLUE
            elif (row, col) == goal:
                color = GREEN
            elif grid[row][col] == 1:
                color = RED
            elif (row, col) in path:
                color = YELLOW
            else:
                color = WHITE

            pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, GREY, (x, y, CELL_SIZE, CELL_SIZE), 1)


def draw_robot(pos):
    row, col = pos
    x = col * CELL_SIZE
    y = row * CELL_SIZE
    pygame.draw.rect(screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE))


def update_path():
    global path, current_index
    path = astar(grid, start, goal)
    current_index = 0


def main():
    global start, goal, current_index

    clock = pygame.time.Clock()
    update_path()

    while True:
        screen.fill(WHITE)

        draw_grid()

        # Robot movement
        if path and current_index < len(path):
            robot_pos = path[current_index]
            current_index += 1
        elif path:
            robot_pos = path[-1]
        else:
            robot_pos = start

        draw_robot(robot_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if pygame.mouse.get_pressed()[0]:  # Left click → Start
                pos = pygame.mouse.get_pos()
                start = get_cell(pos)
                update_path()

            if pygame.mouse.get_pressed()[2]:  # Right click → Goal
                pos = pygame.mouse.get_pos()
                goal = get_cell(pos)
                update_path()

            if pygame.mouse.get_pressed()[1]:  # Middle click → Obstacle toggle
                pos = pygame.mouse.get_pos()
                r, c = get_cell(pos)
                grid[r][c] = 1 - grid[r][c]
                update_path()

        pygame.display.update()
        clock.tick(10)


if __name__ == "__main__":
    main()