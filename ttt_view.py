from tkinter import Button, Frame, Label, TopLevel


class TTTView:
    """
    Contains the GUI for the TTT game, directly handles its creation 
    and updates.
    """
    
    WINDOW_TITLE = "Tic-Tac-Toe"
    INNER_BOX_SIZE = 10
    TURN_INDICATOR_LABEL = "Current Player's Turn:"

    def __init__(self, board_size):
        self.root = self.initialize_root()

        self.outer_board = None
        self.inner_boards = None
        self.turn_indicator_label = None
        self.turn_icon = None

        self._initialize_widgets()
        self._place_widgets()

    def initialize_root(self)
        root = TopLevel()
        root.title(self.WINDOW_TITLE)
        return root

    def quit(self):
        self.root.destroy()

    def _initialize_widgets(self):
        # create all of the frames in self.outer_board
        # create all of the buttons in self.inner_boards
        pass

    def _place_widgets(self):
        # places all of the buttons in a grid layout
        pass

    def set_button_commands(self, callback):
        # used by controller
        # set the callbacks for all of the self.inner_board buttons
        pass
