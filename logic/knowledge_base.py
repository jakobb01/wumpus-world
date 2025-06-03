from collections import defaultdict

class KnowledgeBase:
    def __init__(self):
        self.visited = set()
        self.safe = set()
        self.possible_pits = defaultdict(int)
        self.possible_wumpus = defaultdict(int)
        self.confirmed_pits = set()
        self.confirmed_wumpus = None

    def tell(self, position, percept):
        #position (x, y)
        #percept dict with keys like 'breeze', 'stench', 'glitter'
        
        x, y = position
        self.visited.add(position)
        self.safe.add(position)  # safe if we are on it

        # determine adjacent tiles
        adj = self.get_adjacent(x, y)

        # handle breeze (possible pit nearby)
        if percept.get('breeze', False):
            for a in adj:
                if a not in self.visited and a not in self.safe:
                    self.possible_pits[a] += 1
        # stench - possible Wumpus nearby
        elif percept.get('stench', False):
            for a in adj:
                if a not in self.visited and a not in self.safe:
                    self.possible_wumpus[a] += 1
        else:
            for a in adj:
                # only mark as safe if not already possible wumpus or pit
                if a not in self.possible_wumpus and a not in self.possible_pits:
                    self.safe.add(a)

        # glitter doesnt affect safety

    def ask_safe(self, position):
        if position in self.safe and \
           position not in self.confirmed_pits and \
           position != self.confirmed_wumpus:
            return True
        return False

    def ask_possible_pit(self, position):
        return self.possible_pits.get(position, 0) > 0

    def ask_possible_wumpus(self, position):
        return self.possible_wumpus.get(position, 0) > 0

    # todo: shouldnt return nodes outside the perimiter
    def get_adjacent(self, x, y):
        return [
            (x+1, y), (x-1, y),
            (x, y+1), (x, y-1)
        ]
