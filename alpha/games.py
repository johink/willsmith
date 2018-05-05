import torch

class NestedTTT:

    anti_diag_tensor = torch.ByteTensor([[1 if r + c == 2 else 0 for c in range(3)] for r in range(3)])

    def __init__(self):
        #Board State Tensor
        #Outermost dimension:
        #First value represents Player 0's (X's) holdings, second represents O's
        #Third is filled with the number of the current player to move (0 = X, 1 = O)
        #Rest of the dimensions are (Outer Row, Outer Column, Inner Row, Inner Column)
        self.state = torch.full((3, 3, 3, 3, 3), 0, dtype = torch.float32, requires_grad = False)

        #Valid Move Tensor
        #(Outer Row, Outer Column, Inner Row, Inner Column)
        self.valid_moves = torch.full((3, 3, 3, 3), 1, dtype = torch.uint8, requires_grad = False)

        #Summary Board Tensor
        #(Player, Row, Column)
        self.summary_boards = torch.full((2, 3, 3), 0, dtype = torch.uint8, requires_grad = False)

        #Current Player
        self.current_player = 0

    def check_win(self, board):
        """
        Short-circuits if current player has less than 3 squares on the current board
        If they do, checks all rows, columns, and diagonals for a win

        Returns 0 if the current player did not win the board in question, or 1 if they did
        """
        if board.sum().item() < 3:
            return 0
        else:
            return (board.sum(0) == 3).any().item() or \
                   (board.sum(1) == 3).any().item() or \
                   (board.diag().sum() == 3).item()   or \
                   (board.masked_select(self.anti_diag_tensor).sum() == 3).item()

    def make_move(self, move):
        """
        Takes a move:
          ({0 for X, 1 for O}, outer row, outer col, inner row, inner col)
        Returns 1 if the move won the game, 0 otherwise
        """
        if not self.valid_moves[move[1:]].item():
            raise ValueError("Invalid move placement")
        if move[0] != self.state[2,0,0,0,0].item():
            raise ValueError("Only the current player can make a move")
        self.state[move] = 1
        self.valid_moves[move[1:]] = 0
        self.state[2] = 1 - self.state[2]

        if self.check_win(self.state[move[:3]]):
            self.summary_boards[move[:3]] = 1
            self.valid_moves[move[1:3]] = 0
            if self.check_win(self.summary_boards[move[0]]):
                self.valid_moves.fill_(0)
                return 1

        return 0

    def undo_move(self, move):
        if not self.state[move].item():
            raise ValueError("Can only undo where a move has been played")
        if move[0] == self.current_player:
            raise ValueError("Cannot undo a move for the current player")
        if self.state[(2,0,0,0,0)].item() != self.current_player:
            raise ValueError("Desynchronization between current player and state tensor")
        self.state[move] = 0
        self.valid_moves[move[1:3]] = 1 - self.state[:2, move[1], move[2]].sum(0)

        self.summary_boards[move[:3]] = 0
        self.state[2] = 1 - self.state[2]

    def switch_player(self):
        self.current_player = (self.current_player + 1) % 2

    def copy(self):
        c = self.__new__(NestedTTT)
        c.state = self.state.clone().detach().detach()
        c.valid_moves = self.valid_moves.clone().detach()
        c.summary_boards = self.summary_boards.clone().detach()
        c.current_player = self.current_player
        return c

    def reset(self):
        self.__init__()

    def get_valid_moves(self):
        return self.valid_moves.nonzero().tolist()
