from abc import ABC, abstractmethod


class DisplayController(ABC):
    """
    Abstract base class for the display component of simulators.

    Subclasses must include implementations to manage their display component.
    """

    def __init__(self):
        pass

    @abstractmethod
    def start(self):
        """
        Initialize the display elements.
        """
        pass

    @abstractmethod
    def reset_display(self, game):
        """
        Return the display to an initial state.
        """
        pass

    @abstractmethod
    def update_display(self, game, action):
        """
        Update the display based on the given game state and the last action
        taken.
        """
        pass
