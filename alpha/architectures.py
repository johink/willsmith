import torch.nn as nn
import torch.nn.functional as F

NUM_MOVES_TTT = 81 # Max number of valid moves in a game of NestedTTT

class NestedTTTNet(nn.Module):
    def __init__(self, inner_board_units = 32, outer_board_units = 64, final_units = 256, n_res_layers = 2):
        super(NestedTTTNet, self).__init__()
        self.n_res_layers = n_res_layers
        self.outer_board_units = outer_board_units
        self.final_units = final_units

        self.conv1 = nn.Conv2d(3, inner_board_units, 3, padding = 1)
        self.bn_inner = nn.BatchNorm2d(inner_board_units)
        self.res1 = nn.Conv2d(inner_board_units, inner_board_units, 3, padding = 1)

        self.conv2_collapse = nn.Conv2d(inner_board_units, outer_board_units, 3)
        self.bn_outer = nn.BatchNorm2d(outer_board_units)
        self.res2 = nn.Conv2d(outer_board_units, outer_board_units, 3, padding = 1)

        self.conv3_collapse = nn.Conv2d(outer_board_units, final_units, 3)
        self.bn_linear = nn.BatchNorm1d(final_units)

        self.policy_head = nn.Sequential(
            nn.Linear(final_units, NUM_MOVES_TTT),
            nn.Softmax(dim = 1)
        )

        self.value_head = nn.Sequential(
            nn.Linear(final_units, final_units // 2),
            nn.ReLU(),
            nn.Linear(final_units // 2, 1),
            nn.Tanh()
        )

    def forward(self, board_states):
        '''
        board_states.size() == (-1, 3, 3, 3, 3, 3)
                            == (batch_size, [x-owned, o-owned, turn-state], outer_row, outer_col, inner_row, inner_col)
        '''
        # Move the outer board states to the left so their intra-square can be resolved before introducing inter-square
        board_states = board_states.permute(0, 2, 3, 1, 4, 5).contiguous().view(-1, 3, 3, 3)

        x = F.relu(self.bn_inner(self.conv1(board_states)))
        for _ in range(self.n_res_layers):
            x_conv = F.relu(self.bn_inner(self.res1(x)))
            x = F.relu(x + self.bn_inner(self.res1(x_conv)))

        x = F.relu(self.bn_outer(self.conv2_collapse(x)))
        x = x.view(-1, 3, 3, self.outer_board_units).permute(0, 3, 1, 2).contiguous() # Move them back to the right

        for _ in range(self.n_res_layers):
            x_conv = F.relu(self.bn_outer(self.res2(x)))
            x = F.relu(x + self.bn_outer(self.res2(x_conv)))

        x = F.relu(self.bn_linear(self.conv3_collapse(x).view(-1, self.final_units)))

        policy = self.policy_head(x)
        value = self.value_head(x)

        return policy, value
