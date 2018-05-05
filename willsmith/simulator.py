from logging import getLogger
from random import random

from agents.human_agent import HumanAgent


class Simulator:
    """
    Game simulator that manages running a game and agent players.
    """

    def __init__(self, game, agent_list, time_allowed, gui_display):
        """
        """
        self.game = game(gui_display)
        self.agents = [(agent(i, gui_display) 
                            if agent is not HumanAgent 
                            else agent(i, gui_display, self.game.ACTION))
                            for i, agent in enumerate(agent_list)]

        self.time_allowed = time_allowed
        self.logger = getLogger(__name__)

    def _initialize_game_run(self):
        """
        """
        self.game.reset()
        for agent in self.agents:
            agent.reset()

    def run_mdp(self, mdp, agent, num_trials):
        """
        """
        total_time_steps = 0
        for i in range(num_trials):
            self.logger.info("Trial {}/{}".format(i + 1, num_trials))
            #print("trial {}".format(i+1))
            num_steps = self._run_trial(mdp, agent)
            total_time_steps += num_steps
            #print("reward:{}; timesteps:{}".format(mdp.total_reward, mdp.timesteps))

        #print(agent.weights)
        self.logger.info("Trials complete.")
        input("\nPress enter key to end.")

    def _run_trial(self, mdp, agent):
        """
        """
        mdp.reset()
        prev_state = None

        while not mdp.is_terminal():
            action = agent.get_next_action(mdp.copy())

            prev_state = mdp.copy()
            reward, terminal = mdp.step(action)

            agent.update(prev_state, mdp, reward, action, terminal)

        return mdp.timesteps

    def run_games(self, num_games):
        """
        Run num_games number of game simulations.
        """
        if len(self.agents) != self.game.NUM_PLAYERS:
            raise RuntimeError("Incorrect number of agents for game type.")

        for i in range(num_games):
            self.logger.info("Game {}/{}".format(i + 1, num_games))
            self._initialize_game_run()
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
        for agent in self.agents:
            self.logger.debug("Agent {} start {}".format(agent.agent_id, agent))

        while not self.game.is_terminal():
            current_agent = self.agents[self.game.current_agent_id]
            action = current_agent.search(self.game.copy(), self.time_allowed)
            self.logger.debug("Agent {} {}".format(current_agent.agent_id, current_agent))
            self._advance_by_action(action)

        self.logger.info("Winning agent is {}".format(self.game.get_winning_id()))
        self.logger.debug("Final state\n{}".format(self.game))

    def _advance_by_action(self, action):
        """
        Update the game and agents with the given action.
        """
        self.logger.debug("Agent {} action {}".format(self.game.current_agent_id, action))
        agent_id_for_action = self.game.current_agent_id

        self.game.take_action(action)
        for agent in self.agents:
            agent.take_action(action, agent.agent_id == agent_id_for_action)
