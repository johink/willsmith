from abc import ABC, abstractmethod


class Agent(ABC):
    """
    Abstract base class for game playing agents.
    
    Subclasses are agents that are capable of searching for and returning 
    actions within an allotted time and updating their internal state based 
    on a given action taken in the game.
    """

    def __init__(self, agent_id):
        self.agent_id = agent_id

    @abstractmethod
    def search(self, state, allotted_time):
        """
        Search the action space for the next action to take.  

        Search strategy depends on the subclass implementation.
        """
        pass

    @abstractmethod
    def take_action(self, action):
        """
        Update the agent's internal state by the latest action taken in the 
        game.
        """
        pass
