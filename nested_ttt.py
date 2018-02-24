import numpy as np

from functools import reduce
from state import State
from ttt_move import TTTMove


class NestedTTT(State):

    class Board:
        def __init__(self, board_size = 3):
            self.board_size = board_size
            self.board = np.full((self.board_size, self.board_size), TTTMove.BLANK)

        def take_action(self, action):
            """
            Applies the action to the board.

            BoardAction :: (move, pos)
            """
            move, pos = action
            self.board[pos] = move

        def check_winner(self):
            """
            Check for a winner by summing over columns, rows, and diagonals
            Enum values cannot overlap, so 3 times Enum value means we have 3 in a row
            """
            for team in [TTTMove.X, TTTMove.O]:
                if (np.any(self.board.sum(axis = 1) == team * 3) or
                   np.any(self.board.sum(axis = 0) == team * 3) or
                   np.diag(self.board).sum() == team * 3 or
                   np.diag(self.board[::-1]).sum() == team * 3):
                    return team

            return None

        def check_winner1(self):
            """
            Check for a winner using check_for_win function.
            """
            win = None
            for team in [TTTMove.X, TTTMove.O]:
                for row in self.board:
                    if self.check_for_win(row, team):
                        win = team
                        break
                for col in self.board.swapaxes(0, 1):
                    if self.check_for_win(col, team):
                        win = team
                        break
                for diag in [x.board.diagonal(), x.board[::-1].diagonal()]:
                    if self.check_for_win(diag, team):
                        win = team
                        break

            return win

        def check_winner2(self):
            """
            Check for a winner using check_for_win function.
            """
            winner = None
            for team in [TTTMove.X, TTTMove.O]:
                reduce_func = lambda x,y: x or self.check_for_win(y, team)
                if (reduce(reduce_func, x.board, False) or
                    reduce(reduce_func, x.board.swapaxes(0,1), False) or
                    reduce(reduce_func, [x.board.diagonal(), x.board[::-1].diagonal()], False)):
                    winner = team
            return winner
            

        def check_for_win(self, array, move):
            """
            Returns if all elements are the same as move.

            Uses the fact that sets do not contain duplicate items to 
            quickly determine if there is a complete row.
            """
            move_set = set(array).union({move})
            return len(move_set) == 1
        

    def __init__(self):
        self.outer_board = self.Board()
        self.inner_boards = [[self.Board() for _ in range(3)] for _ in range(3)]
        self.game_over = False

    def get_state(self):
        return self.board

    def take_action(self, action, outer_pos, inner_pos):
        """
        Take an action on the inner board, which will update the outer board if
        it is a winning move.  If the outer board is now won, return 1 to indicate
        the player has won the game, otherwise return None
        """
        self.inner_boards[outer_pos].take_action(action, inner_pos)
        winner = self.inner_boards[outer_pos].check_winner()
        if winner is not None:
            self.outer_board.board[outer_pos] = winner
            if self.outer_board.check_winner():
                return 1

        return None

    def take_action1(self, action):
        """
        Applies the action to the game and updates the outer board if necessary.

        NestedTTTAction :: (outer_position, BoardAction)
        """
        outer_pos, inner_action = action
        self.inner_boards[outer_pos].take_action(inner_action)
        self._update_outer_board(outer_pos, inner_action)

        super().take_action()

    def _update_outer_board(self, outer_pos, inner_action):
        """
        Checks if inner board has been won and updates outer board if so.
        """
        winner = self.inner_boards[outer_pos].check_winner()
        if winner is not None:
            self.outer_board.take_action((outer_pos, winner))

    def final(self):
        return self.outer_board.check_winner() is not None

    def __str__(self):
        result = []
        for i in range(3):
            for j in range(3):
                result.append(" | ".join([str(inner_board.board[j]) for inner_board in self.inner_boards[i]]))
            if i < 2:
                result.append("-"*20)
        return "\n".join(result)
