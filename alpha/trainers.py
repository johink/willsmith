import torch
import random

from util import zero_gen, one_neg_one_gen, ReplayBuffer
from architectures import NestedTTTNet
from agents import AlphaMCTSAgent

class SelfPlayTrainer:
    def __init__(self, agent, game, buffer_file = None, weights_file = None, n_batches = 0):
        self.agent = agent
        self.game = game
        self.replay_buffer = ReplayBuffer()

        if buffer_file is not None:
            self.replay_buffer.buffer = pickle.load(open(buffer_file, "rb"))

        self.current_network = NestedTTTNet()
        self.control_network = NestedTTTNet()

        if weights_file is not None:
            self.control_network.load_state_dict(torch.load(weights_file))

        self.current_network.load_state_dict(self.control_network.state_dict())
        self.control_network.eval()
        self.current_network.train()

        self.agent.update_control_net(self.control_network)

        self.n_batches = n_batches

        self.optim = torch.optim.Adam(self.current_network.parameters(), lr = .01, weight_decay = 10e-4)

    def generate_self_play_data(self, n_games = 100):
        for _ in range(n_games):
            turn_num = 0
            self.game.reset()
            self.agent.reset()
            result = 0
            player_num = 0

            states = []
            move_vectors = []

            while len(self.game.get_valid_moves()) > 0:
                move, move_probs = self.agent.search(self.game.copy(), turn_num, allotted_playouts = 400)

                states.append(self.game.state.tolist())
                move_vectors.append(move_probs)

                result = self.game.make_move(move)
                if not result:
                    self.game.switch_player()
                    self.agent.take_action(move)
                    turn_num += 1
                    player_num = (player_num + 1) % 2

            if not result:
                self.replay_buffer.extend(list(zip(states, move_vectors, zero_gen())))
            else:
                self.replay_buffer.extend(list(zip(states[::-1], move_vectors[::-1], one_neg_one_gen()))[::-1])

    def compare_control_to_train(self):
        self.current_network.eval()
        old_agent = AlphaMCTSAgent(control_net = self.control_network)
        new_agent = AlphaMCTSAgent(control_net = self.current_network)

        agents = [old_agent, new_agent]

        wins = 0
        ties = 0

        game = self.game.copy()

        for game_num in range(100):
            game.reset()
            agents[0].reset()
            agents[1].reset()
            result = 0
            player_num = game_num // 50 #Both take first turn 50 times
            turn_num = 100 #Turn down the temperature

            while len(game.get_valid_moves()) > 0:
                move, _ = agents[player_num].search(game.copy(), turn_num, allotted_playouts = 800)
                _, _ = agents[1 - player_num].search(game.copy(), turn_num, allotted_playouts = 800)

                result = game.make_move(move)
                if not result:
                    game.switch_player()
                    agents[0].take_action(move)
                    agents[1].take_action(move)
                    player_num = (player_num + 1) % 2

            if not result:
                ties += 1
            elif result and player_num == 1:
                wins += 1

            print("After {} games, {} wins and {} ties".format(game_num+1, wins, ties))

        if wins + .5 * ties >= 55:
            print("Challenger network won {} games and tied {} games; it becomes new control network".format(wins, ties))
            torch.save(self.current_network.state_dict(), "control_weights_{}.pth".format(self.n_batches))
            self.control_network.load_state_dict(self.current_network.state_dict())
        else:
            print("Challenger network not sufficiently better; {} wins and {} ties".format(wins, ties))

        self.control_network.eval()
        self.current_network.train()

    def train_on_batch(self, batch_size = 32):
        if len(self.replay_buffer) < batch_size:
            return

        self.current_network.train()

        sample = self.replay_buffer.sample(batch_size)
        states, probs, rewards = zip(*sample)
        states = torch.FloatTensor(states).requires_grad_(True)
        probs = torch.FloatTensor(probs).requires_grad_(True)
        rewards = torch.FloatTensor(rewards).unsqueeze(1).requires_grad_(True)
        self.optim.zero_grad()

        ps, vs = self.current_network(states)

        loss = torch.nn.functional.mse_loss(vs, rewards) - (ps.log() * probs).sum()
        loss.backward()

        self.optim.step()

        self.n_batches += 1

        return loss.item()

    def run(self, total_runs = 10, self_play_games = 100, training_batches = 200, batch_size = 32):
        losses = []
        for run_num in range(1, total_runs+1):
            print("Run {} of {}".format(run_num, total_runs))
            for selfplay_num in range(1, self_play_games + 1):
                self.generate_self_play_data(1)
                print("\tFinished self-play game {} of {} (Buffer size {})".format(selfplay_num, self_play_games, len(self.replay_buffer)))
            print("Finished {} self-play games".format(self_play_games))
            for _ in range(training_batches):
                losses.append(self.train_on_batch(batch_size))
                if len(losses) == 5:
                    print("\tLoss for last 5 batches: {}".format(sum(losses)))
                    losses = []

        self.compare_control_to_train()
