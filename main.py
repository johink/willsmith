"""
The main executable that instantiates the simulator with the proper game and 
agents, as specified by the command-line arguments.

Run python main.py -h for the explanation of command-line arguments.

See README.md for a full-project breakdown.
"""


from argparse import ArgumentParser
from logging import FileHandler, Formatter, StreamHandler, DEBUG, INFO, getLogger

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

LOG_FILENAME = "djjazzyjeff.log"
FILE_LOG_FORMAT = "%(asctime)s::%(name)s::%(levelname)s::%(message)s"
STDERR_LOG_FORMAT = "%(message)s"
TIMESTAMP_FORMAT = "%H:%M:%S"

def create_logger(debug):
    """
    Create and configure the root logger that other loggers refer to.
    
    There are two handlers, one to write out to the file and one to write 
    to console.  
    
    The console handler is always set to only display INFO level messages to 
    prevent clutter.  The file handler can be optionally set to DEBUG level 
    to capture additional information.
    """
    stderr_level = INFO
    file_level = INFO
    if debug:
        file_level = DEBUG

    logger = getLogger()
    logger.setLevel(file_level)

    file_handler = FileHandler(LOG_FILENAME, mode = 'w')
    file_handler.setLevel(file_level)
    file_handler.setFormatter(Formatter(FILE_LOG_FORMAT, TIMESTAMP_FORMAT))

    stderr_handler = StreamHandler()
    stderr_handler.setLevel(stderr_level)
    stderr_handler.setFormatter(Formatter(STDERR_LOG_FORMAT, TIMESTAMP_FORMAT))

    logger.addHandler(file_handler)
    logger.addHandler(stderr_handler)
    return logger

def create_parser():
    parser = ArgumentParser(description = "Run agents through simulations")

    parser.add_argument("game_choice", type = str, 
                        choices = NESTEDTTT_LABELS + HAVANNAH_LABELS,
                        help = "The game for the agents to play")
    parser.add_argument("-a", "--agents", nargs = '*', 
                        default = ["mcts", "rand"], choices = AGENT_LABELS, 
                        help = "Agent types")
    parser.add_argument("-c", "--console_display", action = "store_true",
                        default = False,
                        help = "Render the game on the command-line")
    parser.add_argument("-d", "--debug", action = "store_true",
                        default = False,
                        help = "Turn on debug-level logging")
    parser.add_argument("-n", "--num_games", type = int, default = 1,
                        help = "Number of successive game simulations to run.")
    parser.add_argument("-r", "--no_display", action = "store_true", 
                        default = False,
                        help = "Do not display the game on each turn.")
    parser.add_argument("-t", "--time_allotted", type = float, default = 0.5,
                        help = "Time allotted for agent moves")
    return parser

def lookup_agent(num, agent_str):
    lookup = {"mcts" : MCTSAgent, "rand" : RandomAgent, "human" : HumanAgent}
    try:
        agent = lookup[agent_str]
    except KeyError:
        raise RuntimeError("Unexpected agent string type.")
    getLogger().debug("Agent {} is {}".format(num, agent.__name__))
    return agent

def lookup_game(game_str):
    if game_str in NESTEDTTT_LABELS:
        game = NestedTTT
    elif game_str in HAVANNAH_LABELS:
        game = Havannah
    else:
        raise RuntimeError("Unexpected game type.")
    getLogger().info("Game is {}".format(game.__name__))
    return game

def adjust_display(game, no_display, console):
    if no_display:
        getLogger().debug("Non-display option chosen")
        game.DISPLAY = NoDisplay
    elif console:
        getLogger().debug("Console display chosen")
        game.DISPLAY = ConsoleDisplay

if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()

    logger = create_logger(args.debug)

    game = lookup_game(args.game_choice)
    agents = [lookup_agent(i, astr) for i, astr in enumerate(args.agents)]
        
    adjust_display(game, args.no_display, args.console_display)

    time = args.time_allotted
    logger.debug("Agents have {} seconds per turn".format(time))
    num_games = args.num_games
    logger.debug("{} games will be played".format(num_games))

    simulator = Simulator(game, agents, time)
    simulator.run_games(num_games)
