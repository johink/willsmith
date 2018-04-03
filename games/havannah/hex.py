from copy import copy


class Hex:
    """
    Represents the data needed for a hex in Havannah, and a node in the graph 
    of the board.

    Keeps track of the color of the hex and the coordinates of each of its 
    neighbors, or edges.
    """

    def __init__(self, color, coord, board_size):
        """
        Store the color and call to calculate the coordinates of each 
        neighboring hex, ensuring they stay within the bounds of the board.
        """
        self.color = color
        self.neighbors = self._get_neighbors(coord, board_size)

    def _get_neighbors(self, coord, board_size):
        """
        Calculate the neighbors of a hex, ensuring that coordinates are 
        within the board bounds.
        """
        neighbors = []
        for delta in [(-1, 1, 0), (1, -1, 0), (-1, 0, 1), (1, 0, -1), (0, 1, -1), (0, -1, 1)]:
            # could optimize this by running a for loop and keeping track of 
            # min and max as the addition is done
            new_tuple = tuple([x + y for x,y in zip(coord, delta)])
            if max(new_tuple) < board_size and min(new_tuple) > -board_size:
                neighbors.append(new_tuple)
        return neighbors

    def __deepcopy__(self, memo):
        new = Hex.__new__(Hex)
        memo[id(self)] = new
        new.color = self.color
        new.neighbors = copy(self.neighbors)
        return new

    def __eq__(self, other):
        equal = False
        if isinstance(self, other.__class__):
            equal = (self.color == other.color and 
                        set(self.neighbors) == set(other.neighbors))
        return equal

    def __hash__(self):
        return hash((self.color, frozenset(self.neighbors)))
