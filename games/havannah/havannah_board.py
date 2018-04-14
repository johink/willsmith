from copy import deepcopy
from collections import defaultdict
from itertools import combinations

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

    The game grid is encoded as a lookup table from coordinates to HexNode
    instances.  These nodes store their current color, a neighbor(edge) list,
    and other information relevant to win checking.

    As well as implementing a simple symmetric directed graph, the board also
    implements a union-find data structure.  As actions are taken on the
    board, a hex that is colored is unioned with its same color neighbors to
    create subsets that store progress towards a win condition.

    The coordinates start at (0,0,0) in the center of the board, and each
    coordinate on the board has the property that x + y + z = 0.
    """

    BOARD_SIZE = 10

    def __init__(self):
        self.grid = self._generate_hexes(self.BOARD_SIZE)
        self.winner = None

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

    def take_action(self, action):
        """
        Color the hex at the given coordinate.

        Also, before unioning the newly colored coordinate with all of its 
        same-color neighbors, it is checked to see if it meets the conditions 
        for a potential ring.  If so, after the union we check for this 
        particular win condition.

        This check is done here because the condition that leads to the 
        fastest check_ring implementation is easiest to detect AFTER an 
        action is taking and BEFORE that node is unioned with others.
        """
        self.grid[action.coord].color = action.color

        subset_dict = self._detect_potential_ring(action.coord, action.color)
        self._union_with_neighbors(action.coord, action.color)
        
        if subset_dict:
            self._check_ring(action.coord, action.color, subset_dict)

    def _union_with_neighbors(self, coord, color):
        """
        Call _union method on coord with each of its same color neighbors.
        """
        for neighbor in self.grid[coord].neighbors:
            if self.grid[neighbor].color == color:
                self._union(coord, neighbor)

    def _union(self, coord1, coord2):
        """
        Merge the smaller subset into the larger subset.

        This updates the nodes referenced by both coordinates to have the
        same representative element.

        The win condition information in the new root is updated to include
        the progress made by both sets.

        * Non-root nodes are not kept up-to-date with the win progress, they
        * are guaranteed to be out of date once they are unioned with any
        * other subset that has progress towards a win.
        *
        * Only reference root nodes when checking win progress.
        """
        # retrieve nodes referenced by the coordinates
        root1 = self.grid[self._find(coord1)]
        root2 = self.grid[self._find(coord2)]

        if root1 != root2:  # no need to union if they are already connected
            if root1.size < root2.size:     # ensure larger subset is first
                root1, root2 = root2, root1

            root2.parent = root1.coord
            root1.size += root2.size

            root1.update_win_progress(root2)

    def _find(self, coord):
        """
        Traverse from the node referenced by the coordinate to its root node.
        Then return the coordinate of the root node.

        During the traversal, parent coordinates are updated with coords
        from further up in the tree.  This has a flattening effect to keep
        the number of traversal steps low.
        """
        node = self.grid[coord]
        while not node.is_root():
            next_node = self.grid[node.parent]
            node.parent = next_node.parent
            node = next_node

        return node.coord

    def get_winner(self):
        return self.winner

    def check_for_winner(self, action):
        """
        Check if the last action taken triggered a win.

        This check relies on the union-find nodes keeping track of their
        progress towards a win condition for bridge and fork.
        """
        root = self.grid[self._find(action.coord)]
        if (root.num_corners >= 2 or len(root.edge_labels) >= 3):
            self.winner = action.color

    def _detect_potential_ring(self, coord, color):
        neighbors = [(x, self._find(x)) for x in self.grid[coord].neighbors
                        if self.grid[x].color == color]
        
        root_subsets = defaultdict(list)
        for coordinate, set_id in neighbors:
            root_subsets[set_id].append(coordinate)

        filtered_subsets = dict()
        for key in root_subsets.keys():
            if (len(root_subsets[key]) > 2 
                or (len(root_subsets[key]) == 2 
                    and root_subsets[key][0] not in self.grid[root_subsets[key][1]].neighbors)):
                filtered_subsets[key] = root_subsets[key]
        return filtered_subsets

    def _check_ring(self, coord, color, subset_dict):
        """
        Check if the ring win condition is satisfied.
        
        First check for the easier to detect ring condition when there is not 
        an in-set element adjacent to the newest node.

        Otherwise, check for the case where the adjacent node is also in-set.
        """
        if (self._check_ring_not_filled(coord, subset_dict) 
                or self._check_ring_filled(coord, color)):
            self.winner = color

    def _check_ring_not_filled(self, coord, subset_dict):
        """
        Check if the two in-set neighbors are in the same set and either:
            - they are not adjacent
            - not connected by another in-set neighbor
        """
        ring = False

        i = 0
        pairs = list(subset_dict.items())
        while not ring and i < len(pairs):
            group_id, coords = pairs[i]
            all_neighbors = set()
            for c in coords:
                all_neighbors.update(self.grid[c].neighbors)
            j = 0
            while not ring and j < len(coords):
                if c not in all_neighbors:
                    ring = True
                j += 1
            i += 1
        return ring

    def _check_ring_filled(self, coord, color):
        """
        Check if coloring the node at coord creates a ring in the case where 
        the ring is filled by its own color.

        This check is performed by finding the node inside the ring and then 
        checking if every one of its neighbors is in-set.
        """
        ring = False
        neighbors = [x for x in self.grid[coord].neighbors
                        if self.grid[x].color == color]
        i = 0
        pairs = list(combinations(neighbors, 2))
        while not ring and i < len(pairs):
            n1, n2 = pairs[i]
            in_common = set(self.grid[n1].neighbors) & set(self.grid[n2].neighbors) - {coord}

            if in_common:       # should only have one element
                ic_coord = in_common.pop()
                if ic_coord in self.grid[coord].neighbors:
                    coord_root = self._find(coord)
                    ic_neighbors = self.grid[ic_coord].neighbors
                    if len(ic_neighbors) == 6 and all([self._find(x) == coord_root for x in ic_neighbors]):
                        ring = True
            i += 1
        return ring
        

    def coord_to_color(self, col, slant):
        """
        Convert the axial coordinate to a color string.

        Used in the string representation of the board, which assigns an
        axial coordinate to each hex as it builds the board string.
        """
        return self.grid[hm.axial_to_cubic(col, slant)].color.short_str()

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

            # n, not n-1 steps back because of the call prior to the last loop
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
        new.grid = {k:deepcopy(v, memo) for k, v in self.grid.items()}
        new.winner = self.winner
        return new
