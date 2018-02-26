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
            reduce_func = lambda x,y: x or self._check_axis_for_win(y, team)
            if (reduce(reduce_func, x.board, False) or
                reduce(reduce_func, x.board.swapaxes(0,1), False) or
                reduce(reduce_func, [x.board.diagonal(), x.board[::-1].diagonal()], False)):
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
        winner = self.inner_boards[outer_pos].get_winner()
        if winner is not None:
            self.outer_board.board[outer_pos] = winner
            if self.outer_board.get_winner():
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

        super().take_action()       # increment's State's agent_id, should probably be an inherited function

    def is_terminal(self):
        return self.outer_board.get_winner() is not None

    def _update_outer_board(self, outer_pos, inner_action):
        """
        Checks if inner board has been won and updates outer board if so.
        """
        winner = self.inner_boards[outer_pos].get_winner()
        if winner is not None:
            self.outer_board.take_action((outer_pos, winner))

    def win_check(self, agent_id):
        """
        Determines if the player with agent_id won the game
        """
        agent_move = self._agent_id_to_move(agent_id)
        return agent_move == self.outer_board.get_winner()

    def _agent_id_to_move(self, agent_id):
        lookup = {0 : TTTMove.X, 1 : TTTMove.O}
        return lookup[agent_id]

    def __str__(self):
        result = []
        for i in range(3):
            for j in range(3):
                result.append(" | ".join([str(inner_board.board[j]) for inner_board in self.inner_boards[i]]))
            if i < 2:
                result.append("-"*20)
        return "\n".join(result)
