from abc import ABC, abstractmethod


class DisplayController(ABC):
    """
    Abstract base class for the display component of simulators.

    Subclasses must include implementations to manage their display component.
    """

    def __init__(self):
        pass

    @abstractmethod
    def reset_display(self):
        """
        Return the display to an initial state.
        """
        pass

    @abstractmethod
    def update_display(self, game):
        """
        Update the display based on the given game state.
        """
        pass
