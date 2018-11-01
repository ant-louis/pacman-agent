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

    def minimax_decision(self, state, nb_ghosts):
        """
        """
        action_values = list()

        pac_successors = state.generatePacmanSuccessors()
        for pac_successor in pac_successors:
            value = self.min_value(pac_successor, nb_ghosts)
            action_values.append(value)
        
        return max(action_values)
    
    def max_value(self, state, ghost_index):
        """
        """
        # Check the terminal test
        if state.isWin() or state.isLose():
            return state.getScore()  # Returns the utility value
        
        # Initialize value
        value = - math.inf

        pac_successors = state.generatePacmanSuccessors()
        for pac_successor in pac_successors:
            value = max(value, self.min_value(pac_successor, ghost_index))
        
        return value

    def min_value(self, state, ghost_index):
        """
        """
        # Check the terminal test
        if state.isWin() or state.isLose():
            return state.getScore()  # Returns the utility value
        
        # Initialize value
        value = math.inf

        ghost_successors = state.generateGhostSuccessors(ghost_index)
        for ghost_successor in ghost_successors:
            if ghost_index > 1:
                value = min(value, self.min_value(ghost_successor, ghost_index-1))
            else:
                value = min(value, self.max_value(ghost_successor, self.nb_ghosts))

        return value



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
        # Get the number of ghosts in the layout
        self.nb_ghosts = state.getNumAgents() - 1

        # Compute next move
        next_move = self.minimax_decision(state, self.nb_ghosts)

        return next_move
