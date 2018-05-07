from tests.games.mdp_testcase import MDPTestCase

from games.gridworld.grid import Grid
from games.gridworld.gridworld import Gridworld
from games.gridworld.gridworld_direction import GridworldDirection
from games.gridworld.gridworld_examples import *


class TestGridworld(MDPTestCase):
    
    def setUp(self):
        super().setUp()
        self.mdp = Gridworld(Grid(simple_terminals, 0, simple_walls, (4,3)), 
                                deterministic_transition, (0, 0), None)
        self.test_action = GridworldDirection.UP

    def test_mdp_equality(self):
        self._test_mdp_equality()

    def test_last_position_stays_in_sync(self):
        self.assertFalse(self.mdp.previous_positions)
        self.mdp.step(self.test_action)
        self.assertEqual(self.mdp.previous_positions[0], (0, 0))
