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
        """
        After checking that the action is valid, apply the action to the 
        game state and the agents.
        """
        if game.is_legal_action(action):
            game.take_action(action)
            for agent in self.agents:
                agent.take_action(action)
    
    def run_game(self):
        """
        Run a console version of the game.
        """
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
