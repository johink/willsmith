from copy import copy

class HexNode:
    """
    """

    def __init__(self, color, coord, board_size):
        """
        """
        self.parent = coord
        self.size = 1

        self.color = color
        self.coord = coord
        self.neighbors = []
        self.num_corners = 0
        self.edge_labels = set()
        self._initialize_attributes(board_size)

    def _initialize_attributes(self, board_size):
        """
        """
        self.neighbors = self._get_neighbors(self.coord, board_size)

        if self._check_if_corner(self.coord, board_size):
            self.num_corners += 1

        if self._check_if_edge(self.coord, board_size):
            self.edge_labels.add(self._get_edge_label(self.coord))

    def _check_if_corner(self, coord, board_size):
        """
        Check if the coordinate is in a corner position on the board.

        Corner hex coordinates are always some combination of
        {board_size - 1, -board_size + 1, 0}
        """
        return (max(coord) == board_size - 1
                    and abs(min(coord)) == board_size - 1)

    def _check_if_edge(self, coord, board_size):
        """
        Check if the coordinate is on the edge of the board, excluding
        corners.

        Edges, excluding corners, always have one and only one coordinate
        that satisfies the condition - abs(coord) == board_size - 1
        """
        return ((abs(max(coord)) == board_size - 1)
                    ^ (abs(min(coord)) == board_size - 1))

    @classmethod
    def _get_edge_label(cls, coord):
        """
        Convert a hex coordinate into a label {-x, x, -y, y, -z, z}
        corresponding to the negative-most and positive-most rows of the
        given axis.

        For use on edge coordinates to determine the specific edge they
        lie upon.

        Non-edge coordinates are not anticipated.
        """
        index, _ = max(enumerate(coord), key = lambda x: abs(x[1]))
        mapping = {0: "x", 1: "y", 2: "z"}
        label = mapping[index]

        if abs(min(coord)) > max(coord):
            label = "-" + label
        return label


    @classmethod
    def _get_neighbors(cls, coord, board_size):
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
        new = HexNode.__new__(HexNode)
        memo[id(self)] = new
        new.parent = self.parent
        new.size = self.size
        new.color = self.color
        new.coord = self.coord
        new.neighbors = copy(self.neighbors)
        new.num_corners = self.num_corners
        new.edge_labels = copy(self.edge_labels)
        return new

    def __eq__(self, other):
        equal = False
        if isinstance(self, other.__class__):
            equal = (self.parent == other.parent
                        and self.size == other.size
                        and self.color == other.color
                        and self.coord == other.coord
                        and self.num_corners == other.num_corners
                        and self.edge_labels == other.edge_labels
                        and set(self.neighbors) == set(other.neighbors))
        return equal

    def __hash__(self):
        return hash((self.parent, self.size, self.color, self.coord,
                        frozenset(self.neighbors), self.num_corners,
                        self.edge_labels))
