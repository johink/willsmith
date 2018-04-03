from copy import copy, deepcopy

from games.havannah.havannah_action import HavannahAction
from games.havannah.color import Color
from games.havannah.havannah_board import HavannahBoard

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

    def __init__(self, num_agents):
        super().__init__(num_agents)
        self.board = HavannahBoard()
        self.legal_positions = set(self.board.grid.keys())

    def get_legal_actions(self):
        color = self._agent_id_to_color(self.current_agent_id)
        return [HavannahAction(coord, color) for coord in self.legal_positions]

    def is_legal_action(self, action):
        """
        Check that the action's position is legal and that the action's color 
        matches the expected color for the current turn.
        """
        legal_position = action.coord in self.legal_positions
        legal_color = action.color == self._agent_id_to_color(self.current_agent_id) 
        return legal_position and legal_color

    def _take_action(self, action):
        """
        Take the given action on the game board, and remove the position from 
        the set of legal positions.

        See the Game class for documentation on the progress_game decorator.
        """
        self.board.take_action(action)
        self.board.check_for_winner(action)
        self.legal_positions.remove(action.coord)

    def get_winning_id(self):
        """
        Return the id of the agent who won the game.  
        None is the default value,  indicating either a draw or that the game 
        is still ongoing.
        """
        winner = self.board.get_winner()
        if winner is not None:
            winner = self._color_to_agent_id(winner)
        return winner

    def is_terminal(self):
        return len(self.legal_positions) == 0 or self.board.get_winner() is not None

    def _agent_id_to_color(self, agent_id):
        lookup = {0 : Color.BLUE, 1 : Color.RED}
        return lookup[agent_id]

    def _color_to_agent_id(self, color):
        lookup = {Color.BLUE : 0, Color.RED : 1}
        return lookup[color]

    def __str__(self):
        return str(self.board)

    def __deepcopy__(self, memo):
        h = Havannah.__new__(Havannah)

        # should rely on inheritance for these attributes
        h.num_agents = self.num_agents
        h.current_agent_id = self.current_agent_id

        h.board = deepcopy(self.board)
        h.legal_positions = copy(self.legal_positions)
        return h

    def __eq__(self, other):
        return (type(self) == type(other) and
                self.board == other.board and 
                self.legal_positions == other.legal_positions and
                self.current_agent_id == other.current_agent_id and 
                self.num_agents == other.num_agents)

    def __hash__(self):
        # I believe the frozenset will guarantee equal hashes for equal 
        # sets, but I am not sure and should add some tests for this
        return hash((self.num_agents, self.current_agent_id, 
                       frozenset(self.legal_positions), 
                        self.board))
