from collections import defaultdict

class KnowledgeBase:
    def __init__(self, size):
        self.visited = set()
        self.safe = set()
        self.possible_pits = defaultdict(int)
        self.possible_wumpus = defaultdict(int)
        self.confirmed_pits = set()
        self.confirmed_wumpus = None
        self.size = size  # (max_x, max_y)

    def in_bounds(self, pos):
        x, y = pos
        max_x, max_y = self.size
        return 1 <= x <= max_x and 1 <= y <= max_y

    def tell(self, position, percept):
        x, y = position
        self.visited.add(position)
        self.safe.add(position)  # safe if we are on it

        # determine adjacent tiles
        adj = [a for a in self.get_adjacent(x, y) if self.in_bounds(a)]

        if percept.get('breeze', False):
            for a in adj:
                if a not in self.visited and a not in self.safe:
                    self.possible_pits[a] += 1
        elif percept.get('stench', False):
            for a in adj:
                if a not in self.visited and a not in self.safe:
                    self.possible_wumpus[a] += 1
        else:
            for a in adj:
                if a not in self.possible_wumpus and a not in self.possible_pits:
                    self.safe.add(a)

    def ask_safe(self, position):
        return (
            self.in_bounds(position) and
            position in self.safe and
            position not in self.confirmed_pits and
            position != self.confirmed_wumpus
        )

    def ask_possible_pit(self, position):
        return self.in_bounds(position) and self.possible_pits.get(position, 0) > 0

    def ask_possible_wumpus(self, position):
        return self.in_bounds(position) and self.possible_wumpus.get(position, 0) > 0

    def ask_all(self):
        return {
            'safe': {pos for pos in self.safe if self.in_bounds(pos)},
            'possible_pits': {pos for pos in self.possible_pits.keys() if self.in_bounds(pos)},
            'possible_wumpus': {pos for pos in self.possible_wumpus.keys() if self.in_bounds(pos)}
        }

    def get_adjacent(self, x, y):
        return [
            (x+1, y), (x-1, y),
            (x, y+1), (x, y-1)
        ]
