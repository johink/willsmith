from math import sqrt
from collections import deque
import random

EXPLORATION_PARAM = sqrt(2)

def zero_gen():
    while True:
        yield 0

def one_neg_one_gen():
    while True:
        yield 1
        yield -1

class ReplayBuffer:
    def __init__(self, capacity = 10000):
        self.buffer = deque(maxlen = capacity)

    def push(self, data):
        self.buffer.append(data)

    def extend(self, data):
        self.buffer.extend(data)

    def sample(self, batch_size):
        return random.sample(self.buffer, batch_size)

    def __len__(self):
        return len(self.buffer)

class Node:
    """
    Nodes represent a state in the game.  They can have edges which
    indicate legal actions to take from the state
    """
    def __init__(self, incoming_edge):
        self.parent_edge = incoming_edge
        self.leaf = True
        self.edges = dict()

    def choose_action(self, temperature = 1):
        if not self.edges:
            raise ValueError("Cannot choose action from an unexplored node")

        visits_exp = sum([edge.N ** (1 / temperature) for edge in self.edges.values()])
        thresh = random.random()
        cumsum = 0
        for action, edge in self.edges.items():
            cumsum = cumsum + edge.N ** (1 / temperature)
            if thresh < cumsum / visits_exp:
                return action

    def selection_step(self):
        if self.leaf:
            raise ValueError("Cannot perform selection step at a leaf")
        max_result = None
        max_action = None

        total_trials = sum([edge.N for edge in self.edges.values()])

        for action, edge in self.edges.items():
            current_estimate = edge.value_estimate(total_trials)
            if max_result is None or max_result < current_estimate:
                max_result = current_estimate
                max_action = action

        return max_action

    def expansion(self, actions, ps):
        if actions:
            for action, p in zip(actions, ps):
                self.edges[action] = Edge(self, p)
            self.leaf = False

    def backpropagate(self, value):
        if self.parent_edge is None:
            raise ValueError("Can't start backpropagating at the root")
        else:
            #Current state for player A is a result of the action (edge) chosen by player B
            #If the current state has a good value for player A, then it has a bad value for player B
            #Value of current state (node) is inverted to update value of action taken (incoming edge)
            self.parent_edge.backpropagate(-value)

class Edge:
    """
    Edges represent transitions between game states, initiated by an action
    Edges keep track of the number of visits, the estimated value of taking
    their associated action, and the prior probability of taking that action
    """
    def __init__(self, origin, p):
        self.origin = origin
        self.destination = Node(self)
        self.N = 0 # Visits
        self.Q = 0 # Value estimate
        self.P = p # NN-generated prior

    def backpropagate(self, value):
        self.N += 1
        self.Q = self.Q * ((self.N - 1) / self.N) + value / self.N

        #Alternating edges indicate alternating player actions, so the value of states will be inverted at each layer
        if self.origin.parent_edge is not None:
            self.origin.parent_edge.backpropagate(-value)

    def value_estimate(self, parent_trials):
        return self.Q + EXPLORATION_PARAM * self.P * parent_trials ** .5 / (1 + self.N)

    def __str__(self):
        return "N={}, Q={}, P={}".format(self.N, self.Q, self.P)

    def __repr__(self):
        return str(self)
