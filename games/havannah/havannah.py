from copy import deepcopy

from games.havannah.color import Color
from games.havannah.havannah_action import HavannahAction
from games.havannah.havannah_board import HavannahBoard
from games.havannah.havannah_display import HavannahDisplay

from willsmith.game import Game


class Havannah(Game):
    """
    The game of Havannah, played on a hex board that is typically 10 hexes to 
    a side.  
    
    Players alternate turns placing stones, or coloring hexes in our 
    case, in previously unchosen hexes.  Play continues until one player has 
    formed one of three different winning configurations:  a ring, fork, or 
    bridge.  
    
    These are described and checked in the HavannahBoard class that stores 
    the game state.

    Coordinates system for hexes comes from the flat-topped version described 
    here:  
    https://www.redblobgames.com/grids/hexagons/#coordinates-cube

    See Game documenation for the public API expected by other classes.
    """

    ACTION = HavannahAction
    DISPLAY = HavannahDisplay
    NUM_PLAYERS = 2

    def __init__(self):
        """
        Generate the board and the initial legal actions for the game.  

        Actions are stored in a coord -> action dictionary to provide fast 
        checking if a position is legal and also allow easy updating of the 
        color attribute of the actions when get_legal_actions is called.
        """
        super().__init__()
        self.board = HavannahBoard()
        self.legal_actions = self._generate_initial_legal_actions()

    def _generate_initial_legal_actions(self):
        cur_color = self._agent_id_to_color(self.current_agent_id)
        return {coord : self.ACTION(coord, cur_color) 
                    for coord in self.board.grid.keys()}
    
    def get_legal_actions(self):
        self._update_legal_actions()
        return list(self.legal_actions.values())

    def _update_legal_actions(self):
        """
        Update each of the actions stored in the legal_actions dictionary to 
        the current color.

        Used to keep get_legal_actions result in sync with the game.
        """
        cur_color = self._agent_id_to_color(self.current_agent_id)
        for action in self.legal_actions.values():
            action.color = cur_color

    def is_legal_action(self, action):
        """
        Check that the action's position is legal and that the action's color 
        matches the expected color for the current turn.
        """
        legal_position = action.coord in self.legal_actions
        legal_color = action.color == self._agent_id_to_color(self.current_agent_id) 
        return legal_position and legal_color

    def _take_action(self, action):
        """
        Take the given action on the game board, check it for a win, and 
        remove that action from the set of legal positions
        """
        self.board.take_action(action)
        self.board.check_for_winner(action)
        del self.legal_actions[action.coord]

    def get_winning_id(self):
        winner = self.board.get_winner()
        if winner is not None:
            winner = self._color_to_agent_id(winner)
        return winner

    def is_terminal(self):
        return not self.legal_actions or self.board.get_winner() is not None

    def _agent_id_to_color(self, agent_id):
        lookup = {0 : Color.BLUE, 1 : Color.RED}
        return lookup[agent_id]

    def _color_to_agent_id(self, color):
        lookup = {Color.BLUE : 0, Color.RED : 1}
        return lookup[color]

    def __str__(self):
        return str(self.board)

    def __eq__(self, other):
        equal = False
        if isinstance(self, other.__class__):
            equal = (self.board == other.board 
                        and self.legal_actions == other.legal_actions 
                        and self.current_agent_id == other.current_agent_id 
                        and self.num_agents == other.num_agents)
        return equal

    def __hash__(self):
        return hash((self.num_agents, self.current_agent_id, 
                        frozenset(self.legal_actions), self.board))

    def __deepcopy__(self, memo):
        new = Havannah.__new__(Havannah)
        memo[id(self)] = new

        # should rely on inheritance for these attributes
        new.num_agents = self.num_agents
        new.current_agent_id = self.current_agent_id

        new.board = deepcopy(self.board, memo)
        new.legal_actions = {k : deepcopy(v, memo) 
                                for k, v in self.legal_actions.items()}
        return new
