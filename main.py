from argparse import ArgumentParser

from agents.human_agent import HumanAgent
from agents.mcts_agent import MCTSAgent
from agents.random_agent import RandomAgent

from games.ttt.nested_ttt import NestedTTT
from games.ttt.ttt_action import TTTAction

from willsmith.simulator import Simulator


def create_parser():
    parser = ArgumentParser(description = "Run agents through simulations")

    parser.add_argument("game_choice", type = str, 
                        choices = ["NestedTTT", "ttt"],
                        help = "The game for the agents to play")
    parser.add_argument("-a", "--agent1", type = str, default = "mcts",
                        choices = ["mcts", "rand", "human"],
                        help = "Agent type for player 1")
    parser.add_argument("-b", "--agent2", type = str, default = "rand",
                        choices = ["mcts", "rand", "human"],
                        help = "Agent type for player 2")
    parser.add_argument("-t", "--time_allotted", type = float, default = 1.0,
                        help = "Time allotted for agent moves")
    return parser

def lookup_agent(agent_str):
    lookup = {"mcts" : MCTSAgent, "rand" : RandomAgent, "human" : HumanAgent}
    try:
        agent = lookup[agent_str]
    except KeyError:
        agent = None

    return agent

if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()

    if args.game_choice == "NestedTTT" or args.game_choice == "ttt":
        game = NestedTTT
        action_prompt = TTTAction.prompt_for_action
    else:
        raise RuntimeError("Unexpected game type.")

    agent1 = lookup_agent(args.agent1)
    agent2 = lookup_agent(args.agent2)

    if agent1 is None or agent2 is None:
        raise RuntimeError("Unexpected agent type.")

    time = args.time_allotted

    simulator = Simulator(game, [agent1, agent2], time)
    simulator.add_action_prompt_to_human_agent(action_prompt)
    simulator.run_game()
