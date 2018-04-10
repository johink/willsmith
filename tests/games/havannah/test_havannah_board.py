from copy import deepcopy
from unittest import TestCase

from games.havannah.color import Color
from games.havannah.havannah_action import HavannahAction
from games.havannah.havannah_board import HavannahBoard


class TestHavannahBoard(TestCase):

    def setUp(self):
        HavannahBoard.BOARD_SIZE = 4
        self.board = HavannahBoard()

    def test_check_if_won_empty_board(self):
        self.assertIsNone(self.board.winner)

    def test_check_fork_with_corner(self):
        for coord in [(-3, 0, 3), (-3, 1, 2), (-2, 1, 1), (-2, 2, 0), 
                        (-2, 3, -1)]:
            self.board.take_action(HavannahAction(coord, Color.BLUE))
        self.board.check_for_winner(HavannahAction((-2, 3, -1), Color.BLUE))
        self.assertNotEqual(self.board.winner, Color.BLUE)

    def test_check_fork_error_example_1(self):
        for coord in [(1, 1, -2), (2, 1, -3), (-2, 0, 2), 
                        (-3, 1, 2), (-1, 0, 1), (0, 0, 0), (1, 2, -3), 
                        (0, 1, -1), (-3, 0, 3)]:
            self.board.take_action(HavannahAction(coord, Color.BLUE))
        self.board.check_for_winner(HavannahAction((-3, 0, 3), Color.BLUE))
        self.assertNotEqual(self.board.winner, Color.BLUE)

    def test_check_fork_error_example_2(self):
        for coord in [(3, -1, -2), (3, 0, -3), (2, 1, -3), (1, 2, -3)]:
            self.board.take_action(HavannahAction(coord, Color.BLUE))
        self.board.check_for_winner(HavannahAction((1, 2, -3), Color.BLUE))
        self.assertNotEqual(self.board.winner, Color.BLUE)

    def test_check_bridge_error_example_1(self):
        for coord in [(0, 3, -3), (0, 2, -2), (1, 2, -3)]:
            self.board.take_action(HavannahAction(coord, Color.BLUE))
        self.board.check_for_winner(HavannahAction((1, 2, -3), Color.BLUE))
        self.assertNotEqual(self.board.winner, Color.BLUE)

    def test_deepcopy_action_does_not_affect_original(self):
        action = HavannahAction((0, 0, 0), Color.BLUE)
        other_board = deepcopy(self.board)
        self.board.take_action(action)
        self.assertNotEqual(self.board.grid, other_board.grid)

    def test_check_ring_error_example(self):
        for coord in [(1, 0, -1), (0, 1, -1), (-1, 1, 0), (-1, 0, 1),
                        (0, -1, 1), (0, 0, 0)]:
            self.board.take_action(HavannahAction(coord, Color.BLUE))
        self.board._check_ring((0, 0, 0), Color.BLUE)
        self.assertNotEqual(self.board.winner, Color.BLUE)
