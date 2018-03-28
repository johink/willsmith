from copy import deepcopy

from games.ttt.ttt_board import TTTBoard
from games.ttt.ttt_move import TTTMove

from willsmith.game import Game


class NestedTTT(Game):
    """
    Represents a game of tic-tac-toe where each "square" on the outer board
    is a standard tic-tac-toe board.

    Relevant datatypes for actions:
    Action :: ((or, oc), ((ir, ic), move))
    NestedTTTAction :: (outer_position, BoardAction)
    outer_position :: (r, c)
    BoardAction :: (position, move)
    """

    def __init__(self, num_agents):
        super().__init__(num_agents)

        bs = TTTBoard.BOARD_SIZE

        self.outer_board = TTTBoard()
        self.inner_boards = [[TTTBoard() for _ in range(bs)] for _ in range(bs)]

        self.legal_positions = {((r, c), (ir, ic)) for r in range(bs) for c in range(bs) for ir in range(bs) for ic in range(bs)}

    def copy(self):
        return deepcopy(self)

    def get_legal_actions(self):
        move = self._agent_id_to_move(self.current_agent_id)
        return [(outer_pos, (inner_pos, move)) for outer_pos, inner_pos  in self.legal_positions]

    def get_winning_id(self):
        winner_id = None
        if self.outer_board.winner is not None:
            winner_id = self._move_to_agent_id(self.outer_board.winner)
        return winner_id

    def is_legal_action(self, action):
        """
        Checks that the position for the action is still legal and that
        the given TTTMove in the action matches the current agent.
        """
        outer_pos, inner_action = action
        inner_pos, move = inner_action

        legal = True
        if (((outer_pos, inner_pos) not in self.legal_positions) or
            (move != self._agent_id_to_move(self.current_agent_id))):
            legal = False

        return legal

    @Game.progress_game
    def take_action(self, action):
        outer_pos, inner_action = action
        r, c = outer_pos
        inner_pos, move = inner_action

        board_won = self.inner_boards[r][c].take_action(inner_action)
        if board_won:
            self.outer_board.take_action((outer_pos, move))

        self._remove_illegal_positions(outer_pos, inner_pos, board_won)

    def _remove_illegal_positions(self, outer_pos, inner_pos, board_won):
        """
        Clears positions from self.legal_positions based on action taken and if
        a nested game was completed.
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
        result = []
        for i in range(TTTBoard.BOARD_SIZE):
            for j in range(TTTBoard.BOARD_SIZE):
                result.append(" | ".join([str(inner_board.board[j]) for inner_board in self.inner_boards[i]]))
            if i < 2:
                result.append("-"*27)
        board_string = "\n".join(result)
        return board_string.replace(',', '')
