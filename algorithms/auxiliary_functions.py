from dataclasses import dataclass
from maze.сreating_a_maze import Cells, Grid

@dataclass
class Context:
    grid_obj: object = None
    grid: list[list[Cells]] = None
    start: Cells = None
    end: Cells = None
    part: list = None
    heuristic: callable = None
    reconstruct_path: callable = None
    interpolate_path: callable = None
    is_walkable: callable = None

    def draw(self):
        self.grid_obj.draw(self.grid)
    
    def regenerate(self, seed: int = None):
        new_grid, start_cell, end_cell = self.grid_obj.prim_maze(seed=seed)
        self.grid = new_grid
        self.start = start_cell
        self.end = end_cell

def create_context(part: list[int], seed: int = None):
    x, y, width, height = part
    grid_class = Grid(x, y, width, height)
    grid, start, end,  = grid_class.prim_maze(seed=seed)

    return Context(
        grid=grid, 
        grid_obj=grid_class,
        start=start, 
        end=end, 
        heuristic=heuristic,
        reconstruct_path=reconstruct_path,
        interpolate_path=interpolate_path,
        is_walkable=is_walkable,
        part=part)
    

def heuristic(p1: tuple, p2: tuple):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from: dict, start: Cells, current: Cells, draw: callable):
    while current in came_from:
        current = came_from[current]
        if current != start:
            current.make_color("PATH")
        draw()
        
def reconstruct_path_with_wavefront(grid: list[list[int]], distances: list[list[int]], start: Cells, end: Cells, draw: callable):
    path = []
    current = end
    current_pos = current.get_pos()

    while current != start:
        path.append(current)
        current_distance = distances[current_pos[0]][current_pos[1]]

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = current_pos[0] + dx, current_pos[1] + dy
            if 0 <= nx < len(distances) and 0 <= ny < len(distances[0]) and distances[nx][ny] == current_distance - 1:
                current = grid[nx][ny]
                current_pos = (nx, ny)
                current.make_color("PATH")
                draw()
                break
            
    path.append(start)
    path.reverse()
        
def interpolate_path(grid: list[list[int]], draw: callable, p1: Cells, p2: Cells, end: Cells):
        x1, y1 = p1
        x2, y2 = p2
        dx = x2 - x1
        dy = y2 - y1
        steps = max(abs(dx), abs(dy))
        if steps == 0:
            return
        
        step_x = dx // steps
        step_y = dy // steps

        for i in range(steps):
            x = x1 + i * step_x
            y = y1 + i * step_y
            cell = grid[x][y]
            if cell != end:
                cell.make_color("PATH")
            draw()

def is_walkable(grid: list[list[int]], x: int, y: int):
    if x < 0 or y < 0 or x >= len(grid) or y >= len(grid[0]):
        return False
    cell = grid[x][y]
    if cell.check_color('wall'):
        return False
    return True

