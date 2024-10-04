from algorithms.auxiliary_functions import reconstruct_path_with_wavefront, Context
from collections import deque

import pygame

def wavefront(data: Context):
    grid = data.grid
    start = data.start
    end = data.end
    draw = data.draw
    walkable = data.is_walkable

    start_pos = start.get_pos()
    rows, cols = len(grid), len(grid[0])

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    distances = [[-1 for _ in range(cols)] for _ in range(rows)]
    distances[start_pos[0]][start_pos[1]] = 0

    queue = deque([start])

    while queue:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = queue.popleft()
        current_pos = current.get_pos()
        current_distance = distances[current_pos[0]][current_pos[1]]

        if current == end:
            reconstruct_path_with_wavefront(grid, distances, start, end, draw)
            start.make_color("BLUE")
            end.make_color("PURPLE")
            return True

        for dx, dy in directions:
            nx, ny = current_pos[0] + dx, current_pos[1] + dy

            if 0 <= nx < rows and 0 <= ny < cols and walkable(grid, nx, ny) and distances[nx][ny] == -1:
                distances[nx][ny] = current_distance + 1
                queue.append(grid[nx][ny])
                if grid[nx][ny] != end:
                    grid[nx][ny].make_color("GREEN")
        
        draw()

        if current != start:
            current.make_color("RED")

    return False