from willsmith.agent import Agent


class RandomAgent(Agent):
    """
    Agent that chooses random actions regardless of the game state.
    """

    def __init__(self, agent_id):
        super().__init__(agent_id)

    def search(self, state, max_time = 0.0):
        """
        Request a random, legal action from the game state, then return it.
        """
        self.last_move = state.generate_random_action()
        return self.last_move

    def take_action(self, action):
        pass
