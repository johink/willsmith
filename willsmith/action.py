from abc import ABC, abstractmethod


class Action(ABC):
    """
    Abstract base class for game actions.

    Subclasses are convenient containers to remove the reliance on nested 
    tuples and the copious amounts of packing and unpacking required by 
    them.

    The parse_action method is used to convert strings to the action subclass, 
    and the INPUT_PROMPT attribute is used to convey the format to a user.
    """

    INPUT_PROMPT = None

    def __init__(self):
        if self.INPUT_PROMPT is None:
            raise RuntimeError("Actions must set an input prompt.")

    @staticmethod
    @abstractmethod
    def parse_action(input_str):
        """
        Parse an input string, returning an instance of the Action subclass 
        if the string was valid.
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
