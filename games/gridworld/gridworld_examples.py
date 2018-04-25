from games.gridworld.grid import Grid
from games.gridworld.gridworld import Gridworld
from games.gridworld.gridworld_direction import GridworldDirection
from games.gridworld.gridworld_action import GridworldAction


#####################################
#   Example transition functions
#####################################

def deterministic_transition(action):
    return [action], [1.0]

def shaky_transition(action):
    dirs = list(GridworldDirection)
    action_index = dirs.index(action.direction)

    side1 = GridworldAction(dirs[action_index - 1])
    side2 = GridworldAction(dirs[action_index + 1])

    return [action, side1, side2], [0.8, 0.2, 0.2]


#####################################
#   Example Gridworlds
#####################################

simple_terminals = {(3, 1) : -10, (3, 2) : 10}
simple_living_reward = -1
simple_walls = {(1, 1)}
simple_grid_size = (4,3)
simple_start = (0, 0)

simple_grid = Grid(simple_terminals, simple_living_reward, simple_walls, 
                    simple_grid_size)
simple_gridworld = Gridworld(simple_grid, deterministic_transition, 
                                simple_start)

classic_gridworld = Gridworld(simple_grid, shaky_transition, simple_start)

bridge_crossing_terminals = {(x, y) : -100
                                for x in range(1, 6) for y in [0, 2]}
bridge_crossing_terminals.update({(6, 1) : 10})
bridge_crossing_walls = {(0, 0), (0, 2), (6, 0), (6, 2)}
bridge_crossing_size = (7, 3)
bridge_crossing_start = (0, 1)

bridge_crossing_grid = Grid(bridge_crossing_terminals, simple_living_reward, 
                                bridge_crossing_walls, bridge_crossing_size)
bridge_crossing_gridworld = Gridworld(bridge_crossing_grid, shaky_transition,
                                        bridge_crossing_start)
