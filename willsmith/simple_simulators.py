from willsmith.simulator import Simulator


class ConsoleSimulator(Simulator):
    """
    A simulator that displays the game on the command-line.

    Expects the game to have a __str__ implementation.
    """

    CLEAR_TERMINAL = chr(27) + "[2J"

    def display_game(self):
        print(self.CLEAR_TERMINAL)
        print(self.current_game)


class NoDisplaySimulator(Simulator):
    """
    A simulator that does not render the gamestate.

    Useful for when attempting to run multiple simulations in a row as fast 
    as possible.
    """

    def display_game(self):
        pass
