from world.world_loader import load_world
from agent.agent import WumpusAgent
from gui.visualizer import Visualizer

    # input:
    # the text file, example: wumpus_world.txt

    # output:
    # »trace« of the agent together with all logical entailments for every move of the agent
    # Move to field (2,1)
    # Breeze sensed
    # Move to field (1,1)
    # Move to field (1,2)
    # Smell sensed
    # Found out Wumpus is on field (1,3)
    # Found out pit is on field (3,1)
    # Move to field (2,2)

def main():
    world = load_world("tests/wumpus_world_sample.txt")
    agent = WumpusAgent(world)
    agent.run()
    visualizer = Visualizer(world, agent)
    visualizer.run()

if __name__ == "__main__":
    main()
