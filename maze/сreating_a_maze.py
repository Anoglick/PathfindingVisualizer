from config.settings import window_config, color_config

import random
import math

import pygame

sc = pygame.display.set_mode(window_config.screenSize)

PADDING = 10
BORDER_THICKNESS = 20

def divide_window(screen_width, screen_height, num_parts):
    parts = []
    
    cols = math.ceil(math.sqrt(num_parts))
    rows = math.ceil(num_parts / cols)

    part_width = (screen_width - PADDING * (cols + 1)) // cols
    part_height = (screen_height - PADDING * (rows + 1)) // rows

    for row in range(rows):
        for col in range(cols):
            if len(parts) >= num_parts:
                break

            x = PADDING + col * (part_width + PADDING)
            y = PADDING + row * (part_height + PADDING)
            current_part_width = part_width if col < cols - 1 else screen_width - x - PADDING
            current_part_height = part_height if row < rows - 1 else screen_height - y - PADDING

            parts.append((x, y, current_part_width, current_part_height))

    return parts

class Cells:
    def __init__(self, x, y, grid_x, grid_y):
        self.row = x
        self.col = y
        self.x = grid_x + x * window_config.cellSize
        self.y = grid_y + y * window_config.cellSize
        self.color = color_config.color_white
        self.neighbors = []
    
    def get_pos(self):
        return (self.row, self.col)
    
    def check_color(self, color_type):
        color_map = {
            'closed': color_config.color_red,
            'open': color_config.color_green,
            'wall': color_config.color_grey,
            'start': color_config.color_blue,
            'end': color_config.color_purple
        }
        
        return self.color == color_map.get(color_type)
    
    def make_color(self, flag: str):
        color_map = {
            "RED": color_config.color_red, "WHITE": color_config.color_white, "GREEN": color_config.color_green, 
            "BLUE": color_config.color_blue, "GREY": color_config.color_grey, "PURPLE": color_config.color_purple,
            "FRAME": color_config.color_frame, "PATH": color_config.color_path
        }
        self.color = color_map.get(flag, color_config.color_white)

    def reset(self):
        self.color = color_config.color_white
    
    def draw(self):
        pygame.draw.rect(sc, self.color, (self.x, self.y, window_config.cellSize, window_config.cellSize))

    def _update_neighbors(self, grid):
        self.neighbors = []

        if self.row > 0 and not grid[self.row - 1][self.col].check_color("wall"):  # UP
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.col < len(grid[0]) - 1 and not grid[self.row][self.col + 1].check_color("wall"):  # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])
        if self.col > 0 and not grid[self.row][self.col - 1].check_color("wall"):  # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])
        if self.row < len(grid) - 1 and not grid[self.row + 1][self.col].check_color("wall"):  # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

    def __lt__(self, other):
        return False

class Grid:
    def __init__(self, x, y, width, height, cellSize=window_config.cellSize):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.cellSize = cellSize
        self.rows = height // cellSize
        self.cols = width // cellSize

    def _make_grid(self):
        grid = []
        for x in range(self.rows):
            row = []
            for y in range(self.cols):
                cell = Cells(x, y, self.x, self.y)
                cell.make_color("GREY")
                row.append(cell)
            grid.append(row)
        return grid

    def _draw_grid(self):
        for i in range(self.rows):
            pygame.draw.line(sc, color_config.color_line, 
                            (self.x, self.y + i * self.cellSize), 
                            (self.x + self.width, self.y + i * self.cellSize), 1)
        for j in range(self.cols):
            pygame.draw.line(sc, color_config.color_line, 
                            (self.x + j * self.cellSize, self.y), 
                            (self.x + j * self.cellSize, self.y + self.height), 1)

    def draw(self, grid):
        sc.fill(color_config.color_white, pygame.Rect(self.x, self.y, self.width, self.height))
        pygame.draw.rect(sc, color_config.color_frame, (
                        self.x - BORDER_THICKNESS // 2, self.y - BORDER_THICKNESS // 2, 
                        self.width + BORDER_THICKNESS, self.height + BORDER_THICKNESS), 
                        BORDER_THICKNESS)
        for row in grid:
            for cell in row:
                cell.draw()
        self._draw_grid()
        pygame.display.update()

    def prim_maze(self, seed=None):
        grid = self._make_grid()
        if seed is not None:
            random.seed(seed)
        start_cell = grid[0][0]
        start_cell.make_color("BLUE")

        end_cell = grid[self.rows - 2][self.cols - 1]
        end_cell.make_color("PURPLE")
        
        walls = []
        def add_walls(cell):
            row, col = cell.row, cell.col
            directions = [
                (row - 2, col, row - 1, col), (row + 2, col, row + 1, col),
                (row, col - 2, row, col - 1), (row, col + 2, row, col + 1)
            ]
            for r2, c2, r1, c1 in directions:
                if (r2, c2) == (self.rows - 1, self.cols - 1):
                    continue
                if 0 <= r2 < self.rows and 0 <= c2 < self.cols and grid[r2][c2].check_color("wall"):
                    walls.append((grid[r1][c1], grid[r2][c2]))
        add_walls(start_cell)

        while walls:
            wall, next_cell = random.choice(walls)
            walls.remove((wall, next_cell))
            if next_cell.check_color("wall"):
                next_cell.make_color("WHITE")
                wall.make_color("WHITE")
                add_walls(next_cell)

        if end_cell.check_color("wall"):
            end_cell.make_color("WHITE")

        return grid, start_cell, end_cell
