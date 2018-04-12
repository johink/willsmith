"""
A pair of generic display controllers that can used for almost any game.
"""


from willsmith.display_controller import DisplayController


class ConsoleDisplay(DisplayController):
    """
    A display controller that outputs the game on the command-line.

    Relies on the game's __str__ implementation.
    """

    CLEAR_TERMINAL = chr(27) + "[2J"

    def start(self, is_main):
        pass

    def reset_display(self, game):
        print(self.CLEAR_TERMINAL)

    def update_display(self, game, action):
        print(self.CLEAR_TERMINAL)
        print(game)


class NoDisplay(DisplayController):
    """
    A display controller that does not render the game in any way.

    Useful for when attempting to run simulations as fast as possible.
    """

    def start(self, is_main):
        pass

    def reset_display(self, game):
        pass

    def update_display(self, game, action):
        pass
