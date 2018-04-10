from copy import deepcopy
from unittest import TestCase

from games.ttt.nested_ttt import NestedTTT
from games.ttt.ttt_action import TTTAction
from games.ttt.ttt_move import TTTMove


class TestNestedTTT(TestCase):
    
    def setUp(self):
        self.game = NestedTTT()

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

    def test_deepcopy_is_equal(self):
        game_copy = deepcopy(self.game)
        self.assertEqual(self.game, game_copy)

    def test_deepcopy_action_does_not_affect_orig(self):
        game_copy = deepcopy(self.game)
        game_copy._take_action(TTTAction((0, 0), (0, 0), TTTMove.X))
        self.assertNotEqual(self.game, game_copy)

    def test_remove_illegal_actions_removes_extra_actions_on_win(self):
        outer_pos = (0, 0)
        for inner_pos in [(0, 0), (0, 1), (0, 2)]:
            action = TTTAction(outer_pos, inner_pos, TTTMove.X)
            self.game._take_action(action)
            self.assertFalse(self.game.is_legal_action(action))
        for inner_pos in [(1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]:
            action = TTTAction(outer_pos, inner_pos, TTTMove.X)
            self.assertFalse(self.game.is_legal_action(action))
