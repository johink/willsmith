# Monte Carlo Tree Search

An implementation of the MCTS algorithm as an adversarial game playing agent.  

More details about the algorithm can be found on Wikipedia 
[here](https://en.wikipedia.org/wiki/Monte_Carlo_tree_search).  

Work is being done along with [John Bourassa](https://github.com/johink).  

## Included

The repository currently has an implementation of Nested Tic-Tac-Toe.  This 
plays similarly to the standard game, except instead of 9 spaces there are 
9 inner Tic-Tac-Toe boards to play.  Players can choose any legal move on any 
inner board, and the winner of an inner board claims that space on the outer 
board.  

> Havannah implementation coming soon.

Included agent types:  
- MCTSAgent:  runs the aforementioned algorithm for action selection  
- RandomAgent: randomly chooses an action from the action space on each turn  
- HumanAgent: prompts user for action to take  

## To Run

Run `python main.py -h` to see the currently available options.  
