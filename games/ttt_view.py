from tkinter import Button, Frame, Label, Tk

from games.ttt_board import TTTBoard
from games.ttt_move import TTTMove


class TTTView:
    """
    Contains the GUI for the TTT game, directly handles its creation 
    and updates for the visual components.  
    Returns user actions to its controller for processing and updating game 
    state, then receives the updates and displays them.
    """
    
    WINDOW_TITLE = "Tic-Tac-Toe"
    TURN_INDICATOR_LABEL = "Current Player's Turn:"
    BOARD_BACKGROUND_1 = "#C8B22B"
    BOARD_BACKGROUND_2 = "#000000"

    def __init__(self):
        self.root = self.initialize_root()

        self.outer_board = None
        self.inner_boards = None
        self.turn_indicator_label = None
        self.turn_icon = None

        self._initialize_widgets()
        self._place_widgets()

    def initialize_root(self):
        root = Tk()
        root.title(self.WINDOW_TITLE)
        return root

    def quit(self):
        self.root.destroy()

    def _initialize_widgets(self):
        self._initialize_outer_board()
        self._initialize_inner_boards()
        self._style_inner_boards()
        self._initialize_informational_labels()

    def _place_widgets(self):
        self._place_board(self.outer_board)
        self._place_inner_boards()
        self._place_informational_labels()

    def _initialize_outer_board(self):
        self.outer_board = [[Frame(self.root) for _ in range(TTTBoard.BOARD_SIZE)] for _ in range(TTTBoard.BOARD_SIZE)]

    def _style_inner_boards(self):
        for i, row in enumerate(self.inner_boards):
            for j, inner_board in enumerate(row):
                for k, irow in enumerate(inner_board):
                    for m, button in enumerate(irow):
                        if (i == 1) ^ (j == 1):
                            button.config(highlightbackground = self.BOARD_BACKGROUND_2)
                        else:
                            button.config(highlightbackground = self.BOARD_BACKGROUND_1)

    def _initialize_inner_boards(self):
        self.inner_boards = [[self._generate_inner_board(r, c) for r in range(TTTBoard.BOARD_SIZE)] for c in range(TTTBoard.BOARD_SIZE)]
    
    def _generate_inner_board(self, row, col):
        return [[Button(self.outer_board[row][col], text = str(TTTMove.BLANK)) for _ in range(TTTBoard.BOARD_SIZE)] for _ in range(TTTBoard.BOARD_SIZE)]

    def _initialize_informational_labels(self):
        self.turn_indicator_label = Label(self.root, text = self.TURN_INDICATOR_LABEL)
        self.turn_icon = Label(self.root, text = str(TTTMove.X))

    def _place_board(self, board):
        for i, row in enumerate(board):
            for j, widget in enumerate(row):
                widget.grid(row = i, column = j)

    def _place_inner_boards(self):
        for row in self.inner_boards:
            for board in row:
                self._place_board(board)

    def _place_informational_labels(self):
        self.turn_indicator_label.grid(row = 0, column = TTTBoard.BOARD_SIZE + 1)
        self.turn_icon.grid(row = 1, column = TTTBoard.BOARD_SIZE + 1)

    def set_button_commands(self, callback_generator):
        """
        Used by controller to set the callbacks for the inner_board buttons.
        """
        for i, row in enumerate(self.inner_boards):
            for j, inner_board in enumerate(row):
                for k, irow in enumerate(inner_board):
                    for m, button in enumerate(irow):
                        self._set_button_command(callback_generator, button, i, j, k, m)

    def _set_button_command(self, callback_generator, button, row, col):
        button["command"] = callback_generator(button, i, j)
