from abc import abstractmethod
from tkinter import Tk

from willsmith.display_controller import DisplayController


class GUIDisplayController(DisplayController):
    """
    Abstract base class for Tkinter GUI-based display controllers.

    Sub-classes are expected to provide functionality for widget management.
    """

    def __init__(self):
        self.root = None

    @abstractmethod
    def _initialize_widgets(self):
        """
        Instantiate and assign all the widget attributes for the object.
        """
        pass

    @abstractmethod
    def _place_widgets(self):
        """
        Use a tkinter geometry manager to put the widgets in the main window.
        """
        pass

    @abstractmethod
    def _update_display(self, game, action):
        pass

    @abstractmethod
    def _reset_display(self, game):
        pass

    def start(self):
        self.root = self._initialize_root()
        self._initialize_widgets()
        self._place_widgets()

    def _initialize_root(self):
        """
        Create the window root and update its configuration.
        """
        root = Tk()
        root.title(self.WINDOW_TITLE)
        return root

    def update_display(self, game, action):
        """
        Ensure _update_window method is called when the display is updated.
        """
        self._update_display(game, action)
        self._update_window()

    def reset_display(self, game):
        """
        Ensure _update_window method is called when the display is updated.
        """
        self._reset_display(game)
        self._update_window()

    def _update_window(self):
        """
        Update the GUI window with any changes that have taken place.
       
        This is used to manually update the window only after the display has 
        actually had a background update, instead of letting it control the 
        thread of execution.
        """
        self.root.update_idletasks()
        self.root.update()
