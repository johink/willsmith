from games.havannah.color import Color

from willsmith.action import Action


class HavannahAction(Action):
    """
    Contains the data for a Havannah game action:

    coordinate - cubic hex coordinate in the form (x,y,z)
    color - Blue or Red, corresponding to the player's label
    """

    INPUT_PROMPT = "Choose position and color(x,y,z;Color):  "
    
    def __init__(self, coordinate, color):
        super().__init__()

        self.coord = coordinate
        self.color = color

    @staticmethod
    def parse_action(input_str):
        try:
            coord, color = input_str.split(';')
            coord = tuple(map(int, coord.split(',')))
            color = Color[color.upper()]
            action = HavannahAction(coord, color)
        except ValueError:
            action = None

        return action

    def __str__(self):
        return "{} -> {}".format(self.coord, self.color)

    def __repr__(self):
        return self.__str__()

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
