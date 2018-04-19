from games.gridworld.gridworld_direction import GridworldDirection

from willsmith.action import Action


class GridworldAction(Action):
    """
    Contains the data for a Gridworld game action:

    direction - which direction the agent wants to move in
    """

    INPUT_PROMPT = "Choose a direction[up, right, down, left]:  "

    def __init__(self, direction):
        super().__init__()
        self.direction = direction

    @staticmethod
    def parse_action(input_str):
        try:
            direction = GridworldDirection[input_str.upper()]
            action = GridworldAction(direction)
        except ValueError:
            action = None

        return action

    def __str__(self):
        return str(self.direction)

    def __eq__(self, other):
        equal = False
        if isinstance(self, other.__class__):
            equal = self.direction == other.direction
        return equal

    def __hash__(self):
        return hash((self.direction))

    def __deepcopy__(self, memo):
        new = GridworldAction.__new__(GridworldAction)
        memo[id(self)] = new
        new.direction = self.direction
        return new
