from constants import BOARD_SIZE
from copy import deepcopy
from game import Game
from ttt_board import TTTBoard
from ttt_move import TTTMove


class NestedTTT(Game):
    """
    Action :: ((or, oc), ((ir, ic), move))
    NestedTTTAction :: (outer_position, BoardAction)
    outer_position :: (r, c)
    BoardAction :: (position, move)
    """


    def __init__(self, agent_ids):
        bs = BOARD_SIZE

        self.outer_board = TTTBoard()
        self.inner_boards = [[TTTBoard() for _ in range(bs)] for _ in range(bs)]

        self.legal_positions = {((r, c), (ir, ic)) for r in range(bs) for c in range(bs) for ir in range(bs) for ic in range(bs)}

        super().__init__(agent_ids)

    def copy(self):
        return deepcopy(self)

    def get_legal_actions(self):
        move = self._agent_id_to_move(self.agent_turn)
        return [(outer_pos, (inner_pos, move)) for outer_pos, inner_pos  in self.legal_positions]

    def no_more_actions(self):
        return not bool(self.legal_positions)

    def get_state(self):
        return self.board

    def take_action(self, action):
        """
        Applies the action to the game and updates the outer board if necessary.
        Also removes now illegal positions from self.legal_positions
        """
        outer_pos, inner_action = action
        r, c = outer_pos
        inner_pos, move = inner_action
        board_won = self.inner_boards[r][c].take_action(inner_action)
        if board_won:
            self.outer_board.take_action((outer_pos, move))

        self._remove_illegal_positions(outer_pos, inner_pos, board_won)

        self.increment_agent_turn()

    def _remove_illegal_positions(self, outer_pos, inner_pos, board_won):
        """
        Clears positions from self.legal_positions based on action taken and if
        a nested game was completed.
        """
        self.legal_positions.remove((outer_pos, inner_pos))
        if board_won:
            self.legal_positions -= {(outer_pos, (r, c)) for r in range(BOARD_SIZE) for c in range(BOARD_SIZE)}

    def is_terminal(self):
        winner = self.outer_board.get_winner() is not None
        return winner or not self.get_legal_actions()

    def win_check(self, agent_id):
        """
        Determines if the player with agent_id won the game
        """
        win = False
        if self.is_terminal():
            agent_move = self._agent_id_to_move(agent_id)
            win = self.outer_board.check_if_winner((None, agent_move))
        return win

    def _agent_id_to_move(self, agent_id):
        lookup = {0 : TTTMove.X, 1 : TTTMove.O}
        return lookup[agent_id]

    def __str__(self):
        result = []
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                result.append(" | ".join([str(inner_board.board[j]) for inner_board in self.inner_boards[i]]))
            if i < 2:
                result.append("-"*27)
        board_string = "\n".join(result)
        return board_string.replace(',', '')
