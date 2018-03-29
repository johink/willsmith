from games.ttt.ttt_action import TTTAction
from games.ttt.ttt_board import TTTBoard
from games.ttt.ttt_move import TTTMove

from willsmith.game import Game


class NestedTTT(Game):
    """
    A game of Nested Tic-Tac-Toe, where each square on the outer board 
    is another Tic-Tac-Toe board.

    The game is played as standard Tic-Tac-Toe, except there are 9 inner 
    boards to make moves on.  Winning an inner board claims that space for 
    the winner on the outer board.  Draws result in a square that does not 
    count for either side.  Winning the game requires winning 3 inner boards 
    in a row, forming a win on the outer board.

    The state of the game is stored using the TTTBoard class:  one for the 
    outer board and one for each of the 9 inner boards.  Actions are never 
    explicitly taken by the players on the outer board, only as a result of a 
    win on an inner board.

    See Game documentation for the public API expected by other classes.
    """

    ACTION = TTTAction

    def __init__(self, num_agents):
        """
        Initialize the state for the game and checking for legal moves.

        Both the outer board and the 9 inner boards are initialized with empty 
        squares.  See TTTBoard for the documentation on boards.
        
        The set of legal board positions, one pair of 
        position for each, is also initialized.  This enables faster checking 
        if a move is legal, and also faster generation of the available legal 
        actions in get_legal_actions.
        """
        super().__init__(num_agents)

        bs = TTTBoard.BOARD_SIZE

        self.outer_board = TTTBoard()
        self.inner_boards = [[TTTBoard() for _ in range(bs)] for _ in range(bs)]

        self.legal_positions = {((r, c), (ir, ic)) for r in range(bs) for c in range(bs) for ir in range(bs) for ic in range(bs)}

    def get_legal_actions(self):
        move = self._agent_id_to_move(self.current_agent_id)
        return [TTTAction(outer_pos, inner_pos, move) 
                    for outer_pos, inner_pos  in self.legal_positions]

    def get_winning_id(self):
        """
        Return the id of the agent who won the game.  
        None is the default value,  indicating either a draw or that the game 
        is still ongoing.
        """
        winner_id = None
        if self.outer_board.winner is not None:
            winner_id = self._move_to_agent_id(self.outer_board.winner)
        return winner_id

    def is_legal_action(self, action):
        """
        Check that the action's position is legal and that the action's move 
        matches the expected move for the current turn.
        """
        legal_position = (action.outer_pos, action.inner_pos) in self.legal_positions
        legal_move = action.move == self._agent_id_to_move(self.current_agent_id)
        return legal_position and legal_move

    @Game.progress_game
    def take_action(self, action):
        """
        Take the given action on the indicated inner board.  

        If this triggers a win, update the outer board with the players 
        move.  Either way, remove the positions that are no longer legal from 
        the set of legal positions.

        See the Game class for documentation on the progress_game decorator.
        """
        r, c = action.outer_pos

        board_won = self.inner_boards[r][c].take_action(action.inner_pos, action.move)
        if board_won:
            self.outer_board.take_action(action.outer_pos, action.move)

        self._remove_illegal_positions(action.outer_pos, action.inner_pos, board_won)

    def _remove_illegal_positions(self, outer_pos, inner_pos, board_won):
        """
        Remove the pair of positions from the set of legal positions.

        If the given move was a board winning one, all of the remaining open 
        squares on the inner board are now illegal and are removed as well.
        """
        self.legal_positions.remove((outer_pos, inner_pos))
        if board_won:
            self.legal_positions -= {(outer_pos, (r, c)) for r in range(TTTBoard.BOARD_SIZE) for c in range(TTTBoard.BOARD_SIZE)}

    def is_terminal(self):
        is_winner = self.outer_board.get_winner() is not None
        moves_left = bool(self.legal_positions)
        return is_winner or not moves_left

    def _agent_id_to_move(self, agent_id):
        lookup = {0 : TTTMove.X, 1 : TTTMove.O}
        return lookup[agent_id]

    def _move_to_agent_id(self, move):
        lookup = {TTTMove.X : 0, TTTMove.O: 1}
        return lookup[move]

    def __str__(self):
        """
        Return a string of the gameboard the looks like this:

        [  X  ] | [  O  ] | [O X O]
        [     ] | [X   O] | [O    ]
        [O X  ] | [X O  ] | [  O  ]
        ---------------------------
        [     ] | [O   X] | [X   X]
        [  X  ] | [  X  ] | [     ]
        [    X] | [X   O] | [     ]
        ---------------------------
        [     ] | [     ] | [O   O]
        [     ] | [  O  ] | [O    ]
        [X    ] | [    O] | [X X  ]
        """
        result = []
        for i in range(TTTBoard.BOARD_SIZE):
            for j in range(TTTBoard.BOARD_SIZE):
                result.append(" | ".join([str(inner_board.board[j]) for inner_board in self.inner_boards[i]]))
            if i < 2:
                result.append("-"*27)
        board_string = "\n".join(result)
        return board_string.replace(',', '')
