from willsmith.agent import Agent


class HumanAgent(Agent):
    """
    Agent that relies on user input to make action choices.

    It relies on its action_prompt attribute, set externally by the 
    simulator, to provide the proper prompts and to construct the action.
    """

    def __init__(self, agent_id):
        super().__init__(agent_id)
        
        self.action_prompt = None

    def search(self, state, allotted_time):
        """
        Prompt the player for an action until a legal action is chosen, then 
        return it.
        """
        legal_actions = state.get_legal_actions()
        player_action = None
        while player_action not in legal_actions:
            if player_action is not None:
                print("Last move was not legal, please try again.\n")

            player_action = self.action_prompt(legal_actions)

        return player_action

    def take_action(self, action):
        pass
