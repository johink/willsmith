from agent import Agent


class RandomAgent(Agent):
    """
    Agent that chooses random actions regardless of the game state.
    """
    
    def __init__(self, agent_id):
        super().__init__(agent_id)

    def search(self, state):
        return state.generate_random_action()

    def take_action(self, action):
        pass
