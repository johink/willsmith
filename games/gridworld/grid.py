from collections.abc import MutableMapping
from copy import deepcopy

from games.gridworld.gridworld_direction import GridworldDirection


class Grid(MutableMapping):
    """
    """

    def __init__(self, terminal_states, living_reward, walls, size):
        self.size = size
        self._grid = {(x, y) : self.GridworldSquare((x, y), 
                                    (x, y) in terminal_states,
                                    terminal_states.get((x, y), living_reward))
                for x in range(self.size[0]) for y in range(self.size[1])
                    if (x, y) not in walls}

    def __getitem__(self, key):
        return self._grid[key]

    def __setitem__(self, key, value):
        self._grid[key] = value

    def __delitem__(self, key):
        del self._grid[key]

    def __iter__(self):
        return iter(self._grid)

    def __len__(self):
        return len(self._grid)

    def __eq__(self, other):
        equal = False
        if isinstance(self, other.__class__):
            equal = (self.size == other.size
                        and self._grid == other._grid)
        return equal

    def __hash__(self):
        return hash((self.size, frozenset(self._grid)))

    def __deepcopy__(self, memo):
        new = Grid.__new__(Grid)
        memo[id(self)] = new
        new.size = self.size
        new._grid = {k : deepcopy(v, memo) for k, v in self._grid.items()}
        return new
    
        
    class GridworldSquare:
        """
        Holds the information for a single square in a Gridworld Grid.
        """

        def __init__(self, location, terminal, reward):
            self.location = location
            self.terminal = terminal
            self.reward = reward

        def __eq__(self, other):
            equal = False
            if isinstance(self, other.__class__):
                equal = (self.location == other.location
                            and self.terminal == other.terminal
                            and self.reward == other.reward)
            return equal

        def __hash__(self):
            return hash((self.location, self.terminal, self.reward))

        def __deepcopy__(self, memo):
            new = Grid.GridworldSquare.__new__(Grid.GridworldSquare)
            memo[id(self)] = new

            new.location = self.location
            new.terminal = self.terminal
            new.reward = self.reward
            return new
