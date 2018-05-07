from copy import copy, deepcopy
from random import choices

from games.gridworld.gridworld_direction import GridworldDirection
from games.gridworld.gridworld_display import GridworldDisplay

from willsmith.mdp import MDP


class Gridworld(MDP):
    """
    A wrapper for the standard example of a Markov Decision Process.  
    """

    DISPLAY = GridworldDisplay

    def __init__(self, grid, transition_func, agent_start_pos, use_display):
        """
        """
        super().__init__(use_display)

        self.grid = grid
        self.transition_func = transition_func
        self.action_space = list(GridworldDirection)
        self.start_pos = agent_start_pos
        self._reset()

    def _reset(self):
        self.terminal = False
        self.player_pos = self.start_pos
        self.previous_positions = []

    def _step(self, action):
        actions, weights = self.transition_func(action)
        # choices returns a list but we only ever return one result
        actual_action = choices(actions, weights = weights, k = 1)[0]

        pos, reward, terminal = self._determine_result(actual_action)
        self.previous_positions.append(self.player_pos)
        self.player_pos = pos
        self.terminal = terminal

        return reward, terminal

    def _undo(self, action):
        if self.terminal:
            self.terminal = False
        
        self.player_pos = self.previous_positions.pop()

    def is_terminal(self):
        return self.terminal

    def get_action_space(self):
        return list(self.action_space)

    def _determine_result(self, action):
        """
        """
        x, y = self.player_pos
        dx, dy = GridworldDirection.get_offset(action)
        next_coord = (x + dx, y + dy)

        result_pos = self.player_pos
        if self._valid_position(next_coord):
            result_pos = next_coord

        next_square = self.grid[result_pos]
        reward, terminal = next_square.reward, next_square.terminal
        return result_pos, reward, terminal

    def _valid_position(self, coord):
        return coord in self.grid

    def __str__(self):
        results = []
        for y in range(self.grid.size[1]-1, -1, -1):
            row = []
            for x in range(self.grid.size[0]):
                square = "   "
                if (x,y) in self.grid:
                    if self.player_pos == (x, y):
                        square = "[A]"
                    elif self.grid[(x, y)].terminal:
                        square = "[T]"
                    else:
                        square = "[ ]"
                row.append(square)
            results.append("".join(row))
        return "\n".join(results)

    def __eq__(self, other):
        equal = False
        if isinstance(self, other.__class__):
            equal = (super().__eq__(other)
                        and self.grid == other.grid
                        and self.transition_func == other.transition_func
                        and self.terminal == other.terminal
                        and self.action_space == other.action_space
                        and self.start_pos == other.start_pos
                        and self.player_pos == other.player_pos
                        and self.previous_positions == self.previous_positions)
        return equal

    def __hash__(self):
        return hash((self.grid, self.transition_func, self.action_space, 
                        self.terminal, self.start_pos, self.player_pos, 
                        self.previous_positions))

    def __deepcopy__(self, memo):
        new = Gridworld.__new__(Gridworld)
        memo[id(self)] = new
        self.deepcopy_mdp_attrs(new)

        new.grid = deepcopy(self.grid, memo)
        new.transition_func = self.transition_func
        new.action_space = copy(self.action_space)
        new.terminal = self.terminal

        new.previous_positions = copy(self.previous_positions)
        new.start_pos = self.start_pos
        new.player_pos = self.player_pos

        return new
