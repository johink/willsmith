from math import log, sqrt
from time import time


class MCTSAgent:
    """
    Planning agent that makes decisions based on Monte Carlo Tree Search.
    Computes a number of playouts using the following steps, then chooses the
    optimal action:

        Selection       -   Start at root, use UCB to choose actions until action does not produce child
        Expansion       -   Create new node
        Simulation      -   Play out game until reaching a terminal state
        Backpropagation -   Update win/trial counters for new node and all parents
    """

    EXP_PARAM = sqrt(2)
    NEW_NODE_TRIALS = 0.1       # what should this be?


    def __init__(self, state, agent_id):
        self.state = state
        self.root = self.Node(None, False)
        self.agent_id = agent_id

    def search(self, max_runs = 1000, max_time = 2):
        """
        Searches for the optimal action to take by running max_runs
        number of playouts.
        """
        runs = 0
        start_time = time()

        while runs < max_runs:  # and time() - start_time < 2
            current_state, current_node = self.selection()
            new_node = self.expansion(current_state, current_node)
            win = self.simulation(current_state)
            self.backpropagation(win, new_node)

        best_action = self.root.max_value_estimate()
        return best_action

    def take_action(self, action):
        self.state = self.state.take_action(action)
        self.root = self.root.get_child(action)

    def selection(self):
        """
        Progresses through the tree of Nodes until a leaf is found.
        """
        current_state = self.state
        current_node = self.root

        while current_node.has_children():
            action = current_node.UCB(state, self.root.trials)  # root.trials == total number of trials
            current_state = current_state.take_action(action)
            current_node = current_node.get_child(action)

        return current_state, current_node

    def expansion(self, state, node):
        """
        Handles creation of a new leaf in the Node tree.
        """
        # create a new node for some action ?? where does that action come from
        node.add_child(action, self.Node(node, not node.adversarial))
        new_child = node.get_child(action)
        return new_child

    def simulation(self, state):
        """
        Plays out the game to its conclusion and returns the result.
        """
        while not state.final():
            state = state.take_random_action()

        return state.win(self.agent_id)   # need some reference to agent to determine win or lose

    def backpropagation(self, win, node):
        """
        Propogates simluation result up the tree of nodes.
        """
        while node is not None:
            node.update_node(win)
            node = node.parent


    class Node:
        """
        Used internally by the agent to keep track of the results of trials
        after taking certain actions.
        """
        def __init__(self, parent, adversarial = False):
            self.parent = parent
            self.children = dict() # action : node
            self.trials = 0
            self.wins = 0

        def update_node(self, win):
            """
            Updates node using simulation result during backpropagation step.
            """
            if win ^ adversarial: # either win+maximizing or lose+minimizing
                self.wins += 1
            self.trials += 1

        def value_estimate(self):
            return self.wins / self.trials

        def max_value_estimate(self):
            """
            Returns maximum action at the node given the current children.
            """
            value_func = lambda x: self.children.get_child(x).value_estimate()
            return max(self.children, key=value_func)

        def UCB(self, state, total_trials):
            """
            Chooses an action based on an exploitation vs exploration function
            expressed as:

            num wins at node / num trials node +
                exploration parameter *
                    sqrt(ln total trials / num trials at node)
            """
            valid_actions = state.get_valid_actions()
            results = {}

            for action in valid_actions:
                value_estimate = 0
                exploration_estimate = EXP_PARAM * sqrt(log(total_trials) / NEW_NODE_TRIALS)
                if action in self.children:
                    value_estimate = self.get_child(action).value_estimate()
                    exploration_estimate = EXP_PARAM * sqrt(log(total_trials) / self.trials)

                results[action] = value_estimate + exploration_estimate

            return max(results.keys(), key=results.get)

        def get_child(self, action):
            return self.children[action]

        def has_children(self):
            return bool(self.children)
