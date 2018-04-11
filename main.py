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

from games.havannah.havannah import Havannah
from games.ttt.nested_ttt import NestedTTT

from willsmith.simple_displays import ConsoleDisplay, NoDisplay
from willsmith.simulator import Simulator


HAVANNAH_LABELS = ["Havannah", "hav"]
NESTEDTTT_LABELS = ["NestedTTT", "ttt"]
AGENT_LABELS = ["mcts", "rand", "human"]

def create_parser():
    parser = ArgumentParser(description = "Run agents through simulations")

    parser.add_argument("game_choice", type = str, 
                        choices = NESTEDTTT_LABELS + HAVANNAH_LABELS,
                        help = "The game for the agents to play")
    parser.add_argument("-a", "--agents", nargs = '*', 
                        default = ["mcts", "rand"], choices = AGENT_LABELS, 
                        help = "Agent types")
    parser.add_argument("-c", "--console-render", action = "store_true",
                        default = False,
                        help = "Render the game on the command-line")
    parser.add_argument("-n", "--num_games", type = int, default = 1,
                        help = "Number of successive game simulations to run.")
    parser.add_argument("-r", "--no_render", action = "store_true", 
                        default = False,
                        help = "Do not display the game on each turn.")
    parser.add_argument("-t", "--time_allotted", type = float, default = 0.5,
                        help = "Time allotted for agent moves")
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

    if args.game_choice in NESTEDTTT_LABELS:
        game = NestedTTT
    elif args.game_choice in HAVANNAH_LABELS:
        game = Havannah
    else:
        raise RuntimeError("Unexpected game type.")

    agents = []
    for agent_str in args.agents:
        agent = lookup_agent(agent_str)
        if agent is None:
            raise RuntimeError("Unexpected agent type.")
        agents.append(agent)
        
    display = game.DISPLAY
    if args.no_render:
        display = NoDisplay
    elif args.console_render:
        display = ConsoleDisplay

    time = args.time_allotted

    num_games = args.num_games

    simulator = Simulator(game, agents, time, display())
    simulator.run_games(num_games)
