import numpy as np

from functools import reduce
from game import Game
from ttt_move import TTTMove
from copy import deepcopy


class NestedTTT(Game):
    """
    Action :: ((or, oc), ((ir, ic), move))
    NestedTTTAction :: (outer_position, BoardAction)
    outer_position :: (r, c)
    BoardAction :: (position, move)
    """


    STANDARD_BOARD_SIZE = 3


    def __init__(self, agent_ids, board_size = STANDARD_BOARD_SIZE):
        self.board_size = board_size
        self.outer_board = self.Board(self.board_size)
        self.inner_boards = [[self.Board(self.board_size) for _ in range(self.board_size)] for _ in range(self.board_size)]

        bs = self.board_size
        self.legal_positions = {((r, c), (ir, ic)) for r in range(bs) for c in range(bs) for ir in range(bs) for ic in range(bs)}

        super().__init__(agent_ids)

    def copy(self):
        return deepcopy(self)

    def get_legal_actions(self):
        move = self._agent_id_to_move(self.agent_turn)
        return [(outer_pos, (inner_pos, move)) for outer_pos, inner_pos  in self.legal_positions]

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
            self.legal_positions -= {(outer_pos, (r, c)) for r in range(self.board_size) for c in range(self.board_size)}

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
        for i in range(self.board_size):
            for j in range(self.board_size):
                result.append(" | ".join([str(inner_board.board[j]) for inner_board in self.inner_boards[i]]))
            if i < 2:
                result.append("-"*20)
        return "\n".join(result)

    class Board:
        def __init__(self, board_size):
            self.board_size = board_size
            self.board = np.full((self.board_size, self.board_size), TTTMove.BLANK)

        def take_action(self, action):
            """
            Applies the action to the board.
            Returns whether the board is won or not after this action.
            """
            pos, move = action
            self.board[pos] = move
            return self.check_if_winner(action)

        def get_winner(self):
            """
            Returns the move that won the board or None if it is still ongoing.
            """
            winner = None
            for move in [TTTMove.X, TTTMove.O]:
                if self.check_if_winner((None, move)):
                    winner = move
                    break
            return winner

        def check_if_winner(self, action):
            """
            Determine if the player with move in the action won the board.
            """
            pos, move = action
            if pos is not None:
                r, c = pos
                won = np.all(self.board[:,c] == move) or np.all(self.board[r] == move)
                if r == c and not won:
                    won = np.all(np.diag(self.board) == move)
                if r + c == (self.board_size - 1) and not won:
                    won = np.all(np.diag(self.board[::-1]) == move)
            else:
                reduce_func = lambda x,y: x or self._check_axis_for_win(y, move)
                won = (reduce(reduce_func, self.board, False) or
                        reduce(reduce_func, self.board.swapaxes(0,1), False) or
                        reduce(reduce_func, [self.board.diagonal(), self.board[::-1].diagonal()], False))
            return won

        def _check_axis_for_win(self, array, move):
            """
            Returns if all elements are the same as move.

            Uses the fact that sets do not contain duplicate items to
            quickly determine if there is a complete row.
            """
            move_set = set(array).union({move})
            return len(move_set) == 1
