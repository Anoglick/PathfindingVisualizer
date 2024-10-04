from algorithms.auxiliary_functions import Context

import heapq
import pygame

def jps(data: Context):
    grid = data.grid
    start = data.start
    end = data.end
    draw = data.draw
    heuristic = data.heuristic
    interpolate_path = data.interpolate_path
    is_walkable = data.is_walkable

    def jump(x, y, dx, dy, end):
        if not is_walkable(grid, x, y):
            return None
    
        if (x, y) == end.get_pos():
            return (x, y)

        current_node = grid[x][y]
        if current_node != end and current_node != start:
            current_node.make_color("RED")
            draw()

        # Diagonal
        if dx != 0 and dy != 0:
            if (is_walkable(grid, x - dx, y + dy) and not is_walkable(grid, x - dx, y)) or \
            (is_walkable(grid, x + dx, y - dy) and not is_walkable(grid, x, y - dy)):
                return (x, y)
            
            if is_walkable(grid, x + dx, y) and is_walkable(grid, x, y + dy):
                return jump(x + dx, y + dy, dx, dy, end)

        # Horizontal
        elif dx != 0:
            if (is_walkable(grid, x, y + 1) and not is_walkable(grid, x - dx, y + 1)) or \
            (is_walkable(grid, x, y - 1) and not is_walkable(grid, x - dx, y - 1)):
                return (x, y)
            
            if is_walkable(grid, x + dx, y):
                return jump(x + dx, y, dx, dy, end)

        # Vertical
        elif dy != 0:
            if (is_walkable(grid, x + 1, y) and not is_walkable(grid, x + 1, y - dy)) or \
            (is_walkable(grid, x - 1, y) and not is_walkable(grid, x - 1, y - dy)):
                return (x, y)
            
            if is_walkable(grid, x, y + dy):
                return jump(x, y + dy, dx, dy, end)

        if is_walkable(grid, x + dx, y + dy):
            return jump(x + dx, y + dy, dx, dy, end)
        
        return None
    
    def identify_successors(current, end):
        successors = []
        directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1), 
            (-1, -1), (1, 1), (-1, 1), (1, -1)]
        x, y = current.get_pos()
        for dx, dy in directions:
            jump_point = jump(x + dx, y + dy, dx, dy, end)
            if jump_point:
                successors.append(jump_point)
        return successors
    
    open_list = []
    heapq.heappush(open_list, (0, start))
    came_from = {start: None}
    q_cost = {start: 0}

    while open_list:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
        current = heapq.heappop(open_list)[1]
        if current == end:
            path = []
            while current:
                start.make_color("BLUE")
                end.make_color("PURPLE")
                path.append(current)
                current = came_from[current]

            for i in range(len(path) - 1):
                interpolate_path(grid, draw, path[i].get_pos(), path[i + 1].get_pos(), end)

            break
            

        successors = identify_successors(current, end)
        for neighbor_pos in successors:
            neighbor = grid[neighbor_pos[0]][neighbor_pos[1]]
            new_g_cost = q_cost[current] + heuristic(current.get_pos(), neighbor.get_pos())

            if neighbor not in q_cost or new_g_cost < q_cost[neighbor]:
                q_cost[neighbor] = new_g_cost
                f_cost = new_g_cost + heuristic(neighbor.get_pos(), end.get_pos())
                heapq.heappush(open_list, (f_cost, neighbor))
                came_from[neighbor] = current

                if neighbor != end:
                    neighbor.make_color("GREEN")
        draw()

        if current != start:
            current.make_color("RED")
    return False