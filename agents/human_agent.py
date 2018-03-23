from agents.agent import Agent


class HumanAgent(Agent):
    """
    Agent that prompts for actions from a human player.
    """

    def __init__(self, agent_id):
        super().__init__(agent_id)

    def search(self, state, max_time):
        legal_moves = state.get_legal_actions()
        player_move = None
        while player_move not in legal_moves:
            if player_move is not None:
                print("Last move was not legal, please try again.\n")

            move = legal_moves[0][1][1]

            outer_input = "Please choose board for {} move(row,col):  ".format(move)
            inner_input = "Please choose board position for move(row,col):  "

            outer_pos = tuple(map(int, input(outer_input).split(',')))
            inner_pos = tuple(map(int, input(inner_input).split(',')))

            player_move = (outer_pos, (inner_pos, move))

        return player_move

    def take_action(self, action):
        pass
