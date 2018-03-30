from math import log, sqrt
from random import choice
from time import time

from willsmith.agent import Agent


class MCTSAgent(Agent):
    """
    Planning agent that makes decisions based on Monte Carlo Tree Search.

    Computes as many runs as possible in the time alloted, where a run 
    consists of the following stages:

        Selection       -   Start at root, use UCB to choose actions until 
                                action does not produce child  
        Expansion       -   Create new node  
        Simulation      -   Play out game until reaching a terminal state  
        Backpropagation -   Update win/trial counters for new node and all parents  

    Then, it chooses the action with the most trials and returns that.

    The agents internal game state is stored as a tree of nodes, where the 
    edges are actions and the nodes are the wins/total trials from the 
    perspective of the agent they represent.
    """

    def __init__(self, agent_id):
        super().__init__(agent_id)
        self.root = self.Node(None, None)

    def search(self, state, allotted_time):
        """
        Run as many playouts as possible in the allotted time.

        The individual steps are described in the class docstrings

        Searches the state space for the best available action, using the above 
        steps.
        """
        runs = 0
        start_time = time()

        while time() - start_time < allotted_time:
            current_state = state.copy()
            current_state, current_node, game_over = self._selection(current_state)
            if not game_over:
                new_state, new_node = self._expansion(current_state, current_node)
                winning_id = self._simulation(new_state)
                self._backpropagation(winning_id, new_node)
            else:
                winning_id = self._simulation(current_state)
                self._backpropagation(winning_id, current_node)
            runs += 1

        next_action = self.root.max_trials()
        return next_action

    def take_action(self, action):
        """
        Move the tree root to the child node of the current root corresponding 
        to the action.

        If a node for that action has never been expanded, restart the tree 
        from scratch.  This happens in cases where an adversary takes an 
        action that we have not yet expanded and explored.
        """
        try:
            self.root = self.root.get_child(action)
        except KeyError:
            self.root = self.Node(None, None)

    def _selection(self, state):
        """
        Progress through the tree of Nodes, starting at the root, until a 
        leaf is found or there are unexplored actions at the level we are 
        exploring.

        Uses the UCB algorithm to determine which nodes to progress to.
        """
        node = self.root

        unexplored_actions = set(state.get_legal_actions()) - set(node.children.keys())
        terminal = state.is_terminal()

        while not unexplored_actions and not terminal:
            action = node.UCB(state, self.root.trials)  # root.trials == total number of trials

            state.take_action_if_legal(action)
            node = node.get_child(action)

            unexplored_actions = set(state.get_legal_actions()) - set(node.children.keys())
            terminal = state.is_terminal()

        return state, node, terminal

    def _expansion(self, state, node):
        """
        Handle the creation of a new leaf in the Node tree.

        Makes a random choice of the unexplored actions, adds that Node to 
        the tree, and progress the current game state by that action.
        """
        action = choice([action for action in state.get_legal_actions() if action not in node.children])
        new_child = self.Node(node, state.current_agent_id)
        node.add_child(action, new_child)

        state.take_action_if_legal(action)

        return state, new_child

    def _simulation(self, state):
        """
        Play out the game to its conclusion and returns the winner.
        """
        while not state.is_terminal():
            action = self._random_simulation(state)
            state.take_action_if_legal(action)
        return state.get_winning_id()

    def _random_simulation(self, state):
        """
        Make random choices for actions regardless of the state.

        This strategy is called a "light playout".  It has little 
        computational overhead, but also does not take advantage of any 
        domain knowledge about the game.
        """
        action = state.generate_random_action()
        return action

    def _backpropagation(self, winning_id, node):
        """
        Update nodes from node to the tree root with the simulation result.
        """
        while node is not None:
            node.update_node(winning_id)
            node = node.parent

    def _get_extreme_actions(self):
        """
        Return the nodes with minimum and maximum value estimates in the tree.

        Used for debugging.
        """
        maxi = None
        mini = None
        for action in self.root.children:
            node = self.root.children[action]
            value = node._value_estimate()
            if maxi is None or value > maxi._value_estimate():
                maxi = node
            if mini is None or value < mini._value_estimate():
                mini = node
        return maxi, mini

    def __str__(self):
        return "AgentID:Max:[{}], Min:[{}]".format(*self._get_extreme_actions())


    class Node:
        """
        Used internally by the agent to store the results of simulations.

        Each node keeps track of:
        - its place in the tree, 
        - the agent id of the agent who is choosing the next action, 
        - and the win% of that agent from this point in the game tree.
        """

        EXPLORATION_PARAM = sqrt(2)

        def __init__(self, parent, agent_id):
            self.parent = parent
            self.children = dict() # action : node
            self.trials = 0
            self.wins = 0
            self.agent_id = agent_id

        def update_node(self, winning_id):
            """
            Update node using simulation result during backpropagation step.
            """
            if self.agent_id is not None and winning_id == self.agent_id:
                self.wins += 1
            self.trials += 1

        def _value_estimate(self):
            return self.wins / self.trials

        def max_trials(self):
            """
            Return the child node with the maximum number of trials.
            """
            value_func = lambda x: self.get_child(x).trials
            return max(self.children, key=value_func)

        def UCB(self, state, total_trials):
            """
            Choose an action based on an exploitation vs exploration function
            that expresses node value as:

            (exploitation)
            num wins at node / num trials node +

            (exploration)
            exploration parameter * sqrt(ln(total trials) / num trials at node)
            """
            valid_actions = state.get_legal_actions()
            results = {}

            for action in valid_actions:
                value_estimate = self.get_child(action)._value_estimate()
                exploration_estimate = self.EXPLORATION_PARAM * sqrt(log(total_trials) / self.trials)

                results[action] = value_estimate + exploration_estimate

            return max(results.keys(), key=results.get)

        def add_child(self, action, node):
            self.children[action] = node

        def get_child(self, action):
            return self.children[action]

        def has_children(self):
            return bool(self.children)

        def __str__(self):
                return "ID:{},{}/{}".format(self.agent_id, self.wins, self.trials)
