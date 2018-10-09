from pacman_module.game import Agent
from pacman_module.pacman import Directions
from random import randint
from collections import deque


class PacmanAgent(Agent):


    startingNumFood = None

    # a FIFO queue
    queue = deque()

    # an empty set to maintain visited nodes
    visited = set()

    # a dictionary to maintain meta information (used for path formation)
    # key -> (parent state, action to reach child)
    meta = dict()

    #List to contain the path to the next food iteù
    nextactions = list()
    
    def __init__(self, args):
        """
        Arguments:
        ----------
        - `args`: Namespace of arguments from command-line prompt.
        """
        self.args = args
        

    def construct_path(self, state, meta):
        """ 
        Produce a backtrace of the actions taken to find the food dot, using the 
        recorded meta dictionary

        Arguments:
        ----------
        - `state`: the current game state. See FAQ and class
                   `pacman.GameState`.

        - `meta`: dictionnary containing the path information from one node to another

        Return:
        -------
        - A list of legal moves as defined in `game.Directions`
        """     
        action_list = list()
        
        # Continue until you reach root meta data (i.e. (None, None))
        while meta[state][0] is not None:
            state, action = meta[state]
            action_list.append(action)
        
        self.visited.clear()
        self.queue.clear()
        self.meta.clear()

        action_list.reverse()
        return action_list

    def computeNextTree(self, state):
        """
        Given a pacman state, computes a path from that state to a state
        where pacman has eaten one food dot.

        Arguments:
        ----------
        - `state`: the current game state. See FAQ and class
                   `pacman.GameState`.
        """
        self.queue.append(state) #Append root
        self.meta[state] = (None, None)

        while self.queue: # While not empty
            #Pick one available state
            subtree_root = self.queue.popleft()

            # We found one food dot so we stop and compute a path.
            if subtree_root.getNumFood() < self.startingNumFood:
                self.startingNumFood = subtree_root.getNumFood()
                return self.construct_path(subtree_root, self.meta)

            #Generate the next succesors of the current state
            successors = subtree_root.generatePacmanSuccessors()
            for successor in successors:
                #Successor was already visited
                if (successor[0].getPacmanPosition(), successor[0].getNumFood()) in self.visited:
                    continue
                #Successor wasn't visisted, we enqueue it
                if successor[0] not in self.queue:
                    self.meta[successor[0]] = (subtree_root, successor[1]) # create metadata for these nodes
                    self.queue.append(successor[0])
            
            self.visited.add((subtree_root.getPacmanPosition(), subtree_root.getNumFood()))
         
    def get_action(self, state):

        """
        Given a pacman game state, returns a legal move.

        Arguments:
        ----------
        - `state`: the current game state. See FAQ and class
                   `pacman.GameState`.

        Return:
        -------
        - A legal move as defined in `game.Directions`.
        """

        #Used to make sure that pacman eats a dot before passing
        #through the same position
        self.startingNumFood = state.getNumFood()

        if not self.nextactions:
            self.nextactions = self.computeNextTree(state)

        return self.nextactions.pop(0)
