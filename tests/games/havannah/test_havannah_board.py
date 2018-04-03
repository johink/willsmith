from unittest import TestCase

from games.havannah.havannah_action import HavannahAction
from games.havannah.havannah_board import HavannahBoard
from games.havannah.color import Color


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
        self.assertFalse(self.board._check_fork((-2, 3, -1), Color.BLUE))

    def test_check_fork_error_example_1(self):
        for coord in [(1, 1, -2), (2, 1, -3), (-2, 0, 2), 
                        (-3, 1, 2), (-1, 0, 1), (0, 0, 0), (1, 2, -3), 
                        (0, 1, -1), (-3, 0, 3)]:
            self.board.take_action(HavannahAction(coord, Color.BLUE))
        self.assertFalse(self.board._check_fork((-3, 0, 3), Color.BLUE))

    def test_check_fork_error_example_2(self):
        for coord in [(3, -1, -2), (3, 0, -3), (2, 1, -3), (1, 2, -3)]:
            self.board.take_action(HavannahAction(coord, Color.BLUE))
        self.assertFalse(self.board._check_fork((1, 2, -3), Color.BLUE))

    def test_check_bridge_error_example_1(self):
        for coord in [(0, 3, -3), (0, 2, -2), (1, 2, -3)]:
            self.board.take_action(HavannahAction(coord, Color.BLUE))
        self.assertFalse(self.board._check_bridge((1, 2, -3), Color.BLUE))

    def test_get_edge_label_edge_check_1(self):
        edge_label = self.board._get_edge_label((-3, 1, 2))
        self.assertEqual(edge_label, "-x")

    def test_get_edge_label_edge_check_2(self):
        edge_label = self.board._get_edge_label((3, -1, -2))
        self.assertEqual(edge_label, "x")

    def test_get_edge_label_edge_check_3(self):
        edge_label = self.board._get_edge_label((2, 1, -3))
        self.assertEqual(edge_label, "-z")

    def test_get_edge_label_edge_check_4(self):
        edge_label = self.board._get_edge_label((1, 2, -3))
        self.assertEqual(edge_label, "-z")

    def test_get_edge_label_edge_check_5(self):
        edge_label = self.board._get_edge_label((-1, 3, -2))
        self.assertEqual(edge_label, "y")

    def test_get_edge_label_edge_check_6(self):
        edge_label = self.board._get_edge_label((1, -3, 2))
        self.assertEqual(edge_label, "-y")

    def test_get_edge_label_edge_check_7(self):
        edge_label = self.board._get_edge_label((-2, -1, 3))
        self.assertEqual(edge_label, "z")
