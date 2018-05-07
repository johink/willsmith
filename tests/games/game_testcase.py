from unittest import TestCase


class GameTestCase(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def _test_game_equality(self):
        other_game = self.game.copy()
        self.assertEqual(self.game, other_game)

        self.game.take_action(self.test_action)
        self.assertNotEqual(self.game, other_game)

        other_game.take_action(self.test_action)
        self.assertEqual(self.game, other_game)
