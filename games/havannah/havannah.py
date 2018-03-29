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
    bridge.  These are described and checked in the HavannahBoard class.

    Coordinates system for hexes comes from the flat-topped version described 
    here:  
    https://www.redblobgames.com/grids/hexagons/#coordinates-cube
    """

    BEGINNER_BOARD_SIZE = 8
    BOARD_SIZE = 10

    def __init__(self, num_agents, board_size = BEGINNER_BOARD_SIZE):
        super().__init__(num_agents)
        self.board = HavannahBoard(board_size)
        self.legal_positions = set(self.board.grid.keys())

    def get_legal_actions(self):
        color = self._agent_id_to_color(self.current_agent_id)
        return [HavannahAction(coord, color) for coord in self.legal_positions]

    def is_legal_action(self, action):
        """
        Checks that the action is using the proper color (ie matching the color
        of the current agent's turn) and that the position has not already
        been taken by another player.
        """
        return (action.color == self._agent_id_to_color(self.current_agent_id)) 
                    and (action.coord in self.legal_positions)

    @Game.progress_game
    def take_action(self, action):
        self.board.take_action(action)
        self.legal_positions -= action.coord

    def get_winning_id(self):
        """
        Returns agent_id of player that won the game, or None if a game is 
        in-progress or a draw.
        """
        winner = self.board.check_winner()
        if winner is not None:
            winner = self._color_to_agent_id(winner)
        return winner

    def is_terminal(self):
        return len(self.legal_positions == 0) or self.board.check_winner() is not None

    def _agent_id_to_color(self, agent_id):
        lookup = {0 : Color.BLUE, 1 : Color.RED}
        return lookup[agent_id]

    def _color_to_agent_id(self, color):
        lookup = {Color.BLUE : 0, Color.RED : 1}
        return lookup[color]
