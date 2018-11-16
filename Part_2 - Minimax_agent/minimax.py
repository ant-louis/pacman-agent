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

    def __get_info(self, state):
        """Returns information about a state to uniquely identify it.
        Arguments:
        ----------
        - `state`: the current game state.

        Returns:
        ----------
        Tuple of
            -the hash value of Pacmans position
            -the hash value of the food matrix
            -the tuple of ghost positions
        """
        pos = state.getPacmanPosition()
        food = state.getFood()
        ghost_pos = state.getGhostPositions()     

        return tuple([hash(pos), hash(food), tuple(ghost_pos)])

    def __max_value(self, state, ghost_index):
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
            return state.getScore()
        if state.isLose():
            return - math.inf

        # Initialize value
        value = - math.inf
  
        # Add the current node to the visited set
        self.visited.add(self.__get_info(state))

        successors = state.generatePacmanSuccessors()
        for succ in successors:
            # Check if it was already visited
            if self.__get_info(succ[0]) in self.visited:
                continue
            value = max(value, self.__min_value(succ[0], ghost_index))

        # Case in which all successors were visited
        if value == - math.inf:
            value = math.inf

        return value

    def __min_value(self, state, ghost_index):
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
            return state.getScore()
        if state.isLose():
            return - math.inf

        # Initialize value
        value = math.inf

        # Add the current node to the visited set
        self.visited.add(self.__get_info(state))

        successors = state.generateGhostSuccessors(ghost_index)
        for succ in successors:
            if ghost_index > 1:
                value = min(value, self.__min_value(succ[0], ghost_index-1))
            else:
                value = min(value, self.__max_value(succ[0], self.nb_ghosts))

        # Case in which all successors were visited
        if value == math.inf:
            value = - math.inf

        return value

    def get_action(self, state):
        """
        Given a pacman game state, returns a legal move according to the
        Minimax algorithm.
        Arguments:
        ----------
        - `state`: the current game state. 

        Return:
        -------
        - The best legal move as defined in `game.Directions`, according to
        the Minimax algorithm.
        """
        self.visited = set()
        best_value = - math.inf
        best_action = Directions.WEST

        # Get the number of ghosts in the layout
        self.nb_ghosts = state.getNumAgents() - 1

        # Add the current node to the visited set
        self.visited.add(self.__get_info(state))

        # For each successor of the current node  
        successors = state.generatePacmanSuccessors()
        for next_state, next_action in successors:
            value = self.__min_value(next_state, self.nb_ghosts)
            if value > best_value:
                best_value = value
                best_action = next_action

        return best_action
