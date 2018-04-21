from tests.games.game_testcase import GameTestCase

from games.ttt.nested_ttt import NestedTTT
from games.ttt.ttt_action import TTTAction
from games.ttt.ttt_move import TTTMove


class TestNestedTTT(GameTestCase):
    
    def setUp(self):
        super().setUp()
        self.game = NestedTTT()
        self.test_action = TTTAction((0, 0), (0, 0), TTTMove.X)

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

    def test_remove_illegal_actions_removes_extra_actions_on_win(self):
        outer_pos = (0, 0)
        for inner_pos in [(0, 0), (0, 1), (0, 2)]:
            action = TTTAction(outer_pos, inner_pos, TTTMove.X)
            self.game._take_action(action)
            self.assertFalse(self.game.is_legal_action(action))
        for inner_pos in [(1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]:
            action = TTTAction(outer_pos, inner_pos, TTTMove.X)
            self.assertFalse(self.game.is_legal_action(action))

    def test_game_equality(self):
        self._test_game_equality()
