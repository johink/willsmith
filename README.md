# Monte Carlo Tree Search

An implementation of the MCTS algorithm as an adversarial game playing agent.  

Work is being done along with [John Bourassa](https://github.com/johink).  

## Included

#### Games included:
- Nested Tic-Tac-Toe
> Tic-Tac-Toe, but each square on the outer board is another Tic-Tac-Toe board.
> 
> The game is played as standard Tic-Tac-Toe, except there are 9 inner 
> boards to make moves on.  Winning an inner board claims that space for 
> the winner on the outer board.  Draws result in a square that does not 
> count for either side.  Winning the game requires winning 3 inner boards 
> in a row, forming a win on the outer board.

- Havannah (coming soon)
> The game of Havannah is played on a hex board that is typically 10 hexes to 
> a side.  
> 
> Players alternate turns placing stones, or coloring hexes in our 
> case, in previously unchosen hexes.  Play continues until one player has 
> formed one of three different winning configurations:  a ring, fork, or 
> bridge.

#### Included agent types:  
- MCTSAgent
> Planning agent that makes decisions based on Monte Carlo Tree Search.
> 
> Computes as many runs as possible in the time alloted, where a run 
> consists of the following stages:
> 
> >  Selection       -   Start at root, use UCB to choose actions until 
> >                        action does not produce child  
> >  Expansion       -   Create new node  
> >  Simulation      -   Play out game until reaching a terminal state  
> >  Backpropagation -   Update win/trial counters for new node and all parents  
> 
> Then, it chooses the action with the most trials and returns that.

- RandomAgent
> Agent that chooses random actions regardless of the game state.

- HumanAgent
> Agent that relies on user input to make action choices.

## To Run

Run `python main.py -h` to see the available options for games and agents.  
An example game of Nested Tic-Tac-Toe can be shown by running 
`python main.py ttt`, which will start the game with a MCTSAgent against a 
RandomAgent with a default time-allowed of 1 second.
