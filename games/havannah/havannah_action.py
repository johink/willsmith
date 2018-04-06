from willsmith.action import Action


class HavannahAction(Action):
    """
    Contains the data for a Havannah game action:

    coordinate - cubic hex coordinate in the form (x,y,z)
    color - Blue or Red, corresponding to the player's label
    """
    
    def __init__(self, coordinate, color):
        super().__init__()

        self.coord = coordinate
        self.color = color

    @staticmethod
    def prompt_for_action(legal_actions):
        """
        Create a HavannahAction based on user input.

        Prompts for the hex coordinate, expected to be in the form "x,y,z" 
        with no extra characters, and all three values are expected in the 
        range [0,board size).
        """
        color = legal_actions[0].color

        prompt = "Choose position for next {} move(x,y,z):  ".format(color)
        coord = tuple(map(int, input(prompt).split(',')))

        return HavannahAction(coord, color)

    def __str__(self):
        return "{} : {}".format(self.coord, self.color)

    def __eq__(self, other):
        equal = False
        if isinstance(self, other.__class__):
            equal = self.coord == other.coord and self.color == other.color
        return equal

    def __hash__(self):
        return hash((self.coord, self.color))

    def __deepcopy__(self, memo):
        new = HavannahAction.__new__(HavannahAction)
        memo[id(self)] = new
        new.coord = self.coord
        new.color = self.color
        return new
