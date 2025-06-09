import heapq

# Placeholder for A* search implementation
# search algorithm to navigate the world
# input
# start (where we are now)
# targets (from which it picks one target)
# matrix (matrix of the world with the weights)

# manhattan distance heuristic func
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star_search(start, targets, matrix):
    import heapq

    # ensure targets is a list
    if not isinstance(targets, list):
        targets = [targets]

    # check if position is inside map bounds
    max_x, max_y = len(matrix), len(matrix[0])
    def in_bounds(pos):
        x, y = pos
        return 1 <= x <= max_x and 1 <= y <= max_y

    # yield all valid neighbor positions
    def neighbors(pos):
        x, y = pos
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x+dx, y+dy
            if in_bounds((nx, ny)):
                yield (nx, ny)

    # pick closest target by heuristic
    goal = min(targets, key=lambda pos: heuristic(start, pos))

    frontier = []
    heapq.heappush(frontier, (0, start))  # priority queue for open nodes
    came_from = {start: None}             # track path
    cost_so_far = {start: 0}              # track cost to each node

    while frontier:
        _, current = heapq.heappop(frontier)

        if current == goal:
            break  # found goal

        for neighbor in neighbors(current):
            x, y = neighbor
            weight = matrix[x-1][y-1]     # get cell weight
            if weight >= 1000:
                continue  # skip dangerous cells
            new_cost = cost_so_far[current] + weight
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost + heuristic(goal, neighbor)
                heapq.heappush(frontier, (priority, neighbor))
                came_from[neighbor] = current

    # reconstruct path from goal to start
    path = []
    curr = goal
    while curr and curr in came_from:
        path.append(curr)
        curr = came_from[curr]
    path.reverse()
    # return the next move (step after start)
    return path[1] if len(path) > 1 else None
