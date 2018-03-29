from willsmith.action import Action


class HavannahAction(Action):
    
    def __init__(self, coordinate, color):
        super().__init__()

        self.coord = coordinate
        self.color = color

    @staticmethod
    def prompt_for_action(legal_actions):
        color = legal_actions[0].color

        prompt = "Choose position for next {} move(x,y,z):  ".format(color)
        coord = tuple(map(int, input(prompt).split(',')))

        return HavannahAction(coord, color)

    def __eq__(self, other):
        equal = False
        if isinstance(self, other.__class__):
            equal = self.coord == other.coord and self.color == other.coord
        return equal

    def __hash__(self):
        return hash((self.coord, self.color))
