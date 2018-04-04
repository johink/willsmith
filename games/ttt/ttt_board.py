from itertools import product

from games.ttt.ttt_move import TTTMove


class TTTBoard:
    """
    The gameboard for Tic-Tac-Toe.

    Holds the state for the board and keeps track of the winner if the board 
    has been won.

    Contains class attribute winning_positions, which is a generated set of 
    all possible winning board configurations.  This solved a problem where 
    the calculation after every move to determine if the board was won slowed 
    down simulation of games to a crawl.  

    Now, the program pauses momentarily at the start of the game to calculate 
    this set.  Then, for the rest of the game a win check only requires the 
    calculation of the hash of the board state, drastically reducing the time 
    spent on these checks.
    """

    BOARD_SIZE = 3
    winning_positions = None

    def __init__(self):
        """
        Initialize the board with blank squares and no winner.

        On the first instantiation of the class it also generates the set 
        of winning board configurations.
        """
        self.board = [[TTTMove.BLANK for _ in range(TTTBoard.BOARD_SIZE)] for _ in range(TTTBoard.BOARD_SIZE)]
        self.winner = None

        if TTTBoard.winning_positions is None:
            TTTBoard.winning_positions = TTTBoard.generate_winning_positions()

    def take_action(self, position, move):
        """
        Applies the move to the board position.
        """
        r, c = position
        self.board[r][c] = move

    def get_winner(self):
        """
        Returns the move that won the board or None if it is still ongoing.
        """
        return self.winner

    def check_for_winner(self, move):
        """
        Check if the board has been won, returning a boolean to indicate this.

        If the board is won, update the winner attribute to the given move.
        """
        won = self._check_if_won()
        if won:
            self.winner = move
        return won

    def _check_if_won(self):
        """
        Check if the board is won by comparing it to the set of winning boards.
        """
        return tuple(map(tuple, self.board)) in self.winning_positions

    @staticmethod
    def generate_winning_positions():
        """
        Calculate every possible winning configuration of the board and 
        return the set of them.
        """
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
