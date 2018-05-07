from abc import ABC, abstractmethod
from random import random


class MDPAgent(ABC):
    """
    """

    def __init__(self, action_space, learning_rate, discount, 
                    exploration_rate):
        self.action_space = action_space
        self.learning_rate = learning_rate
        self.discount = discount
        self.exploration_rate = exploration_rate

    @abstractmethod
    def _get_next_action(self, state):
        pass

    @abstractmethod
    def update(self, prev_state, curr_state, reward, action, terminal):
        """
        """
        pass

    @abstractmethod
    def reset(self):
        """
        """
        pass

    def get_next_action(self, state):
        """
        """
        action = state.action_space_sample()
        if random() > self.exploration_rate:
            action = self._get_next_action(state)
        return action
