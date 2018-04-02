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

    def test_check_if_won_error_example(self):
        for coord in [(3, -1, -2), (3, 0, -3), (2, 1, -3), (1, 2, -3)]:
            self.board.take_action(HavannahAction(coord, Color.BLUE))
        self.assertFalse(self.board._check_fork((1, 2, -3), Color.BLUE))

    def test_check_fork_with_corner(self):
        for coord in [(-3, 0, 3), (-3, 1, 2), (-2, 1, 1), (-2, 2, 0), 
                        (-2, 3, -1)]:
            self.board.take_action(HavannahAction(coord, Color.BLUE))
        self.assertFalse(self.board._check_fork((-2, 3, -1), Color.BLUE))

    def test_check_fork_with_corner_error_example(self):
        for coord in [(1, 1, -2), (2, 1, -3), (-2, 0, 2), 
                        (-3, 1, 2), (-1, 0, 1), (0, 0, 0), (1, 2, -3), 
                        (0, 1, -1), (-3, 0, 3)]:
            self.board.take_action(HavannahAction(coord, Color.BLUE))
        print(self.board)
        self.assertFalse(self.board._check_fork((-3, 0, 3), Color.BLUE))

    def test_get_neighbors_edge_coord_neighbors_inside_board(self):
        expected_neighbors = {(-3, 1, 2), (-2, 0, 2), (-2, -1, 3)}
        calculated_neighbors = set(self.board._get_neighbors((-3, 0, 3)))
        self.assertEqual(calculated_neighbors, expected_neighbors)

    def test_get_neighbors_outside_board_coord_empty(self):
        calculated_neighbors = set(self.board._get_neighbors((-5, 0, 5)))
        self.assertEqual(calculated_neighbors, set())

    def test_get_neighbors_center_coord_correct_neighbors(self):
        expected_neighbors = {(-1, 1, 0), (1, -1, 0), (-1, 0, 1), (1, 0, -1), (0, 1, -1), (0, -1, 1)}
        calculated_neighbors = set(self.board._get_neighbors((0, 0, 0)))
        self.assertEqual(calculated_neighbors, expected_neighbors)
