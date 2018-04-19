from unittest import TestCase

from games.gridworld.grid import Grid
from games.gridworld.gridworld import Gridworld
from games.gridworld.gridworld_action import GridworldAction
from games.gridworld.gridworld_direction import GridworldDirection
from games.gridworld.gridworld_examples import *


class TestGridworld(TestCase):
    
    def setUp(self):
        self.game = Gridworld(Grid(rewards_lookup, 0, walls, (4,3)), 
                                deterministic_transition)
        self.test_action = GridworldAction(GridworldDirection.UP)

    def test_gridworld_init_equal_games(self):
        other_game = standard_gridworld
        self.assertEqual(self.game, other_game)

    def test_gridwold_one_action_unequal_games(self):
        self.game._take_action(self.test_action)
        self.assertNotEqual(self.game, standard_gridworld)

    def test_gridworld_same_action_equal_games(self):
        self.game._take_action(self.test_action)
        other_game = standard_gridworld
        other_game._take_action(self.test_action)
        self.assertEqual(self.game, other_game)
