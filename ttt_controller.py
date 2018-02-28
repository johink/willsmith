from ttt_view import TTTView


class TTTViewController:
    """
    Controls the GUI for the TTT game and provides and interface for the 
    simulator to send/receive inputs/game actions.
    """

    def __init__(self, board_size):
        self.view = self.initialize_view(board_size)

    def initialize_view(self, board_size);
        view = TTTView(board_size)
        # call set_button_commands with proper callback
        return view
