from games.havannah.color import Color


class HavannahBoard:
    """
    The board for a game of Havannah, made up of hexes with sides typically 
    of length 10.

    The game is won by forming one of three configurations:
    (descriptions from Wikipedia - https://en.wikipedia.org/wiki/Havannah)
        Ring - loop around one or more cells, where the encircled cells are 
                occupied by the other player or empty
        Bridge - connect any two of the six corner cells of the board
        Fork -  connect any three edges of the board; corner points are not 
                    considered parts of an edge

    Encodes the gameboard using a dense graph representation stored as a 
    lookup table from cubic hex coordinates to hex colors.  Also keeps track 
    of the color of the winner if the game is over.

    Edges between graph nodes are implicit from each hex to all of its 
    neighbors, calculated as needed.
    """

    BEGINNER_BOARD_SIZE = 8
    BOARD_SIZE = 10

    def __init__(self):
        self.grid = self._generate_hexes(self.BOARD_SIZE)
        self.winner = None

    def take_action(self, action):
        self.grid[action.coord] = action.color

    def get_winner(self, action):
        return self.winner

    def _generate_hexes(self, board_size):
        """
        """
        hexes = [(x, y, z) for x in range(-board_size + 1, board_size)
                           for y in range(-board_size + 1, board_size)
                           for z in range(-board_size + 1, board_size)
                                 if x + y + z == 0]
        return {key: Color.BLANK for key in hexes}

    def _check_bridge(self, pos, color):
        """
        Checks the bridge win condition, described in the class docstring.
        """
        fringe = [pos]
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
            neighbors = [x for x in self._get_neighbors(current) if self.grid[x] == color and x not in visited]
            fringe.extend(neighbors)

        return win

    def _check_fork(self, pos, color):
        """
        Checks the fork win condition, described in the class docstring.
        """
        fringe = [pos]
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
            neighbors = [x for x in self._get_neighbors(current) if self.grid[x] == color and x not in visited]
            fringe.extend(neighbors)

        return win

    def _check_ring(self, pos, color):
        """
        Checks the ring win condition, described in the class docstring.
        """
        pass

    def _check_if_corner(self, pos):
        """
        Check if the coordinate is in a corner position on the board.

        Corner hex coordinates are always some combination of 
        {board_size - 1, -board_size + 1, 0}
        """
        return max(pos) == self.BOARD_SIZE - 1 and abs(min(pos)) == self.BOARD_SIZE - 1

    def _check_if_edge(self, pos):
        """
        Check if the coordinate is on the edge of the board, excluding 
        corners.

        Edges, excluding corners, always have one and only one coordinate 
        that satisfies the condition - abs(coord) == board_size - 1
        """
        return (abs(max(pos)) == self.BOARD_SIZE - 1) ^ (abs(min(pos)) == self.BOARD_SIZE - 1)

    def _get_neighbors(self, pos):
        """
        Calculate the neighbors of a hex, ensuring that coordinates are 
        within the board bounds.
        """
        neighbors = []
        for delta in [(-1, 1, 0), (1, -1, 0), (-1, 0, 1), (1, 0, -1), (0, 1, -1), (0, -1, 1)]:
            new_tuple = tuple([x + y for x,y in zip(pos, delta)])
            if max(new_tuple) < self.BOARD_SIZE and min(new_tuple) > -self.BOARD_SIZE:
                neighbors.append(new_tuple)
        return neighbors

    def _get_edge_label(self, pos):
        """
        Convert a hex coordinate into a label {-x, x, -y, y, -z, z} 
        corresponding to the negative-most and positive-most rows of the 
        given axis.  
        
        For use on edge coordinates to determine the specific edge they 
        lie upon.  Non-edge coordinates are not anticipated.
        """
        index, _ = max(enumerate(pos), key = lambda x: x[1])
        mapping = {0: "x", 1: "y", 2: "z"}
        label = mapping[index]

        if abs(min(pos)) > max(pos):
            label = "-" + label
        return label
