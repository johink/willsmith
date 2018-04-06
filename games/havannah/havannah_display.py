from tkinter import Canvas

from games.havannah.color import Color
from games.havannah.hex_math import cubic_to_axial

from willsmith.gui_display_controller import GUIDisplayController


class HavannahDisplay(GUIDisplayController):
    """
    The display controller for Havannah games.

    Creates a Tkinter GUI with a Canvas that is used to draw the hexes.  

    Board coordinates are converted to a canvas pixel location, where this 
    new canvas location is the left-most point of the given (flat-topped) 
    hex.  This is the reason for the half-hex shift of the canvas center.

    Hex width should be divisible by 4 so that all of the math is on 
    integers.
    """

    WINDOW_TITLE = "Havannah"

    HEX_BLANK = "#FFFFFF"
    HEX_BLUE = "#0000FF"
    HEX_RED = "#FF0000"
    HEX_BORDER_COLOR = "#000000"

    HEX_WIDTH = 32
    HEX_BORDER = 2

    CANVAS_HEIGHT = HEX_WIDTH * 20
    CANVAS_WIDTH = HEX_WIDTH * 16
    CANVAS_CENTER = (CANVAS_WIDTH // 2 - HEX_WIDTH // 2, CANVAS_HEIGHT // 2)

    def __init__(self):
        super().__init__()
        self.canvas = None

    def _reset_display(self, game):
        """
        Update the board with blank hexes.
        """
        for coord in game.board.grid.keys():
            canvas_coord = self._havannah_coord_to_canvas_coord(coord)
            self._draw_hex(canvas_coord, self.HEX_BLANK)

    def _update_display(self, game, action):
        """
        Redraw the hex using the given action.
        """
        canvas_coord = self._havannah_coord_to_canvas_coord(action.coord)
        canvas_color = self._havannah_color_to_canvas_color(action.color)
        self._draw_hex(canvas_coord, canvas_color)

    def _initialize_widgets(self):
        self.canvas = Canvas(self.root, width = self.CANVAS_WIDTH, 
                                height = self.CANVAS_HEIGHT)

    def _place_widgets(self):
        self.canvas.pack()

    def _havannah_coord_to_canvas_coord(self, coord):
        """
        Convert a board hex coordinate (x,y,z) to the canvas coordinate (x,y) 
        that is the starting point of the hex.

        The resulting coordinate is the left-most point in the hex.  Hexes 
        are the flat-topped.
        """
        col, slant = cubic_to_axial(*coord)
        canvas_x, canvas_y = self.CANVAS_CENTER

        canvas_x += col * self.HEX_WIDTH // 4 * 3
        canvas_y += (col * self.HEX_WIDTH // 2) + (slant * self.HEX_WIDTH)

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

        The deltas correspond to the coordinate shift moving from the current 
        point along the edge to the next point of the hex for each of the 6 
        points.
        """
        deltas = [(0,0), (self.HEX_WIDTH // 4, self.HEX_WIDTH // 2),
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
