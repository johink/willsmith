from unittest import TestCase

from games.ttt.nested_ttt import NestedTTT
from games.ttt.ttt_action import TTTAction
from games.ttt.ttt_move import TTTMove


class TestNestedTTT(TestCase):
    
    def setUp(self):
        self.game = NestedTTT(2)

    def test_winning_inner_win_triggers_outer_action(self):
        outer_pos = (0, 0)
        r, c = outer_pos
        for inner_pos in [(0, 0), (1, 1), (2, 2)]:
            action = TTTAction(outer_pos, inner_pos, TTTMove.X)
            self.game._take_action(action)
        self.assertEqual(self.game.outer_board.board[r][c], TTTMove.X)

    def test_winning_outer_updates_winner(self):
        positions = [(0, 0), (1, 1), (2, 2)]
        for outer_pos in positions:
            for inner_pos in positions:
                action = TTTAction(outer_pos, inner_pos, TTTMove.X)
                self.game._take_action(action)
        self.assertEqual(self.game.outer_board.winner, TTTMove.X)
