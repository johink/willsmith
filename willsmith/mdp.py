from abc import ABC, abstractmethod
from copy import deepcopy


class MDP(ABC):
    """
    """

    def __init__(self):
        pass

    @abstractmethod
    def get_action_space(self):
        pass

    @abstractmethod
    def step(self, action):
        pass

    @abstractmethod
    def action_space_sample(self):
        pass

    @abstractmethod
    def reset(self):
        pass

    def copy(self);
        return deepcopy(self)
