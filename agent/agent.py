class WumpusAgent:
    def __init__(self, world):
        self.world = world
        self.position = (1, 1)
        self.facing = 'right'
        self.visited = set()
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

    def run(self):
        print("Move to field (1,1)")
        if ('B1', 1) in self.world.get('B', []):
            print("Breeze sensed")
