from abc import ABC, abstractmethod
from copy import deepcopy
from random import choice

from willsmith.action import Action
from willsmith.display_controller import DisplayController


class Game(ABC):
    """
    Abstract base class for games.

    Subclasses are turn-based games where players take single alternating 
    actions until a winner is decided.  
    
    The interface enforced by this class is used by Agent instances to 
    determine their next action and Simulator to control the game as they run 
    agents through a match.

    The ACTION class attribute is expected to be a subclass of the Action 
    base class.

    The NUM_PLAYERS class attribute is required to set the number of agents 
    expected for the game.

    The DISPLAY class attribute is required to set the display for the 
    simulator to use.
    """

    ACTION = None
    DISPLAY = None
    NUM_PLAYERS = None

    def __init__(self):
        """
        Start the game with the first player and sets the number of agents 
        for keeping this index within bounds.

        Also runs checks to ensure the class attributes have been properly 
        assigned by subclass.
        """
        self.num_agents = self.NUM_PLAYERS
        self.current_agent_id = 0

        if (self.ACTION is None 
                or not issubclass(self.ACTION, Action)):
            raise RuntimeError("Game must set its own action, which must subclass Action.")
        if (self.DISPLAY is None 
                or not issubclass(self.DISPLAY, DisplayController)):
            raise RuntimeError("Game must set its display, which must subclass DisplayController.")
        if self.NUM_PLAYERS is None:
            raise RuntimeError("Game must set expected number of players.")

    def get_legal_actions(self):
        results = []
        if not self.is_terminal():
            results = self._get_legal_actions()
        return results

    @abstractmethod
    def _get_legal_actions(self):
        """
        Return a list of the available actions for the current agent in the
        current state of the game.
        """
        pass
    @abstractmethod
    def is_legal_action(self, action):
        """
        Return a boolean indicating if the action is valid and legal.
        """
        pass

    @abstractmethod
    def _take_action(self, action):
        """
        Progress the internal game state by the given action.

        Overriden version of this method should be decorated with 
        progress_game to ensure the current_agent_id attribute remains valid.
        """
        pass

    @abstractmethod
    def get_winning_id(self):
        """
        Return the agent id of the player that won the game.

        None typically indicates a draw or an ongoing game.
        """
        pass

    @abstractmethod
    def is_terminal(self):
        """
        Return a boolean indicating if the game is in a terminal state.
        """
        pass

    def take_action(self, action):
        """
        Ensure that only legal actions are applied to the game, and update 
        the current_agent_id to the next agent.
        """
        if not self.is_legal_action(action):
            raise RuntimeError("Received illegal action: {}".format(action))

        self._take_action(action)
        self._increment_current_agent_id()

    def generate_random_action(self):
        """
        Make a random choice of the available legal actions.  

        Used by random agents or for game playouts by other agents.
        """
        random_action = choice(self.get_legal_actions())
        return random_action

    def copy(self):
        """
        Return a copy of the state.

        Used by the simulator to allow agents to run simulations without 
        corrupting the actual state of the game.
        """
        return deepcopy(self)

    def _increment_current_agent_id(self):
        """
        Increment the agent id of the current player, indicating a new turn.

        This method forces the id to stay in legal range [0, num_agents)
        """
        self.current_agent_id += 1
        if self.current_agent_id == self.num_agents:
            self.current_agent_id = 0

    def __eq__(self, other):
        return self.num_agents == other.num_agents and self.current_agent_id == other.current_agent_id

    def deepcopy_game_attrs(self, new):
        new.num_agents = self.num_agents
        new.current_agent_id = self.current_agent_id
        return new
