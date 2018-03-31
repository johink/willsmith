from games.havannah.color import Color
import games.havannah.hex_math as hm

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
    BOARD_SIZE = 3

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

    def coord_to_color(self, col, slant):
        """
        axial coord -> hex coord
        hex coord -> color
        color -> string
        """
        return str(col) + str(slant)

    def __str__(self):
        """
        top rows function
        " " * ((3n - 2) - 3i) + "__" + "/<>\__" * i | i [0,n-1]
        
        middle rows function
        repeat n times:
        "/<>\" + "__/<>\" * (n-1)
        "\__/" + "<>\__/" * (n-1)
        
        bottom rows function
        " " * 3i + "\__/" + "<>\__/" * (n-1-i) | i <- [1, n-1]
        
        7 space,        __
        4 space,     __/0@\__   
        1 space,  __/!!\__/1@\__
        0 space, /@0\__/0!\__/2@\
        0 space, \__/!0\__/1!\__/
        0 space, /@1\__/00\__/2!\
        0 space, \__/!1\__/10\__/
        0 space, /@2\__/01\__/20\
        0 space, \__/!2\__/11\__/
        3 space,    \__/02\__/
        6 space,       \__/

        negative numbers are shift char for number
        """
        n = self.BOARD_SIZE
        f = self.coord_to_color
        result = []
        col = 0
        slant = -(n-1)
        print("{},{}".format(col,slant))
        for i in range(n):
            sub_result = []
            sub_result.append(" " * ((3 * n - 2) - 3 * i) + "__")
            for j in range(i):
                print("{},{}".format(col,slant))
                sub_result.append("/{}\\__".format(f(col, slant)))
                col, slant = hm.axial_east(col, slant)

            col, slant = hm.axial_n_moves(hm.axial_west, i, col, slant)
            # top coord was always off because of the top row where 
            # there are no hex values but only the __ of the topmost hex
            if i != 0:
                col, slant = hm.axial_s_west(col, slant)
            result.append("".join(sub_result))

        col = -(n-1)
        slant = 0
        for i in range(n):
            sub_result = []
            sub_result.append("/{}\\".format(f(col, slant)))
            col, slant = hm.axial_east(col, slant)
            for j in range(n-1):
                sub_result.append("__/{}\\".format(f(col, slant)))
                col, slant = hm.axial_east(col, slant)

            result.append("".join(sub_result))

            col, slant = hm.axial_n_moves(hm.axial_west, n-1, col, slant)
            col, slant = hm.axial_s_east(col, slant)
            sub_result = []
            sub_result.append("\\__/")
            for j in range(n-1):
                sub_result.append("{}\\__/".format(f(col, slant)))
                col, slant = hm.axial_east(col, slant)

            col, slant = hm.axial_n_moves(hm.axial_west, n-1, col, slant)
            col, slant = hm.axial_s_west(col, slant)
            result.append("".join(sub_result))

        col = -(n-1) + 1
        slant = (n-1)
        for i in range(1, n):
            sub_result = []
            sub_result.append(" " * 3 * i + "\\__/")
            for j in range(n-1-i):
                sub_result.append("{}\\__/".format(f(col,slant)))
                col, slant = hm.axial_east(col, slant)

            col, slant = hm.axial_n_moves(hm.axial_west, n-1-i, col, slant)
            col, slant = hm.axial_s_east(col, slant)
            result.append("".join(sub_result))

        return "\n".join(result)


