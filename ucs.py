from pacman_module.game import Agent
from pacman_module.pacman import Directions
from pacman_module.util import PriorityQueue


class PacmanAgent(Agent):

    def __init__(self, args):
        """
        Arguments:
        ----------
        - `args`: Namespace of arguments from command-line prompt.
        """
        self.args = args
        self.nextactions = list() #List to contain the path to the next food item
        
    def construct_path(self, state, meta):
        """ 
        Produce a backtrace of the actions taken to find the food dot, using the 
        recorded meta dictionary
        Arguments:
        ----------
        - `state`: the current game state. 
        - `meta`: dictionnary containing the path information from 
                    one node to another
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
        fringe = PriorityQueue() # a priority queue
        visited = set() # an empty set to maintain visited nodes

        # a dictionary to maintain path information : key -> (parent state, action to reach child)
        meta = dict()
        meta[state] = (None, None)

        #Append root
        fringe.push(state,0) 
        
        # While not empty
        while fringe: 
            #Pick one available state
            current_node = fringe.pop()

            if current_node[1].isWin():
                return self.construct_path(current_node[1], meta)

            #Generate the next successors of the current state
            successors = current_node[1].generatePacmanSuccessors()
            for successor in successors:
                #Successor was already visited
                if hash((successor[0].getPacmanPosition(), successor[0].getFood())) not in visited:
                    #Successor wasn't visisted, we enfringe it
                    meta[successor[0]] = (current_node[1], successor[1]) 
                    
                    x, y = successor[0].getPacmanPosition()
                    #Assign priority based on the presence of food
                    priority = 0 if successor[0].hasFood(x, y) else 1 
                    fringe.push(successor[0], current_node[0] + priority)

            #Add the current node to the visited set
            visited.add(hash((current_node[1].getPacmanPosition(), current_node[1].getFood())))
         
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