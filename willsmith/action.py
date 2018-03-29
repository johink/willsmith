from abc import ABC, abstractmethod


class Action(ABC):
    """
    Abstract base class for game actions.

    Subclasses are convenient containers to remove the reliance on nested 
    tuples and the copious amounts of packing and unpacking required by 
    them.

    Also has the method prompt_for_action needed by HumanAgent to be able to 
    prompt a user for a game action.
    """

    def __init__(self):
        pass

    @staticmethod
    @abstractmethod
    def prompt_for_action(legal_actions):
        """
        Prompt the user and parse the input of their choice to create an 
        instance of the Action subclass.
        """
        pass

    @abstractmethod
    def __eq__(self, other):
        """
        Compares two objects.

        Required to ensure proper behavior comparing actions, such as 
        testing if an action is an element of a list.

        isinstance(self, other.__class__) should be used to ensure equality 
        tests of different classes return False instead of raising an 
        AttributeError
        """
        pass

    @abstractmethod
    def __hash__(self):
        """
        Hashes the object.

        A custom equality implementation requires a custom hash 
        implementation.

        A simple default is to create a tuple of the instance attributes and 
        call hash() on it.
        """
        pass
