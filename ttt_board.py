from itertools import product
from ttt_move import TTTMove


class TTTBoard:
    """
    Represents a tic-tac-toe board and the operations that go with it.
    Used for both inner and outer boards of NestedTTT.
    """
    
    BOARD_SIZE = 3
    winning_positions = None

    def __init__(self):
        self.board = [[TTTMove.BLANK for _ in range(TTTBoard.BOARD_SIZE)] for _ in range(TTTBoard.BOARD_SIZE)]

    def take_action(self, action):
        """
        Applies the action to the board.
        Returns whether the board is won or not after this action.
        """
        pos, move = action
        r, c = pos
        self.board[r][c] = move
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
        return tuple(map(tuple, self.board)) in self.winning_positions

    def _check_axis_for_win(self, array, move):
        """
        Returns if all elements are the same as move.

        Uses the fact that sets do not contain duplicate items to
        quickly determine if there is a complete row.
        """
        move_set = set(array).union({move})
        return len(move_set) == 1

    @staticmethod
    def generate_winning_positions():
        bs = TTTBoard.BOARD_SIZE
        winning_positions = set()
        other_moves = [TTTMove.BLANK, TTTMove.X, TTTMove.O]
        all_possibilities = list(product(other_moves, repeat = (bs ** 2 - bs)))

        for move in [TTTMove.X, TTTMove.O]:
            winner = (move,) * bs
            for possibility in all_possibilities:
                #Creating row wins
                for r in range(bs):
                    board = []
                    pcopy = list(possibility)
                    for i in range(bs):
                        if i == r:
                            board.append(winner)
                        else:
                            board.append((pcopy.pop(), pcopy.pop(), pcopy.pop()))
                    winning_positions.add(tuple(board))

                #Creating column wins
                for col in range(bs):
                    board = []
                    pcopy = list(possibility)
                    for _ in range(bs):
                        board.append(tuple((move if curr == col else pcopy.pop() for curr in range(bs))))
                    winning_positions.add(tuple(board))

                #Creating diagonal wins
                board = []
                pcopy = list(possibility)
                for d in range(bs):
                    board.append(tuple(move if i == d else pcopy.pop() for i in range(bs)))
                winning_positions.add(tuple(board))

                #Creating counter-diagonal wins
                board = []
                pcopy = list(possibility)
                for d in range(bs):
                    board.append(tuple(move if (i + d) == (bs - 1) else pcopy.pop() for i in range(bs)))
                winning_positions.add(tuple(board))
        return winning_positions


# initializes the winning_positions class attribute for use in its methods
TTTBoard.winning_positions = TTTBoard.generate_winning_positions()
