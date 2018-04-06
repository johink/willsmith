from willsmith.agent import Agent


class RandomAgent(Agent):
    """
    Agent that chooses random actions regardless of the game state.
    """

    def __init__(self, agent_id):
        super().__init__(agent_id)
        self.last_action = None

    def search(self, state, allotted_time):
        """
        Request a random, legal action from the game state, then return it.
        """
        self.last_action = state.generate_random_action()
        return self.last_action

    def take_action(self, action):
        pass

    def __str__(self):
        return "last action:  {}".format(self.last_action)
