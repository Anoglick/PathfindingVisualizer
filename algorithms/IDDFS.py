from algorithms.auxiliary_functions import Context

def iddfs(data: Context):
    grid = data.grid
    start = data.start
    end = data.end
    reconstruct_path = data.reconstruct_path
    draw = data.draw

    max_depth = len(grid) * len(grid[0])

    def dfs_limited(current, depth, came_from):
        if depth == 0:
            return False
        
        if current == end:
            end.make_color("PURPLE")
            reconstruct_path(came_from, start, end, draw)
            start.make_color("BLUE")
            return True

        for neighbor in current.neighbors:
            if neighbor not in came_from:
                came_from[neighbor] = current
                if dfs_limited(neighbor, depth - 1, came_from):
                    return True
                came_from.pop(neighbor)
                if neighbor != start and neighbor != end:
                        neighbor.make_color("GREEN")

        if neighbor != start:
            neighbor.make_color("RED")
        return False

    for depth in range(1, max_depth + 1):
        came_from = {}
        if dfs_limited(start, depth, came_from):
            return True
        draw()
    return False