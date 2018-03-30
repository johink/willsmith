from agents.human_agent import HumanAgent


class Simulator():
    """
    Game simulator that manages running a game and agent players.
    """

    def __init__(self, game, agent_list, time_allowed, display_controller):
        """
        Store the game and agent classes for later instantiation when a 
        simulation is started.  Also stores the display controller for 
        use during simulation.
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
        self.display_controller.start()
        for i in range(num_games):
            print("Game {}/{}".format(i + 1, num_games))
            self.initialize_match()
            self._run_game()
        input("Games complete, press enter key to end.")

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
            self.display_controller.update_display(self.current_game, action)

        print("Winning agent id:  {}".format(self.current_game.get_winning_id()))

    def _advance_by_action(self, action):
        """
        Pass the action to the game to progress the game state.  

        Only if it is legal, the game state and agents are updated with the 
        action.
        """
        if self.current_game.take_action_if_legal(action):
            for agent in self.current_agents:
                agent.take_action(action)
    
    def _add_prompt_to_human_agents(self, action_prompt):
        """
        Add the action prompt to all HumanAgent instances.

        Used to update those agents with the proper game-specific prompt so 
        users can choose actions.
        """
        for agent in self.current_agents:
            if isinstance(agent, HumanAgent):
                agent.action_prompt = action_prompt
