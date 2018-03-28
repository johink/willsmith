from games.havannah.color import Color


class HavannahBoard:
    """
    Encodes the gameboard using a dense graph representation stored as a 
    lookup table from cubic hex coordinates to hex colors.  

    Edges are implicit from each hex to all of its neighbors, calculated as 
    needed.

    The game is won by forming one of three configurations:
    (descriptions from Wikipedia - https://en.wikipedia.org/wiki/Havannah)
        Ring - a loop around one or more cells (no matter whether the encircled cells are occupied by any player or empty
        Bridge - which connects any two of the six corner cells of the board
        Fork -  which connects any three edges of the board; corner points are not considered parts of an edge
    """

    def __init__(self, board_size):
        self.board_size = board_size
        self.grid = self._generate_hexes(self.board_size)

    def take_action(self, action):
        pos, color = action
        self.grid[pos] = color

    def check_winner(self, action):
        pass

    def _generate_hexes(self, board_size):
        hexes = [(x, y, z) for x in range(-board_size + 1, board_size)
                           for y in range(-board_size + 1, board_size)
                           for z in range(-board_size + 1, board_size)
                                 if x + y + z == 0]
        return {key: Color.BLANK for key in hexes}

    def _check_bridge(self, pos, color):
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
        pass

    def _check_if_corner(self, pos):
        """
        Corner hex coordinates are always some combination of 
        {board_size - 1, -board_size + 1, 0}
        """
        return max(pos) == self.board_size - 1 and abs(min(pos)) == board_size - 1

    def _check_if_edge(self, pos):
        """
        Edges, excluding corners, always have one and only one coordinate 
        that satisfies the condition - abs(coord) == board_size - 1
        """
        return (abs(max(pos)) == self.board_size - 1) ^ (abs(min(pos)) == self.board_size - 1)

    def _get_neighbors(self, pos):
        """
        Calculate the neighbors of a hex, ensuring that coordinates are 
        within the board bounds.
        """
        neighbors = []
        for delta in [(-1, 1, 0), (1, -1, 0), (-1, 0, 1), (1, 0, -1), (0, 1, -1), (0, -1, 1)]:
            new_tuple = tuple([x + y for x,y in zip(pos, delta)])
            if max(new_tuple) < self.board_size and min(new_tuple) > -self.board_size:
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
