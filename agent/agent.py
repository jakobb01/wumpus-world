from logic.knowledge_base import KnowledgeBase
from search.planner import a_star_search

class WumpusAgent:
    def __init__(self, world):
        self.world = world
        self.position = (1, 2)
        self.facing = 'right'
        self.visited = set()
        self.kb = KnowledgeBase()
        print(f"Starting at {self.position}, facing {self.facing}")

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
        print(f"Percepts sensed: {percept}")
        # go for tell knowledge base
        self.kb.tell(self.position, percept)
        print(f"Safe fields known: {self.kb.safe}")
        print(f"Possible pits: {dict(self.kb.possible_pits)}")
        print(f"Possible wumpus: {dict(self.kb.possible_wumpus)}")
        # with knows 
        #path = a_star_search(self.position, goal, self.kb, self.world)
        #print("Planned path:", path)
