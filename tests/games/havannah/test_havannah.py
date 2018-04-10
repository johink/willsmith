from unittest import TestCase

from games.havannah.color import Color
from games.havannah.havannah import Havannah
from games.havannah.havannah_action import HavannahAction

class TestHavannah(TestCase):

    def setUp(self):
        self.game = Havannah()
        self.test_action = HavannahAction((0, 0, 0), Color.BLUE)

    def test_havannah_init_equal_games(self):
        self.assertEqual(self.game, Havannah())

    def test_havannah_one_action_unequal_games(self):
        self.game.take_action_if_legal(self.test_action)
        self.assertNotEqual(self.game, Havannah())

    def test_havannah_same_action_equal_games(self):
        self.game.take_action_if_legal(self.test_action)
        other_game = Havannah()
        other_game.take_action_if_legal(self.test_action)
        self.assertEqual(self.game, other_game)

    def test_deepcopy_actions_do_not_affect_orig(self):
        other_game = self.game.copy()
        other_game.take_action_if_legal(self.test_action)
        self.assertNotEqual(self.game, other_game)

    def test_get_legal_actions_color_stays_in_sync(self):
        first_action = self.game.get_legal_actions()[0]
        self.assertEqual(first_action.color, Color.BLUE)
        self.game.take_action_if_legal(first_action)
        second_action = self.game.get_legal_actions()[0]
        self.assertEqual(second_action.color, Color.RED)
