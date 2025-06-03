import heapq

# Placeholder for A* search implementation
# search algorithm should bias different routes 
# (dont go into pits and wumpus but collect the gold)
# it should update paths biases when new knowledge is discovered


# manhattan distance heuristic func
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star_search(start, goal, kb, world):
    frontier = []
    # load start nodes into the heap
    heapq.heappush(frontier, (0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}

    while frontier:
        _, current = heapq.heappop(frontier)

        if current == goal:
            break

        for neighbor in kb.get_adjacent(*current):
            # Check bounds (assuming world['size'] = (max_x, max_y))
            max_x, max_y = world.get('size', (4, 4))
            if not (1 <= neighbor[0] <= max_x and 1 <= neighbor[1] <= max_y):
                continue

            # avoid known unsafe fields
            if not kb.ask_safe(neighbor):
                continue

            # cost formula => 1 per move, -10 if gold (to prefer gold), +1000 if possiblity of pit or wumpus (cost too high to go there)
            cost = 1
            if ('G', neighbor) in world.get('G', []):
                cost -= 10  # prefer gold
            if kb.ask_possible_pit(neighbor) or kb.ask_possible_wumpus(neighbor):
                cost += 1000  # avoid danger

            new_cost = cost_so_far[current] + cost
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost + heuristic(goal, neighbor)
                heapq.heappush(frontier, (priority, neighbor))
                came_from[neighbor] = current

    # Reconstruct path
    path = []
    curr = goal
    while curr and curr in came_from:
        path.append(curr)
        curr = came_from[curr]
    path.reverse()
    return path if path and path[0] == start else []
