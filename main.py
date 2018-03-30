"""
The main executable that instantiates the simulator with the proper game and 
agents, as specified by the command-line arguments.

Run python main.py -h for the explanation of command-line arguments.

See README.md for a full-project breakdown.
"""


from argparse import ArgumentParser

from agents.human_agent import HumanAgent
from agents.mcts_agent import MCTSAgent
from agents.random_agent import RandomAgent

from games.ttt.nested_ttt import NestedTTT
from games.ttt.ttt_display import TTTDisplay

from willsmith.simple_displays import ConsoleDisplay
from willsmith.simple_displays import NoDisplay
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
    parser.add_argument("-c", "--console-render", action = "store_true",
                        default = False,
                        help = "Render the game on the command-line")
    parser.add_argument("-r", "--no_render", action = "store_true", 
                        default = False,
                        help = "Do not display the game on each turn.")
    parser.add_argument("-t", "--time_allotted", type = float, default = 0.5,
                        help = "Time allotted for agent moves")
    parser.add_argument("-n", "--num_games", type = int, default = 1,
                        help = "Number of successive game simulations to run.")
    return parser

def lookup_agent(agent_str):
    """
    Determine the appropriate class associated with the command-line arg 
    string.  
    
    None is used as a default value for an agent-type that the program does 
    not currently handle.
    """
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
        display = TTTDisplay()
    else:
        raise RuntimeError("Unexpected game type.")

    agent1 = lookup_agent(args.agent1)
    agent2 = lookup_agent(args.agent2)

    if agent1 is None or agent2 is None:
        raise RuntimeError("Unexpected agent type.")
        
    if args.no_render:
        display = NoDisplay()
    elif args.console_render:
        display = ConsoleDisplay()

    time = args.time_allotted

    num_games = args.num_games

    simulator = Simulator(game, [agent1, agent2], time, display)
    simulator.run_games(num_games)
