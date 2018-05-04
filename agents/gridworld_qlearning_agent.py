from agents.approx_qlearning_agent import ApproxQLearningAgent


class GridworldQLearningAgent(ApproxQLearningAgent):
    """
    """
    
    def __init__(self, action_space, learning_rate, discount, exploration_rate):
        feature_functions = [self.x_pos_feature, self.y_pos_feature, 
                                self.score_feature]
        super().__init__(action_space, learning_rate, discount, 
                            exploration_rate, feature_functions)

    def x_pos_feature(self, state, action):
        return state.player_pos[0]

    def y_pos_feature(self, state, action):
        return state.player_pos[1]

    def score_feature(self, state, action):
        return state.total_reward
