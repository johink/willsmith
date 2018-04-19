from games.gridworld.grid import Grid
from games.gridworld.gridworld import Gridworld


rewards_lookup = {(3, 1): -10, (3, 2): 10}
walls = [(1,1)]

def deterministic_transition(action):
    return [action], [1.0]

simple_grid = Grid(rewards_lookup, 0, walls, (4,3))

standard_gridworld = Gridworld(simple_grid, deterministic_transition)
