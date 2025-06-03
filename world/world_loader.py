def load_world(filename):
    world = {}
    with open(filename, 'r') as file:
        for line in file:
            entry = line.strip()
            if entry:
                tag = entry[:2]
                coords = (int(entry[-2]), int(entry[-1]))
                if tag not in world:
                    world[tag] = []
                world[tag].append(coords)
    return world
