from pacman_module.game import Agent
from pacman_module.pacman import Directions
from random import randint
from collections import deque


class PacmanAgent(Agent):


    # a FIFO open_set
    open_set = deque()

    # an empty set to maintain visited nodes
    closed_set = set()

    # a dictionary to maintain meta information (used for path formation)
    # key -> (parent state, action to reach child)
    meta = dict()

    #List to contains the final path to the food source
    nextactions = list()
    
    
    def __init__(self, args):
        """
        Arguments:
        ----------
        - `args`: Namespace of arguments from command-line prompt.
        """
        self.args = args

    def construct_path(self, state, meta):
        """ Produce a backtrace of the actions taken to find the goal node, using the 
            recorded meta dictionary
        """

        print("INSIDE !!!!!!!!!!!!!!!!!")
        
        action_list = list()
        
        # Continue until you reach root meta data (i.e. (None, None))
        while meta[state][0] is not None:
            state, action = meta[state]
            action_list.append(action)
        
        action_list.reverse()
        return action_list


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
        #Root of the tree (May be wrong)
        if not self.closed_set: #Only append root at start
            self.open_set.append(state)
            #print("State %s",state.getNumFood())
            self.meta[state] = (None, None)

            while self.open_set: #While not empty
                subtree_root = self.open_set.popleft()
                #print("Subtree %s" ,subtree_root.getNumFood())

                # We found the node we wanted so stop and emit a path.
                if subtree_root.isWin() : #We ate all the food
                    self.nextactions = self.construct_path(subtree_root, self.meta)
                    break
            
                #Generate all the legal actions from the current state
                legals = subtree_root.getLegalActions()
                legals.remove(Directions.STOP)

                for action in legals:
                    successor = subtree_root.generatePacmanSuccessor(action)
                    #Successor was already visited
                    if successor in self.closed_set:
                        continue
                    #Successor wasn't visisted, we enqueue it
                    if successor not in self.open_set:
                        self.meta[successor] = (subtree_root, action) # create metadata for these nodes
                        self.open_set.append(successor)
                #print(subtree_root)
                self.closed_set.add(subtree_root)

        if self.nextactions:
            nextaction = self.nextactions.pop(0)
            print(self.nextactions)
        else:
            nextaction = Directions.STOP
        return nextaction
