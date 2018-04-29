from abc import ABC, abstractmethod


class MDPAgent(ABC):
    """
    """

    def __init__(self):
        pass

    @abstractmethod
    def next_action(self, state):
        pass

    @abstractmethod
    def after_action_update(self, action, state, reward):
        pass
