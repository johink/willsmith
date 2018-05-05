from logging import getLogger


class Simulator:
    """
    """

    def __init__(self):
        self.logger = getLogger(__name__)

    def run_games(self, game, agents, time_allowed, num_games):
        """
        Run num_games number of game simulations.
        """
        if len(agents) != game.NUM_PLAYERS:
            raise RuntimeError("Incorrect number of agents for game type.")

        for i in range(num_games):
            self.logger.info("Game {}/{}".format(i + 1, num_games))
            self._run_game(game, agents, time_allowed)
        self.logger.info("Games complete")
        input("\nPress enter key to end.")

    def _run_game(self, game, agents, time_allowed):
        """
        """
        game.reset()
        for agent in agents:
            agent.reset()
            self.logger.debug("Agent {} start {}".format(agent.agent_id, agent))

        while not game.is_terminal():
            current_agent = agents[game.current_agent_id]
            action = current_agent.search(game.copy(), time_allowed)
            self.logger.debug("Agent {} {}".format(current_agent.agent_id, current_agent))
            self._advance_by_action(game, agents, action)

        self.logger.info("Winning agent is {}".format(game.get_winning_id()))
        self.logger.debug("Final state\n{}".format(game))

    def _advance_by_action(self, game, agents, action):
        """
        Update the game and agents with the given action.
        """
        self.logger.debug("Agent {} action {}".format(game.current_agent_id, action))
        agent_id_for_action = game.current_agent_id

        game.take_action(action)
        for agent in agents:
            agent.take_action(action, agent.agent_id == agent_id_for_action)

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
