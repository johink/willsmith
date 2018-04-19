from logging import getLogger

from agents.human_agent import HumanAgent


class Simulator:
    """
    Game simulator that manages running a game and agent players.
    """

    def __init__(self, game, agent_list, time_allowed, gui_display):
        """
        Prepares all of the objects for a game simulation:

        - Store the game and agent classes for later instantiation when a 
        simulation is started.  
        - Adds action information to HumanAgents if they are playing.
        - Constructs display classes for game and possibly agents.
        - Retrieves the logger instance for this module.
        - Checks the number of players expected by the game against the 
        number of agents provided.
        """
        self.game = game
        self.agents = agent_list
        if len(self.agents) != self.game.NUM_PLAYERS:
            raise RuntimeError("Incorrect number of agents for game type.")

        self.time_allowed = time_allowed
        self.logger = getLogger(__name__)

        self._add_prompt_to_human_agents(self.game.ACTION)
        self._create_displays(gui_display)

    def _create_displays(self, gui_display):
        self.game_display_controller = self.game.DISPLAY()
        self.agent_display_controllers = dict()

        if gui_display:
            for i, agent in enumerate(self.agents):
                if agent.GUI_DISPLAY is not None:
                    self.agent_display_controllers[i] = agent.GUI_DISPLAY()
        

    def initialize_match(self):
        """
        Create instances of the game and the agents, in preparation for a 
        new simulation.
        """
        self.current_game = self.game()
        self.current_agents = [agent(i) for i, agent in enumerate(self.agents)]

        self.game_display_controller.reset_display(self.current_game)
        for agent_id, display in self.agent_display_controllers.items():
            display.reset_display(self.current_agents[agent_id])
        
    def run_games(self, num_games):
        """
        Run num_games number of game simulations.
        """
        self.game_display_controller.start(is_main = True)
        for display in self.agent_display_controllers.values():
            display.start(is_main = False)

        for i in range(num_games):
            self.logger.info("Game {}/{}".format(i + 1, num_games))
            self.initialize_match()
            self._run_game()
        self.logger.info("Games complete")
        input("\nPress enter key to end.")

    def _run_game(self):
        """
        Run a playthrough of the game.

        Progresses through the list of agents repeatedly, prompting them for 
        an action selection and then taking that action, until a terminal 
        state of the game is reached.
        """
        for agent in self.current_agents:
            self.logger.debug("Agent {} start {}".format(agent.agent_id, agent))
        while not self.current_game.is_terminal():
            current_agent = self.current_agents[self.current_game.current_agent_id]
            action = current_agent.search(self.current_game.copy(), self.time_allowed)
            self.logger.debug("Agent {} {}".format(current_agent.agent_id, current_agent))
            self._advance_by_action(action)

        self.logger.info("Winning agent is {}".format(self.current_game.get_winning_id()))
        self.logger.debug("Final state\n{}".format(self.current_game))

    def _advance_by_action(self, action):
        """
        Update the game, agents, and display with the given action.

        The update only applies if the action is deemed legal by the game.  
        Illegal actions still progress the game by a turn, skipping the agent 
        who provided the action.

        An agent display is only updated after it takes actions.
        """
        self.logger.debug("Agent {} action {}".format(self.current_game.current_agent_id, action))
        action_agent_id = self.current_game.current_agent_id

        if self.current_game.take_action_if_legal(action):
            self.game_display_controller.update_display(self.current_game, action)
            for agent_id, display in self.agent_display_controllers.items():
                if agent_id == action_agent_id:
                    display.update_display(self.current_agents[agent_id], action)

            for agent in self.current_agents:
                agent.take_action(action)
    
    def _add_prompt_to_human_agents(self, action):
        """
        Update any HumanAgents with the information needed to input the 
        actions for the given game.
        """
        for agent in self.agents:
            if agent is HumanAgent:
                agent.add_input_info(action.INPUT_PROMPT, action.parse_action)
