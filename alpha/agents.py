from util import Node, Edge

class AlphaMCTSAgent:
    def __init__(self, control_net = None):
        self.root = Node(None)
        self.playout_total = 0
        self.control_net = control_net

    def update_control_net(self, control_net):
        self.control_net = control_net

    def search(self, game, turn_num, allotted_playouts = 800):
        if self.control_net is None:
            raise ValueError("Control net must be set before starting searches")
        playouts = 0

        start_time = time()
        while playouts < allotted_playouts:
            current_game = game.copy()
            current_game, node = self._selection(current_game)

            actions = current_game.get_valid_moves()
            ps, v = self.control_net(current_game.state.unsqueeze(0))
            ps.squeeze_()
            v = v.squeeze().item()

            indices = [self.ttt_position_to_index(action) for action in actions]

            actions = [(round(current_game.state[2,0,0,0,0].item()),) + tuple(action) for action in actions]

            node.expansion(actions, ps.detach().numpy()[indices])

            if id(self.root) != id(node):
                node.backpropagate(v)

            playouts += 1

        temp = 1 if turn_num < 30 else .1
        max_action = self.root.choose_action(temp)

        # debug info
        self.playout_total = playouts
        self.action_node = max_action

        actions = game.get_valid_moves()
        indices = [self.ttt_position_to_index(action) for action in actions]
        actions = [(round(game.state[2,0,0,0,0].item()),) + tuple(action) for action in actions]

        mcts_probs = {indices[i]: self.root.edges[actions[i]].N for i in range(len(indices))}
        total_trials = sum(mcts_probs.values())
        mcts_probs = [mcts_probs.get(x, 0) / total_trials for x in range(81)]

        return max_action, mcts_probs

    def take_action(self, action):
        try:
            self.root = self.root.edges[action].destination
        except KeyError:
            print("Action not found, throwing away tree")
            self.reset()

    def reset(self):
        self.root = Node(None)

    def _selection(self, state):
        """
        Progress through the tree of Nodes, starting at the root, until a
        leaf is found or there are unexplored actions at the level we are
        exploring.

        Uses the UCT algorithm to determine which nodes to progress to.
        """
        node = self.root
        while not node.leaf:
            move = node.selection_step()
            node = node.edges[move].destination
            state.make_move(move)
        return state, node

    @staticmethod
    def index_to_ttt_position(idx):
        return idx // 27 % 3, idx // 9 % 3, idx // 3 % 3, idx % 3

    @staticmethod
    def ttt_position_to_index(position):
        return position[0] * 27 + position[1] * 9 + position[2] * 3 + position[3]
