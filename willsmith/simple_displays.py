from willsmith.display_controller import DisplayController


class ConsoleDisplay(DisplayController):
    """
    A display controller that outputs the game on the command-line.

    Relies on the game's __str__ implementation.
    """

    CLEAR_TERMINAL = chr(27) + "[2J"

    def reset_display(self):
        print(self.CLEAR_TERMINAL)

    def update_display(self, game):
        print(self.CLEAR_TERMINAL)
        print(game)


class NoDisplay(DisplayController):
    """
    A display controller that does not render the game in any way.

    Useful for when attempting to run simulations as fast as possible.
    """

    def reset_display(self):
        pass

    def update_display(self, game):
        pass
