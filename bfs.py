from pacman_module.game import Agent
from pacman_module.pacman import Directions
from collections import deque


class PacmanAgent(Agent):

    def __init__(self, args):
        """
        Arguments:
        ----------
        - `args`: Namespace of arguments from command-line prompt.
        """
        self.args = args

        #List to contain the path to the next food item
        self.nextactions = list()
        
    def construct_path(self, state, meta):
        """ 
        Produce a backtrace of the actions taken to find the food dot, using the 
        recorded meta dictionary
        Arguments:
        ----------
        - `state`: the current game state. 
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

        action_list.reverse()
        return action_list

    def computeNextTree(self, state):
        """
        Given a pacman state, computes a path from that state to a state
        where pacman has eaten one food dot.
        Arguments:
        ----------
        - `state`: the current game state. 
        """
        # a FIFO queue
        queue = deque()

        # an empty set to maintain visited nodes
        visited = set()

        # a dictionary to maintain meta information (used for path formation)
        # key -> (parent state, action to reach child)
        meta = dict()

        queue.append(state) #Append root
        meta[state] = (None, None)

        while queue: # While not empty
            #Pick one available state
            current_node = queue.popleft()

            # We found one food dot so we stop and compute a path.
            if current_node.isWin():
                return self.construct_path(current_node, meta)

            #Generate the next succesors of the current state
            successors = current_node.generatePacmanSuccessors()
            for successor in successors:
                #Successor was already visited
                if hash((successor[0].getPacmanPosition(), successor[0].getFood())) in visited:
                    continue
                #Successor wasn't visisted, we enqueue it
                if successor[0] not in queue:
                    meta[successor[0]] = (current_node, successor[1]) # create metadata for these nodes
                    queue.append(successor[0])
            
            # add the current node to the visited set
            visited.add(hash((current_node.getPacmanPosition(), current_node.getFood())))
         
    def get_action(self, state):

        """
        Given a pacman game state, returns a legal move.
        Arguments:
        ----------
        - `state`: the current game state.
        Return:
        -------
        - A legal move as defined in `game.Directions`.
        """

        if not self.nextactions:
            self.nextactions = self.computeNextTree(state)

        return self.nextactions.pop(0)