import numpy as np

from functools import reduce
from state import State
from ttt_move import TTTMove
from copy import deepcopy


class NestedTTT(State):
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
        self.is_draw = False

        super().__init__(agent_ids)

    def copy(self):
        return deepcopy(self)

    def get_legal_actions(self):
        move = self._agent_id_to_move(self.agent_turn)
        bs = self.board_size
        results = [((r, c), ((ir, ic), move)) for r in range(bs) for c in range(bs) for ir in range(bs) for ic in range(bs)
                   if self.outer_board.board[r,c] == TTTMove.BLANK and self.inner_boards[r][c].board[ir, ic] == TTTMove.BLANK]

        self.is_draw = bool(results)
        return results

    def get_state(self):
        return self.board

    def take_action(self, action):
        """
        Applies the action to the game and updates the outer board if necessary.
        """
        outer_pos, inner_action = action
        r, c = outer_pos
        self.inner_boards[r][c].take_action(inner_action)
        self._update_outer_board(outer_pos, inner_action)

        self.increment_agent_turn()

    def is_terminal(self):
        winner = self.outer_board.get_winner() is not None
        return winner or not self.get_legal_actions()

    def _update_outer_board(self, outer_pos, inner_action):
        """
        Checks if inner board has been won and updates outer board if so.
        """
        # does not handle draws on the outer board
        r, c = outer_pos
        winner = self.inner_boards[r][c].get_winner()
        if winner is not None:
            self.outer_board.take_action((outer_pos, winner))

    def win_check(self, agent_id):
        """
        Determines if the player with agent_id won the game
        """
        win = False
        if self.is_terminal():
            agent_move = self._agent_id_to_move(agent_id)
            win = agent_move == self.outer_board.get_winner()
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
            """
            pos, move = action
            self.board[pos] = move

        def get_winner(self):
            """
            Determine if the game has been won, and returns the winning
            piece or None if the game is still ongoing.
            """
            winner = None
            for move in [TTTMove.X, TTTMove.O]:
                    if self._check_if_move_won(move):
                        winner = move
            return winner

        def _check_if_move_won(self, move):
            won = False
            reduce_func = lambda x,y: x or self._check_axis_for_win(y, move)
            if (reduce(reduce_func, self.board, False) or
                reduce(reduce_func, self.board.swapaxes(0,1), False) or
                reduce(reduce_func, [self.board.diagonal(), self.board[::-1].diagonal()], False)):
                won = True
            return won

        def _check_axis_for_win(self, array, move):
            """
            Returns if all elements are the same as move.

            Uses the fact that sets do not contain duplicate items to
            quickly determine if there is a complete row.
            """
            move_set = set(array).union({move})
            return len(move_set) == 1
