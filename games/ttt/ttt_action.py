from games.ttt.ttt_move import TTTMove

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

    INPUT_PROMPT = "Choose board, board position, and move(r,c;r,c;Move):  "

    def __init__(self, outer_pos, inner_pos, move):
        super().__init__()

        self.outer_pos = outer_pos
        self.inner_pos = inner_pos
        self.move = move

    @staticmethod
    def parse_action(input_str):
        try:
            outer_pos, inner_pos, move = input_str.split(';')
            outer_pos = tuple(map(int, outer_pos.split(',')))
            inner_pos = tuple(map(int, inner_pos.split(',')))
            move = TTTMove[move.upper()]
            action =TTTAction(outer_pos, inner_pos, move)
        except ValueError:
            action = None
        return action

    def __str__(self):
        return "{},{} -> {}".format(self.outer_pos, self.inner_pos, self.move)

    def __eq__(self, other):
        equal = False
        if isinstance(self, other.__class__):
            equal = (self.outer_pos == other.outer_pos and 
                        self.inner_pos == other.inner_pos and 
                        self.move == other.move)
        return equal

    def __hash__(self):
        return hash((self.outer_pos, self.inner_pos, self.move))

    def __deepcopy__(self, memo):
        new = TTTAction.__new__(TTTAction)
        memo[id(self)] = new
        new.outer_pos = self.outer_pos
        new.inner_pos = self.inner_pos
        new.move = self.move
        return new
