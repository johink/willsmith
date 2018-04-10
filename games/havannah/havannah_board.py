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
        self._union_with_neighbors(action.coord, action.color)

    def _union(self, first_coord, second_coord):
        """
        Merge two sets within the board to have the same root.

        Also updates root information on the relevant progress towards a win by
        fork or bridge.
        """
        root1 = self.grid[self._find(first_coord)]
        root2 = self.grid[self._find(second_coord)]

        if root1 != root2:
            if root1.size < root2.size:
                root1, root2 = root2, root1

            root2.parent = root1.coord
            root1.size += root2.size
            root1.num_corners += root2.num_corners
            root1.edge_labels.update(root2.edge_labels)

    def _find(self, coord):
        """
        Traverse from a coordinate to the root node, updating parent nodes along
        the way to flatten the node tree

        Returns a coordinate instead of a node, for a consistent public interface
        """
        node = self.grid[coord]
        while node.parent != node.coord:
            next_node = self.grid[node.parent]
            node.parent = next_node.parent
            node = next_node

        return node.coord

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

    def _union_with_neighbors(self, coord, color):
        neighbors = [x for x in self.grid[coord].neighbors
                        if self.grid[x].color == color]

        for neighbor in neighbors:
            self._union(coord, neighbor)

    def check_for_winner(self, action):
        """
        """
        coord, color = action.coord, action.color

        root = self.grid[self._find(coord)]
        if (root.num_corners >= 2                       # bridge
                or len(root.edge_labels) >= 3           # fork
                or self._check_ring(coord, color)):     # ring
            self.winner = color

    def _check_ring(self, coord, color):
        """
        """
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
        If we traverse only the neighbors of current node which are not 
        adjacent to prior node, and we eventually reach a visited node, we 
        must have surrounded other nodes
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
