from nested_ttt import NestedTTT
from mcts_agent import MCTSAgent
from random_agent import RandomAgent


class Simulator:
    """
    Manages the game and its state, and prompts agents for actions.
    """

    CLEAR_TERMINAL = chr(27) + "[2J"

    def __init__(self, game, agent_list):
        self.game = game(len(agent_list))
        self.agents = [agent(i) for i, agent in enumerate(agent_list)]

    def advance_by_action(self, action):
        legal = self.game.take_action(action)
        if legal:
            for agent in self.agents:
                agent.take_action(action)
    
    def run_game(self):
        while not self.game.is_terminal():
            current_agent = self.agents[self.game.current_agent_id]
            action = current_agent.search(self.game.copy())
            self.advance_by_action(action)
            self.display_game()
    
    def display_game(self):
        print(self.CLEAR_TERMINAL)
        print(self.game)


if __name__ == "__main__":
    simulator = Simulator(NestedTTT, [MCTSAgent, RandomAgent])
    simulator.run_game()
