from world.world_loader import load_world
from agent.agent import WumpusAgent
from gui.visualizer import Visualizer

def main():
    world = load_world("tests/wumpus_world_sample.txt")
    agent = WumpusAgent(world)
    agent.run()
    visualizer = Visualizer(world, agent)
    visualizer.run()

if __name__ == "__main__":
    main()
