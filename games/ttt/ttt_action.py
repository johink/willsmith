from willsmith.action import Action


class TTTAction(Action):
    """
    Contains the information for a NestedTTT game action.

    Outer position - selects a board
    Inner position - selects a position on that board
    Move - X or O, corresponding to player's label
    """

    def __init__(self, outer_pos, inner_pos, move):
        super().__init__()

        self.outer_pos = outer_pos
        self.inner_pos = inner_pos
        self.move = move

    @staticmethod
    def prompt_for_action(legal_actions):
        move = legal_actions[0].move

        outer_input = "Choose board for {} move(row,col):  ".format(move)
        inner_input = "Choose board position for move(row,col):  "

        outer_pos = tuple(map(int, input(outer_input).split(',')))
        inner_pos = tuple(map(int, input(inner_input).split(',')))

        return TTTAction(outer_pos, inner_pos, move)

    def __eq__(self, other):
        """
        Needed for comparing actions that are equal but not the same instance 
        in memory.
        Specifically, for testing if the return value from prompt_for_action 
        is in the list of legal actions.
        """
        equal = False
        if isinstance(self, other.__class__):
            equal = (self.outer_pos == other.outer_pos and 
                        self.inner_pos == other.inner_pos and 
                        self.move == other.move)
        return equal

    def __hash__(self):
        """
        Defining a custom equality check requires this definition as well.
        """
        return hash((self.outer_pos, self.inner_pos, self.move))
