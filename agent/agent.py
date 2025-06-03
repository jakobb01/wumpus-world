class WumpusAgent:
    def __init__(self, world):
        self.world = world
        self.position = (1, 1)
        self.facing = 'right'
        self.visited = set()
        print(f"Starting at {self.position}, facing {self.facing}")

    def run(self):
        print("Move to field (1,1)")
        if ('B1', 1) in self.world.get('B', []):
            print("Breeze sensed")
