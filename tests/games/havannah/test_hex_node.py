from unittest import TestCase

from games.havannah.color import Color
from games.havannah.hex_node import HexNode


class TestHexNode(TestCase):
    
    def setUp(self):
        self.board_size = 4

    def test_get_neighbors_edge_coord_neighbors_inside_board(self):
        expected_neighbors = {(-3, 1, 2), (-2, 0, 2), (-2, -1, 3)}
        calculated_neighbors = set(HexNode._get_neighbors((-3, 0, 3), self.board_size))
        self.assertEqual(calculated_neighbors, expected_neighbors)

    def test_get_neighbors_outside_board_coord_empty(self):
        calculated_neighbors = set(HexNode._get_neighbors((-5, 0, 5), self.board_size))
        self.assertEqual(calculated_neighbors, set())

    def test_get_neighbors_center_coord_correct_neighbors(self):
        expected_neighbors = {(-1, 1, 0), (1, -1, 0), (-1, 0, 1), (1, 0, -1), (0, 1, -1), (0, -1, 1)}
        calculated_neighbors = set(HexNode._get_neighbors((0, 0, 0), self.board_size))
        self.assertEqual(calculated_neighbors, expected_neighbors)
