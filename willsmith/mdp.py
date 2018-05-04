from abc import ABC, abstractmethod
from copy import copy, deepcopy
from random import choice

from willsmith.simple_displays import ConsoleDisplay, NoDisplay


class MDP(ABC):
    """
    """

    DISPLAY = None

    def __init__(self, use_display):
        self.timesteps = 0
        self.total_reward = 0
        self.reward_history = []

        self.display = NoDisplay()
        if use_display is not None:
            if not use_display or self.DISPLAY is None:
                self.display = ConsoleDisplay()
            else:
                self.display = self.DISPLAY()
        self.display.start(is_main = True)

    @abstractmethod
    def get_action_space(self):
        pass

    @abstractmethod
    def _step(self, action):
        pass

    @abstractmethod
    def _undo(self):
        pass

    @abstractmethod
    def _reset(self):
        pass

    @abstractmethod
    def is_terminal(self):
        pass

    def step(self, action):
        if not self.is_legal_action(action):
            raise RuntimeError("Received illegal action: {}".format(action))

        reward, terminal = self._step(action)

        self.timesteps += 1
        self.total_reward += reward
        self.reward_history.append(reward)

        if self.display is not None:
            self.display.update_display(self, action)
        
        return reward, terminal

    def undo(self, action):
        self.timesteps -= 1
        self.total_reward -= self.reward_history.pop()
        self._undo(action)

        if self.display is not None:
            self.display.update_display(self, action)

    def reset(self):
        self.timesteps = 0
        self.total_reward = 0
        self.reward_history = []
        self._reset()
        
        if self.display is not None:
            self.display.reset_display(self)

    def is_legal_action(self, action):
        return not self.is_terminal() and action in self.action_space

    def action_space_sample(self):
        return choice(self.action_space)

    def copy(self):
        return deepcopy(self)

    def __eq__(self, other):
        return (self.timesteps == other.timesteps
                    and self.total_reward == other.total_reward
                    and self.reward_history == other.reward_history)

    def deepcopy_mdp_attrs(self, new):
        """
        Used by subclasses to copy over the game attributes to a new deepcopy 
        of the subclass.

        Does not copy the display instance over, so that modifications to 
        a copy do not update/change the original.
        """
        new.timesteps = self.timesteps
        new.total_reward = self.total_reward
        new.reward_history = copy(self.reward_history)
        new.display = None
        return new
