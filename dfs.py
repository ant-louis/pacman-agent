from pacman_module.game import Agent
from pacman_module.pacman import Directions


class PacmanAgent(Agent):

    nb_foods = None

    #List to contain the path to the next food
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

        # a stack for the nodes to explore
        stack = list()

        # an empty set to maintain visited nodes
        visited = set()

        # a dictionary to maintain meta information (used for path formation)
        # key -> (parent state, action to reach child)
        meta = dict()

        stack.append(state) #Append root
        meta[state] = (None, None)

        while stack: # While not empty
            #Pick one available state
            current_node = stack.pop()

            # We found one food dot so we stop and compute a path.
            if current_node.getNumFood() < self.nb_foods:
                self.nb_foods = current_node.getNumFood()
                return self.construct_path(current_node, meta)

            #Generate the next succesors of the current state
            successors = current_node.generatePacmanSuccessors()
            for successor in successors:
                #Successor was already visited
                if (successor[0].getPacmanPosition(), successor[0].getNumFood()) in visited:
                    continue
                #Successor wasn't visisted, we push it onto the stack
                if successor[0] not in stack:
                    meta[successor[0]] = (current_node, successor[1]) # create metadata for these nodes
                    stack.append(successor[0])
            
            visited.add((current_node.getPacmanPosition(), current_node.getNumFood()))
         
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
        self.nb_foods = state.getNumFood()

        if not self.nextactions:
            self.nextactions = self.computeNextTree(state)

        return self.nextactions.pop(0)
