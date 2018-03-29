from willsmith.action import Action


class TTTAction(Action):
    """
    Contains the data for a NestedTTT game action:

    Outer position - selects a board
    Inner position - selects a position on that board
    Move - X or O, corresponding to player's label

    The prompt_for_action method is overridden from the Action parent 
    class.  This functionality is used by the HumanAgent to provide 
    game-specific prompts on its turn.
    """

    def __init__(self, outer_pos, inner_pos, move):
        super().__init__()

        self.outer_pos = outer_pos
        self.inner_pos = inner_pos
        self.move = move

    @staticmethod
    def prompt_for_action(legal_actions):
        """
        Create a TTTAction based on user input.

        Prompts for a choice of inner board, then a position on that board.  
        Both positions are expected to be in the format "r,c" with no extra 
        characters, and both r,c are in the range [0,9).
        """
        move = legal_actions[0].move

        outer_input = "Choose board for {} move(row,col):  ".format(move)
        inner_input = "Choose board position for move(row,col):  "

        outer_pos = tuple(map(int, input(outer_input).split(',')))
        inner_pos = tuple(map(int, input(inner_input).split(',')))

        return TTTAction(outer_pos, inner_pos, move)

    def __eq__(self, other):
        equal = False
        if isinstance(self, other.__class__):
            equal = (self.outer_pos == other.outer_pos and 
                        self.inner_pos == other.inner_pos and 
                        self.move == other.move)
        return equal

    def __hash__(self):
        return hash((self.outer_pos, self.inner_pos, self.move))
