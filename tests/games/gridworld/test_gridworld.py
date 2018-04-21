from tests.games.game_testcase import GameTestCase

from games.gridworld.grid import Grid
from games.gridworld.gridworld import Gridworld
from games.gridworld.gridworld_action import GridworldAction
from games.gridworld.gridworld_direction import GridworldDirection
from games.gridworld.gridworld_examples import *


class TestGridworld(GameTestCase):
    
    def setUp(self):
        super().setUp()
        self.game = Gridworld(Grid(rewards_lookup, 0, walls, (4,3)), 
                                deterministic_transition)
        self.test_action = GridworldAction(GridworldDirection.UP)

    def test_game_equality(self):
        self._test_game_equality()
