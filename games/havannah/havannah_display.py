from math import sqrt
from tkinter import Tk, Canvas

from games.havannah.color import Color

from willsmith.display_controller import DisplayController

import games.havannah.hex_math as hm


class HavannahDisplay(DisplayController):
    """
    The display controller for Havannah games.

    Creates a Tkinter GUI that displays the board.
    """

    HEX_BLANK = "#FFFFFF"
    HEX_BLUE = "#0000FF"
    HEX_RED = "#FF0000"

    # not sure exactly how the border works.  Does it take from the inside
    # or the outside of the hex?  The total hex size needs to be divisible by 
    # 4 to keep the coordinate math simple
    HEX_BORDER = 2
    HEX_BORDER_COLOR = "#000000"
    HEX_WIDTH = 32

    WINDOW_TITLE = "Havannah"

    CANVAS_HEIGHT = HEX_WIDTH * 20
    CANVAS_WIDTH = HEX_WIDTH * 16
    # half hex width is needed because havannah (0,0,0) is converted to 
    # the leftmost point of the hex for drawing
    CANVAS_CENTER = (CANVAS_WIDTH // 2 - HEX_WIDTH // 2, CANVAS_HEIGHT // 2)

    def __init__(self):
        """
        Declare the attributes needed for the GUI.
        """
        self.root = None
        self.canvas = None

    def start(self):
        """
        Initialize the root window and the display widgets.
        """
        self.root = self._initialize_root()
        self._initialize_widgets()
        self._place_widgets()
        self._update_window()

    def reset_display(self, game):
        """
        Update the board with blank hexes.
        """
        for coord in game.board.grid.keys():
            canvas_coord = self._havannah_coord_to_canvas_coord(coord)
            self._draw_hex(canvas_coord, self.HEX_BLANK)

    def update_display(self, game, action):
        """
        Redraw the hex from the given action.
        """
        canvas_coord = self._havannah_coord_to_canvas_coord(action.coord)
        canvas_color = self._havannah_color_to_canvas_color(action.color)
        self._draw_hex(canvas_coord, canvas_color)
        self._update_window()

    def _initialize_root(self):
        """
        Create the window root and update it's configuration.
        """
        root = Tk()
        root.title(self.WINDOW_TITLE)
        return root

    def _initialize_widgets(self):
        self.canvas = Canvas(self.root, width = self.CANVAS_WIDTH, 
                                height = self.CANVAS_HEIGHT)

    def _place_widgets(self):
        self.canvas.pack()

    def _update_window(self):
        self.root.update_idletasks()
        self.root.update()

    def _havannah_coord_to_canvas_coord(self, coord):
        """
        Convert a board hex coordinate (x,y,z) to the canvas coordinate (x,y) 
        that is the starting point of the hex.

        The resulting coordinate is the left-most point in the hex.  Hexes 
        are the flat-topped variety.
        """
        col, slant = hm.cubic_to_axial(*coord)
        canvas_x, canvas_y = self.CANVAS_CENTER

        canvas_x += col * self.HEX_WIDTH // 4 * 3
        canvas_y += (col * self.HEX_WIDTH // 2) + (slant * self.HEX_WIDTH)

        return (canvas_x, canvas_y)

    def _other(self, coord):
        col, slant = hm.cubic_to_axial(*coord)
        canvas_x, canvas_y = self.CANVAS_CENTER

        canvas_x += self.HEX_WIDTH // 2 * 3 * col
        canvas_y += self.HEX_WIDTH * sqrt(3) * (slant + col / 2)

        return (canvas_x, canvas_y)

    def _havannah_color_to_canvas_color(self, color):
        """
        Convert Color enums to the matching fill color.
        """
        canvas_color = None
        if color == Color.BLANK:
            canvas_color = self.HEX_BLANK
        elif color == Color.BLUE:
            canvas_color = self.HEX_BLUE
        elif color == Color.RED:
            canvas_color = self.HEX_RED
        else:
            raise RuntimeError("Unexpected hex color.")
        return canvas_color

    def _draw_hex(self, coord, color):
        """
        Draw a colored hex at the given coord.
        """
        deltas = [(self.HEX_WIDTH // 4, self.HEX_WIDTH // 2), 
                    (self.HEX_WIDTH // 2, 0), 
                    (self.HEX_WIDTH // 4, -self.HEX_WIDTH // 2),
                    (-self.HEX_WIDTH // 4, -self.HEX_WIDTH // 2),
                    (-self.HEX_WIDTH // 2, 0)]
        points = [coord]
        x, y = coord
        for dx, dy in deltas:
            x += dx
            y += dy
            points.append((x, y))
            
        self.canvas.create_polygon(points, outline=self.HEX_BORDER_COLOR, 
                                    fill=color, width=self.HEX_BORDER)
