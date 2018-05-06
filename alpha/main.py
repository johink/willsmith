from argparse import ArgumentParser
from trainers import SelfPlayTrainer
from games import NestedTTT
from agents import AlphaMCTSAgent

def create_parser():
    parser = ArgumentParser(description = "Train AlphaTTTNet")

    parser.add_argument("-b", "--buffer_file", type = str, default = None,
                        help = "File containing self-play game data")
    parser.add_argument("-c", "--complete_batches", type = int, default = 0,
                        help = "Number of previously completed batches")
    parser.add_argument("-n", "--num_games", type = int, default = 1,
                        help = "Number of successive game simulations to run.")
    parser.add_argument("-r", "--runs", type = int, default = 10,
                        help = "Number of self-play/train runs to conduct before comparison.")
    parser.add_argument("-s", "--self_play_games", type = int, default = 100,
                        help = "Number of self-play games per training run.")
    parser.add_argument("-t", "--training_batches", type = int, default = 200,
                        help = "Number of self-play games per training run.")
    parser.add_argument("-w", "--weights_file", type = str, default = None,
                        help = "File containing weights for control network")

    return parser

def main():
    parser = create_parser()
    args = parser.parse_args()

    trainer = SelfPlayTrainer(AlphaMCTSAgent(), NestedTTT(),
                                args.buffer_file, args.weights_file, args.complete_batches)

    trainer.run(args.runs, args.self_play_games, args.training_batches)

    trainer.compare_control_to_train()

if __name__ == "__main__":
    main()
