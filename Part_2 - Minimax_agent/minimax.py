from pacman_module.game import Agent
from pacman_module.pacman import Directions
import math



class PacmanAgent(Agent):
    def __init__(self, args):
        """
        Arguments:
        ----------
        - `args`: Namespace of arguments from command-line prompt.
        """
        self.args = args
        self.nb_ghosts = 0
        self.visited = set()

    def get_info(self, state):
        """Returns information about a state to uniquely identify it.
        Arguments:
        ----------
        - `state`: the current game state.

        Returns:
        ----------
        Tuple of 
            -the hash value of Pacmans position, 
            -the hash value of the food matrix 
            -the tuple of ghost positions
        """
        pos = state.getPacmanPosition()
        food = state.getFood()
        ghost_pos = state.getGhostPositions()        

        return tuple([hash(pos), hash(food), tuple(ghost_pos)])

    def minimax_decision(self, state, nb_ghosts):
        """Returns the best legal action according to the minimax algorithm.
        Arguments:
        ----------
        - `state`: the current game state.
        - `nb_ghosts`: the number of ghosts in the grid.

        Returns:
        ----------
        The best legal action for the defined maximal depth.
        """
        values = list()
        actions = list()

        # Add the current node to the visited set
        curr_info = self.get_info(state)
        self.visited.add(curr_info)

        # For each successor of the current node            
        pac_successors = state.generatePacmanSuccessors()
        for next_state, next_action in pac_successors:
            value = self.min_value(next_state, nb_ghosts)
            values.append(value)
            actions.append(next_action)
            
        index = values.index(max(values))

        return actions[index]
    
    def max_value(self, state, ghost_index):
        """
        Arguments:
        ----------
        - `state`: the current game state.
        - `ghost_index`: the index of the ghost agent.

        Returns:
        ----------
        The max utility value of the successor nodes.
        """
        # Check the terminal test
        if state.isWin():
            return state.getScore()  # Returns the utility value
        if state.isLose():
            return - math.inf
        
        # Initialize value
        value = - math.inf
  
        # Add the current node to the visited set
        curr_info = self.get_info(state)
        self.visited.add(curr_info)
        
        pac_successors = state.generatePacmanSuccessors()
        for pac_successor in pac_successors:
            # Check if it was already visited
            if self.get_info(pac_successor[0]) in self.visited:
                continue
            value = max(value, self.min_value(pac_successor[0], ghost_index))
        
        if value == - math.inf:
            value = math.inf

        return value

    def min_value(self, state, ghost_index):
        """
        Arguments:
        ----------
        - `state`: the current game state.
        - `ghost_index`: the index of the ghost agent.

        Returns:
        ----------
        The min utility value of the successor nodes.
        """
        # Check the terminal test
        if state.isWin():
            return state.getScore()  # Returns the utility value
        if state.isLose():
            return - math.inf
        
        # Initialize value
        value = math.inf

        # Add the current node to the visited set
        curr_info = self.get_info(state)
        self.visited.add(curr_info)

        ghost_successors = state.generateGhostSuccessors(ghost_index)
        for ghost_successor in ghost_successors:
            if ghost_index > 1:
                value = min(value, self.min_value(ghost_successor[0], ghost_index-1))
            else:
                value = min(value, self.max_value(ghost_successor[0], self.nb_ghosts))

        if value == math.inf:
            value = - math.inf

        return value

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
        # Get the number of ghosts in the layout
        self.nb_ghosts = state.getNumAgents() - 1

        # Compute next move
        next_move = self.minimax_decision(state, self.nb_ghosts)
        self.visited = set()

        return next_move
