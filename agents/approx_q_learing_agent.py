from random import random


class ApproxQLearningAgent:
    """
    A template for an agent that uses appoximate Q-learning to learn a policy.

    The expectation is that this base class subclassed with a given set of 
    feature functions that provide it with some domain specific knowledge 
    about and MDP and that agent will attempt to learn an optimal policy.

    This class takes the given set of feature functions and slowly updates a 
    weighted value for each of them while progressing through the MDP.  These 
    weights are updated based on the difference between the expected reward 
    for a transition from one state to antoher and the actual reward received.
    """

    def __init__(self, action_space, feature_functions, learning_rate, discount):
        self.action_space = action_space

        self.discount = discount
        self.learning_rate = learning_rate

        self.features = feature_functions
        self.weights = self._create_random_weight_list(len(self.features))

    def get_max_action(self, state):
        """
        Returns the best(determined by sum of weighted feature function)
        available action given the current state.
        """
        values = {action : self._get_q_value(state, action) 
                    for action in self.action_space}
        return max(values, key=values.get)

    def update_weights(self, prev_state, curr_state, reward, last_action, done):
        """
        Updates the feature weights based on expected future rewards and
        the difference between the previous reward and what it was expected
        to be.
        """
        difference = self._calculate_difference(prev_state, curr_state, 
                                                    reward, last_action, done)

        current_weights = self._get_weights(last_action)
        new_weights = []

        for feature, weight in zip(self.features, current_weights):
            new_weight = (weight 
                            + (self.learning_rate 
                                    * difference 
                                    * feature(prev_state, last_action)))
            new_weights.append(new_weight)

        self._update_weights(new_weights, last_action)

    def _create_random_weight_list(self, n):
        return [random() for _ in range(n)]

    def _get_q_value(self, state, action):
        """
        Calculate the q-value for a given state, action pair.
        """
        weights = self._get_weights(action)
        next_state = state.copy()
        next_state.step(action)
        return sum([feature(next_state, action) * weight 
                        for (feature, weight) in zip(self.features, weights)])

    def _get_max_q_value(self, state):
        values = [self._get_q_value(state, action) 
                    for action in self.action_space]
        return max(values)

    def _get_weights(self, action):
        return self.weights.copy()

    def _update_weights(self, new_weights, action):
        self.weights = new_weights

    def _calculate_difference(self, prev_state, curr_state, reward, last_action, done):
        """
        Calculates the difference received reward and what was predicted.
        """
        future_reward = 0
        if not done:
            future_reward = self._get_max_q_value(curr_state)

        expected_reward = self._get_q_value(prev_state, last_action)
        return (reward + self.discount * future_reward) - expected_reward
