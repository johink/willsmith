

class Action:
    """
    Base class for game actions.

    Subclasses are convenient containers to remove the reliance on nested 
    tuples and the copious amounts of packing and unpacking required by 
    these.

    Also has a method needed by HumanAgent to be able to prompt a user for 
    a game action.
    """

    def __init__(self):
        pass

    @staticmethod
    def prompt_for_action(legal_actions):
        """
        Asks game specific prompt(s) to gather information to create an 
        action for the game.
        """
        raise NotImplementedError()

    def __eq__(self, other):
        """
        Required to ensure proper behavior comparing actions, such as 
        testing if an action is an element of a list.

        isinstance(self, other.__class__) should be used to ensure equality 
        tests of different classes return False instead of raising an 
        AttributeError
        """
        raise NotImplementedError()

    def __hash__(self):
        """
        A custom equality implementation requires a custom hash 
        implementation.

        A simple default is to create a tuple of the instance attributes and 
        call hash() on it.
        """
        raise NotImplementedError()
