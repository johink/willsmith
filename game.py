from random import choice


class Game:
    """
    Base class to enforce the game interface required by the simulator and 
    agents to play.
    """

    def __init__(self, num_agents):
        self.num_agents = num_agents
        self.current_agent_id = 0

    def copy(self):
        """
        Returns a copy of the state, so that agents can manipulate it as 
        they decide on actions.
        """
        raise NotImplementedError()

    def get_legal_actions(self):
        """
        Returns a list of the actions in the action space that are still legal.
        """
        raise NotImplementedError

    def take_action(self, action):
        """
        Returns an updated state based on the given action
        """
        raise NotImplementedError

    def generate_random_action(self):
        random_action = choice(self.get_legal_actions())
        return random_action

    def win_check(self, agent_id):
        """
        Returns True if the given agent has won the game, False otherwise.
        """
        raise NotImplementedError

    def is_terminal(self):
        """
        Returns True if the game is in a terminal state, False otherwise.
        """
        raise NotImplementedError

    @classmethod
    def progress_game(cls, func):
        """
        Decorator for use by sub-classes, to call _increment_current_agent_id 
        without an explicit method call.
        """
        def f(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            self._increment_current_agent_id()
            return result
        return f

    def _increment_current_agent_id(self):
        """
        Increments the attribute while ensuring it stays within range 
        [0, self.num_agents).
        """
        self.current_agent_id += 1
        if self.current_agent_id == self.num_agents:
            self.current_agent_id = 0
