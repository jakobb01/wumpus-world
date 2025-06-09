from logic.knowledge_base import KnowledgeBase
from search.planner import a_star_search

class WumpusAgent:
    def __init__(self, world):
        self.world = world
        self.position = world['A'][0] if 'A' in world and world['A'] else (1, 1)
        self.exit_cave_pos = world['GO'][0] if 'GO' in world and world['GO'] else (1, 1)
        self.facing = 'right' # predefined starting face for agent
        self.visited = set()
        self.size = tuple(world['size'][0]) if isinstance(world['size'], list) else world['size']
        self.kb = KnowledgeBase(self.size)
        self.found_gold = set() # store were we found gold, so we can count only once at the end.
        #print(f"Starting at {self.position}, facing {self.facing}")

    # rules
    # price of shooting the (only) arrow is -100 points
    # start position of the agent is facing right
    # starting position of the agent is in .txt as A, example: A11 > agent on x=1 and y=1
    # exit from the cave is GOxy = goal field x and y
    # agent should:
    # capable of navigating the cave, avoiding pits and the Wumpus, 
    # picking up as much gold as possible (or maximise the number of points), 
    # and reach the exit point of the cave - field (x,y) that is defined in advance as the goal field.

    # agent should use KB, as the first order logic to figure out what is around him and on the field he is right now.
    # agent uses search algorithm for planning (search algorithm should bias different routes (dont go into pits and wumpus but collect the gold))
    # agent can read the whole cave map at once, but must not »see« fields, that it didn't yet visit 
    
    # extract percepts (cutila/zaznave) from world for the current position
    def get_percept(self, position):
        percept = {}
        x, y = position
        if (x, y) in self.world.get('B', []):
            percept['breeze'] = True
        if (x, y) in self.world.get('S', []):
            percept['stench'] = True
        if (x, y) in self.world.get('G', []):
            percept['glitter'] = True
        return percept

    def run(self):
        # simulation for one move

        print(f"Move to field {self.position}")
        # get all percepts
        percept = self.get_percept(self.position)
        # output for TESTING only
        print(f"Percepts sensed: {percept}")
        # go for tell knowledge base
        self.kb.tell(self.position, percept)
        self.visited.add(self.position)

        # check if agent found gold
        if percept.get('glitter'):
            self.found_gold.add(self.position)

        # output for TESTING only
        info = self.kb.ask_all()
        print("Safe fields:", info['safe'])
        print("Possible pits:", info['possible_pits'])
        print("Possible wumpus:", info['possible_wumpus'])
        matrix = self.build_weighted_matrix(info)

        # planning should first explore all unvisited, safe tiles (updating on the go) and later head for the exit
        safe_unvisited = [pos for pos in info['safe'] if pos not in self.visited and pos != self.exit_cave_pos]
        if safe_unvisited:
            targets = safe_unvisited
        else:
            targets = [self.exit_cave_pos]
        # pass targets to the planning algorithm
        next_move = a_star_search(self.position, targets, matrix)
        # print next move
        print("Next move:", next_move)

    def build_weighted_matrix(self, info):
        max_x, max_y = self.size
        matrix = [[1 for _ in range(max_y)] for _ in range(max_x)]  # default: unknown

        for x in range(1, max_x+1):
            for y in range(1, max_y+1):
                pos = (x, y)
                if pos in info['safe']:
                    if pos == self.exit_cave_pos:
                        matrix[x-1][y-1] = 2  # exit is not preferred over exploring
                    elif pos in self.visited:
                        matrix[x-1][y-1] = 0  # already visited safe
                    else:
                        matrix[x-1][y-1] = 1  # unvisited safe
                if pos in info['possible_pits'] or pos in info['possible_wumpus']:
                    matrix[x-1][y-1] = 1000
        print(matrix)
        return matrix
