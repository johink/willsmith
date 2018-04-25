from tkinter import Canvas, BOTH

from games.gridworld.gridworld_direction import GridworldDirection

from willsmith.gui_display_controller import GUIDisplayController


class GridworldDisplay(GUIDisplayController):
    """
    """

    WINDOW_TITLE = "Gridworld"

    SQUARE_WIDTH = 64
    SQUARE_BORDER = 2

    BACKGROUND_COLOR = "#FFFFFF"
    SQUARE_EMPTY_COLOR = "#A9A9A9"
    SQUARE_BORDER_COLOR = "#000000"
    SQUARE_AGENT_COLOR = "#FFFF00"

    TERM_COLOR_POS = "#00FF00"
    TERM_COLOR_NEG = "#FF0000"

    def __init__(self):
        super().__init__()
        self.canvas = None
        self.height = None

    def _initialize_widgets(self):
        self.canvas = Canvas(self.root)
        self.root["background"] = self.BACKGROUND_COLOR
        self.canvas["background"] = self.BACKGROUND_COLOR

    def _place_widgets(self):
        self.canvas.pack(fill = BOTH, expand = 1)

    def _update_display(self, state, action):
        """
        Clear the previous square the agent occupied by redrawing it, then 
        draw the agent in its new position.
        """
        clear_pos = self._square_coord_to_canvas_coord(*state.last_player_pos)
        new_pos = self._square_coord_to_canvas_coord(*state.player_pos)
        self._draw_square(state.grid[state.last_player_pos], clear_pos, False)
        self._draw_square(state.grid[state.player_pos], new_pos, True)

    def _reset_display(self, state):
        """
        Resize the window/canvas, then draw the entire board as is.

        Expects the agent to have been put back in its starting position.
        """
        width, height = state.grid.size
        self.height = (height * self.SQUARE_WIDTH 
                        + self.SQUARE_BORDER * 4)
        self.root.geometry("{}x{}".format((width * self.SQUARE_WIDTH 
                                                + self.SQUARE_BORDER * 4), 
                                            self.height))

        for pos in state.grid.keys():
            agent_square = False
            if pos == state.player_pos:
                agent_square = True
            canvas_pos = self._square_coord_to_canvas_coord(*pos)
            self._draw_square(state.grid[pos], canvas_pos, agent_square)

    def _square_coord_to_canvas_coord(self, x, y):
        """
        Convert a square's position on the grid to a pixel position on the 
        canvas.

        The subtraction in the y coordinate is because Tkinter reverses the 
        y-axis from a standard orientation.
        """
        canvas_x = x * self.SQUARE_WIDTH + self.SQUARE_BORDER * 2
        canvas_y = (self.height - self.SQUARE_BORDER * 2 - 
                        (y + 1) * self.SQUARE_WIDTH)
        return canvas_x, canvas_y

    def _draw_square(self, square, pos, agent):
        """
        Draw a colored square at the given location.

        If the agent is there, draw a smaller box indicating this.
        """
        square_color = self._determine_square_color(square)
        self.canvas.create_rectangle(pos[0], pos[1], 
                                    pos[0] + self.SQUARE_WIDTH, 
                                    pos[1] + self.SQUARE_WIDTH,
                                    fill = square_color,
                                    outline = self.SQUARE_BORDER_COLOR,
                                    width = self.SQUARE_BORDER)

        if agent:
            a_x1 = pos[0] + self.SQUARE_WIDTH // 4 - self.SQUARE_BORDER
            a_y1 = pos[1] + self.SQUARE_WIDTH // 4 - self.SQUARE_BORDER
            a_x2 = pos[0] + self.SQUARE_WIDTH * 3 // 4
            a_y2 = pos[1] + self.SQUARE_WIDTH * 3 // 4
            self.canvas.create_rectangle(a_x1, a_y1, a_x2, a_y2,
                                        fill = self.SQUARE_AGENT_COLOR)

    def _determine_square_color(self, square):
        """
        Determine which color the square should be based on whether it is 
        terminal and its reward.
        """
        color = self.SQUARE_EMPTY_COLOR
        if square.terminal and square.reward < 0:
            color = self.TERM_COLOR_NEG
        elif square.terminal and square.reward > 0:
            color = self.TERM_COLOR_POS
        return color
