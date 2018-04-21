from tests.games.game_testcase import GameTestCase

from games.havannah.color import Color
from games.havannah.havannah import Havannah
from games.havannah.havannah_action import HavannahAction

class TestHavannah(GameTestCase):

    def setUp(self):
        super().setUp()
        self.game = Havannah()
        self.test_action = HavannahAction((0, 0, 0), Color.BLUE)

    def test_get_legal_actions_color_stays_in_sync(self):
        first_action = self.game.get_legal_actions()[0]
        self.assertEqual(first_action.color, Color.BLUE)
        self.game.take_action(first_action)
        second_action = self.game.get_legal_actions()[0]
        self.assertEqual(second_action.color, Color.RED)

    def test_game_equality(self):
        self._test_game_equality()
