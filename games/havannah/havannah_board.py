from copy import deepcopy

from games.havannah.color import Color
from games.havannah.hex_node import HexNode

import games.havannah.hex_math as hm


class HavannahBoard:
    """
    The board for a game of Havannah, made up of hexes with sides typically 
    of length 10.

    The game is won by forming one of three configurations:
        Ring - connect a loop enclosing at least one hex
        Bridge - connect any two of the corner hexes
        Fork -  connect any three board edges, excluding corners

    Encodes the gameboard using a dense graph representation stored as a 
    lookup table from cubic hex coordinates to hexes.  Also keeps track 
    of the color of the winner if the game is complete.

    The coordinates start at (0,0,0) in the center of the board, and each 
    coordinate on the board has the property that x + y + z = 0.

    Edges are stored in the hexes, calculated as the board is created.
    """

    BEGINNER_BOARD_SIZE = 8
    BOARD_SIZE = 10

    def __init__(self):
        self.grid = self._generate_hexes(self.BOARD_SIZE)
        self.winner = None

    def take_action(self, action):
        self.grid[action.coord].color = action.color

    def get_winner(self):
        return self.winner

    def _generate_hexes(self, board_size):
        """
        Generate a list of cubic coordinates for every possible position 
        on the board.

        Then return a dictionary from each coordinate to a hex.
        """
        hexes = [(x, y, z) for x in range(-board_size + 1, board_size)
                           for y in range(-board_size + 1, board_size)
                           for z in range(-board_size + 1, board_size)
                                 if x + y + z == 0]
        return {key: HexNode(Color.BLANK, key, board_size) for key in hexes}

    def check_for_winner(self, action):
        if self._check_if_won(action):
            self.winner = action.color
    
    def _check_if_won(self, action):
        coord, color = action.coord, action.color
        return (self._check_bridge(coord, color)
                    or self._check_fork(coord, color)
                    or self._check_ring(coord, color))

    def _check_bridge(self, coord, color):
        """
        Checks the bridge win condition, described in the class docstring.
        """
        fringe = {coord}
        win = False
        visited = set()
        corner_count = 0

        while fringe and not win:
            current = fringe.pop()
            visited.add(current)
            if self._check_if_corner(current):
                corner_count += 1
                if corner_count >= 2:
                    win = True
            neighbors = [x for x in self.grid[current].neighbors 
                            if self.grid[x].color == color 
                                and x not in visited 
                                and x not in fringe]
            fringe.update(neighbors)
        return win

    def _check_fork(self, coord, color):
        """
        Checks the fork win condition, described in the class docstring.
        """
        fringe = {coord}
        win = False
        visited = set()
        edge_set = set()
        unique_edge_count = 0

        while fringe and not win:
            current = fringe.pop()
            visited.add(current)
            if self._check_if_edge(current):
                edge_label = self._get_edge_label(current)
                if edge_label not in edge_set:
                    unique_edge_count += 1
                    edge_set.add(edge_label)
                    if unique_edge_count >= 3:
                        win = True
            neighbors = [x for x in self.grid[current].neighbors 
                            if self.grid[x].color == color 
                                and x not in visited 
                                and x not in fringe]
            fringe.update(neighbors)

        return win

    def _check_ring(self, coord, color):
        """
        Checks the ring win condition, described in the class docstring.
        """
        # Initial state:  Just-placed node is prior node, then for each neighbor -> run algorithm
        # with neighbor as current node
        neighbors = [x for x in self.grid[coord].neighbors
                        if self.grid[x].color == color]
        win = False

        for neighbor in neighbors:
            win = self._recursive_ring(color, coord, neighbor, set())
            if win:
                break

        return win

    def _recursive_ring(self, color, prior_coord, current_coord, visited_set):
        """
        # Assume we have a prior node, and a current node
        # If we traverse only the neighbors of current node which are not adjacent
        # to prior node, and we eventually reach a visited node, we must have surrounded
        # other nodes
        """
        if current_coord in visited_set:
            return True

        previous_neighbors = set(self.grid[prior_coord].neighbors)
        previous_neighbors.add(prior_coord)

        valid_neighbors = {x for x in self.grid[current_coord].neighbors
                            if self.grid[x].color == color
                            and x not in previous_neighbors}

        if not valid_neighbors:
            win = False
        else:
            visited_set.add(current_coord)
            for neighbor in valid_neighbors:
                win = self._recursive_ring(color, current_coord, neighbor, visited_set)
                if win:
                    break

            visited_set.remove(current_coord)

        return win

    def _check_if_corner(self, coord):
        """
        Check if the coordinate is in a corner position on the board.

        Corner hex coordinates are always some combination of 
        {board_size - 1, -board_size + 1, 0}
        """
        return (max(coord) == self.BOARD_SIZE - 1 
                    and abs(min(coord)) == self.BOARD_SIZE - 1)

    def _check_if_edge(self, coord):
        """
        Check if the coordinate is on the edge of the board, excluding 
        corners.

        Edges, excluding corners, always have one and only one coordinate 
        that satisfies the condition - abs(coord) == board_size - 1
        """
        return ((abs(max(coord)) == self.BOARD_SIZE - 1) 
                    ^ (abs(min(coord)) == self.BOARD_SIZE - 1))

    def _get_edge_label(self, coord):
        """
        Convert a hex coordinate into a label {-x, x, -y, y, -z, z} 
        corresponding to the negative-most and positive-most rows of the 
        given axis.  
        
        For use on edge coordinates to determine the specific edge they 
        lie upon.  Non-edge coordinates are not anticipated.
        """
        index, _ = max(enumerate(coord), key = lambda x: abs(x[1]))
        mapping = {0: "x", 1: "y", 2: "z"}
        label = mapping[index]

        if abs(min(coord)) > max(coord):
            label = "-" + label
        return label

    def coord_to_color(self, col, slant):
        """
        Convert the axial coordinate to a color string.

        Used in the string representation of the board, which assigns an 
        axial coordinate to each hex as it builds the board string.
        """
        return str(self.grid[hm.axial_to_cubic(col, slant)].color)

    def __str__(self):
        """
        Return a string representation of the game board that looks like:

                  __
               __/  \__
            __/  \__/  \__
         __/  \__/  \__/  \__
        /  \__/  \__/  \__/  \
        \__/  \__/  \__/  \__/
        /  \__/  \__/  \__/  \
        \__/  \__/bb\__/  \__/
        /  \__/  \__/  \__/  \
        \__/rr\__/  \__/  \__/
        /  \__/  \__/  \__/  \
        \__/  \__/  \__/  \__/
           \__/  \__/  \__/
              \__/  \__/
                 \__/
        """
        n = self.BOARD_SIZE
        f = self.coord_to_color
        col = 0
        slant = -(n-1)

        result = []
        for i in range(n):
            sub_result = []
            sub_result.append(" " * ((3 * n - 2) - 3 * i) + "__")
            for j in range(i):
                sub_result.append("/{}\\__".format(f(col, slant)))
                col, slant = hm.axial_east(col, slant)

            col, slant = hm.axial_n_moves(hm.axial_west, i, col, slant)
            # top coord was always off because of the top row where 
            # there are no hex values but only the __ of the topmost hex
            if i != 0:
                col, slant = hm.axial_s_west(col, slant)

            result.append("".join(sub_result))

        for i in range(n):
            sub_result = []
            sub_result.append("/{}\\".format(f(col, slant)))
            col, slant = hm.axial_east(col, slant)
            for j in range(n - 1):
                sub_result.append("__/{}\\".format(f(col, slant)))
                col, slant = hm.axial_east(col, slant)

            result.append("".join(sub_result))

            # n, not n-1 steps back because of the format call on ln 205
            col, slant = hm.axial_n_moves(hm.axial_west, n, col, slant)
            col, slant = hm.axial_s_east(col, slant)

            sub_result = []
            sub_result.append("\\__/")
            for j in range(n - 1):
                sub_result.append("{}\\__/".format(f(col, slant)))
                col, slant = hm.axial_east(col, slant)

            col, slant = hm.axial_n_moves(hm.axial_west, n - 1, col, slant)
            col, slant = hm.axial_s_west(col, slant)
            result.append("".join(sub_result))

        # not sure why the previous computation leaves the coordinate an 
        # extra hex west, but this is the correction needed
        col, slant = hm.axial_east(col, slant)
        for i in range(1, n):
            sub_result = []
            sub_result.append(" " * 3 * i + "\\__/")
            for j in range(n - 1 - i):
                sub_result.append("{}\\__/".format(f(col,slant)))
                col, slant = hm.axial_east(col, slant)

            col, slant = hm.axial_n_moves(hm.axial_west, n - 1 - i, col, slant)
            col, slant = hm.axial_s_east(col, slant)

            result.append("".join(sub_result))

        return "\n".join(result)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        equal = False
        if isinstance(self, other.__class__):
            equal = self.winner == other.winner and self.grid == other.grid
        return equal

    def __hash__(self):
        return hash((self.winner, frozenset(self.grid)))

    def __deepcopy__(self, memo):
        new = HavannahBoard.__new__(HavannahBoard)
        memo[id(self)] = new
        new.grid = self._grid_deepcopy(self.grid, memo)
        new.winner = self.winner
        return new

    def _grid_deepcopy(self, grid, memo):
        """
        Deepcopy the grid dictionary.

        Manually iterates through to save the overhead calling deepcopy on 
        the dictionary while still calling the custom deepcopy for Hex.
        """
        return {k:deepcopy(v, memo) for k, v in grid.items()}
