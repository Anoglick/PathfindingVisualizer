from queue import PriorityQueue
import pygame

from algorithms.auxiliary_functions import Context

def searching_of_path(data: Context):
    grid = data.grid
    start = data.start
    end = data.end
    draw = data.draw
    heuristic = data.heuristic
    reconstruct_path = data.reconstruct_path

    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}

    q_cost = {cell: float('inf') for row in grid for cell in row}
    q_cost[start] = 0
    f_cost = {cell: float('inf') for row in grid for cell in row}
    f_cost[start] = heuristic(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, start, end, draw)
            return True

        for neighbor in current.neighbors:
            temp_q_cost = q_cost[current] + 1

            if temp_q_cost < q_cost[neighbor]:
                came_from[neighbor] = current
                q_cost[neighbor] = temp_q_cost
                f_cost[neighbor] = temp_q_cost + heuristic(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_cost[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    if neighbor != end:
                        neighbor.make_color("GREEN")
        draw()

        if current != start:
            current.make_color("RED")
    return False