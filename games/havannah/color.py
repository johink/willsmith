from enum import Enum


class Color(Enum):
    """
    Represents the colors possible in a board position in Havannah.
    """

    BLANK = 1
    BLUE = 2
    RED = 3
    
    def __str__(self):
        return self.name

    def short_str(self):
        """
        Returns strings of length two for console printing format of the 
        Havannah board.
        """
        if self.name == "BLANK":
            val = "  "
        elif self.name == "BLUE":
            val = "bb"
        elif self.name == "RED":
            val = "rr"
        else:
            raise RuntimeError("Unexpected Color: {}".format(self.name))

        return val
