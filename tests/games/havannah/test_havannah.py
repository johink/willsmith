from unittest import TestCase
from timeit import timeit

from games.havannah.color import Color
from games.havannah.havannah import Havannah
from games.havannah.havannah_action import HavannahAction

class TestHavannah(TestCase):

    def setUp(self):
        self.game = Havannah(2)

    def test_havannah_init_equal_games(self):
        self.assertEqual(self.game, Havannah(2))

    def test_havannah_one_action_unequal_games(self):
        action = HavannahAction((0, 0, 0), Color.BLUE)
        self.game.take_action_if_legal(action)
        self.assertNotEqual(self.game, Havannah(2))

    def test_havannah_same_action_equal_games(self):
        action = HavannahAction((0, 0, 0), Color.BLUE)
        self.game.take_action_if_legal(action)
        other_game = Havannah(2)
        other_game.take_action_if_legal(action)
        self.assertEqual(self.game, other_game)

    def test_deepcopy_actions_do_not_affect_orig(self):
        other_game = self.game.copy()
        action = HavannahAction((0, 0, 0), Color.BLUE)
        other_game.take_action_if_legal(action)
        self.assertNotEqual(self.game, other_game)
