# reads the .txt file and creates tags and coordinates of those tags on the map
def load_world(filename):
    world = {}
    with open(filename, 'r') as file:
        for line in file:
            entry = line.strip()
            if entry:
                # goal field - exit
                if entry.startswith('GO'):
                    tag = 'GO'
                    world[tag] = [ (int(entry[2]), int(entry[3])) ]
                # agent starting coordinates
                elif entry.startswith('A'):
                    tag = 'A'
                    world[tag] = [ (int(entry[1]), int(entry[2])) ]
                # map size
                elif entry.startswith('M'):
                    world['size'] = [ (int(entry[1]), int(entry[2])) ]
                else:
                    tag = entry[0]
                    if tag not in world:
                        world[tag] = []
                    world[tag].append((int(entry[1]), int(entry[2])))
    return world
