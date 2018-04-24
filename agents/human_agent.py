from agents.displays.human_display import HumanDisplay
from willsmith.agent import Agent


class HumanAgent(Agent):
    """
    Agent that relies on user input to make action choices.

    It relies on its action_prompt attribute, set externally by the 
    simulator, to provide the proper prompts and to construct the action.
    """
    
    GUI_DISPLAY = None #HumanDisplay is not yet ready
    INPUT_PROMPT = None
    INPUT_PARSER = None

    def __init__(self, agent_id):
        super().__init__(agent_id)

        if self.INPUT_PROMPT is None or self.INPUT_PARSER is None:
            raise RuntimeError("INPUT_PROMPT and INPUT_PARSER need to be set for HumanAgent to be able to create actions from user input.")

    def search(self, state, allotted_time):
        """
        Prompt the player for an action until a legal action is chosen, then 
        return it.
        """
        legal_actions = state.get_legal_actions()
        player_action = HumanAgent.INPUT_PARSER(input(HumanAgent.INPUT_PROMPT))
        while player_action not in legal_actions:
            print("Last move was not legal, please try again.\n")
            player_action = HumanAgent.INPUT_PARSER(input(HumanAgent.INPUT_PROMPT))

        return player_action

    def take_action(self, action):
        pass

    @staticmethod
    def add_input_info(input_prompt, input_parser):
        HumanAgent.INPUT_PROMPT = input_prompt
        HumanAgent.INPUT_PARSER = input_parser

    def __str__(self):
        return ""
