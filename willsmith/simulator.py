from agents.human_agent import HumanAgent


class Simulator():
    """
    Game simulator that manages running a game and agent players.
    """

    def __init__(self, game, agent_list, time_allowed, display_controller):
        """
        Store the game and agent classes.
        """
        self.game = game
        self.agents = agent_list
        self.time_allowed = time_allowed
        self.display_controller = display_controller

        self.current_game = None
        self.current_agents = None

    def initialize_match(self):
        """
        Create instances of the game and the agents, in preparation for a 
        new simulation.
        """
        self.current_game = self.game(len(self.agents))
        self.current_agents = [agent(i) for i, agent in enumerate(self.agents)]

        self._add_prompt_to_human_agents(self.current_game.ACTION.prompt_for_action)
        self.display_controller.reset_display()
        
    def run_games(self, num_games):
        """
        Run num_games number of game simulations.
        """
        self.initialize_match()
        for _ in range(num_games):
            self._run_game()

    def _run_game(self):
        """
        Run a playthrough of the game.

        Progresses through the list of agents repeatedly, prompting them for 
        an action selection and then taking that action, until a terminal 
        state of the game is reached.
        """
        while not self.current_game.is_terminal():
            current_agent = self.current_agents[self.current_game.current_agent_id]
            action = current_agent.search(self.current_game.copy(), self.time_allowed)
            self._advance_by_action(action)
            self.display_controller.update_display(self.current_game)
        print("Winning agent id:  {}".format(self.current_game.get_winning_id()))

    def _advance_by_action(self, action):
        """
        Advance the game state and each of the agent's internal states by the 
        given action.

        The action is checked if it is legal before taking it, but the 
        current agent's turn is over regardless.
        """
        if self.current_game.is_legal_action(action):
            self.current_game.take_action(action)
            for agent in self.current_agents:
                agent.take_action(action)
        else:   
            # awkwardly catches the case where an agent manages to make an 
            # illegal action choice and the game needs to be progressed
            self.current_game.progress_game(lambda: None)()
    
    def _add_prompt_to_human_agents(self, action_prompt):
        """
        Add the action prompt to all HumanAgent instances.

        Used to update those agents with the proper game-specific prompt so 
        users can choose actions.
        """
        for agent in self.current_agents:
            if isinstance(agent, HumanAgent):
                agent.action_prompt = action_prompt
