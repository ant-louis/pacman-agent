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
        self.depth = 5
    
    def score_evaluation(self, state):
        """Returns the score of the state.
        Arguments:
        ----------
        - `state`: the current game state.

        Returns:
        ----------
        The score of the given state.
        """
        return state.getScore()

    def cutoff_test(self, state, depth):
        return state.isWin() or state.isLose() or depth == 0

    def eval_state(self, state):
        return self.score_evaluation(state)  # Returns the utility value


    def alphabeta_decision(self, state, depth, nb_ghosts):
        """Returns the best legal action according to the H-minimax algorithm.
        Arguments:
        ----------
        - `state`: the current game state.
        - `depth`: the largest authorized depth before evaluation.
        - `nb_ghosts`: the number of ghosts in the grid.

        Returns:
        ----------
        The best legal action for the defined maximal depth.
        """
        values = list()
        actions = list()
        alpha = - math.inf
        beta = math.inf

        pac_successors = state.generatePacmanSuccessors()
        for next_state, next_action in pac_successors:
            value = self.min_value(next_state, alpha, beta, depth, nb_ghosts)
            if value >= beta:
                return next_action

            alpha = max(alpha, value)
            values.append(value)
            actions.append(next_action)

        index = values.index(max(values))

        return actions[index]
    
    def max_value(self, state, alpha, beta, depth, ghost_index):
        """
        Arguments:
        ----------
        - `state`: the current game state.
        - `depth`: the biggest autorized depth before evaluation.
        - `ghost_index`: the index of the ghost agent.

        Returns:
        ----------
        The max utility value of the successor nodes.
        """
        if self.cutoff_test(state, depth):
            return self.eval_state(state)    
        
        # Initialize value
        value = - math.inf

        pac_successors = state.generatePacmanSuccessors()
        for pac_successor in pac_successors:
            value = max(value, self.min_value(pac_successor[0], alpha, beta, depth-1, ghost_index))
            if value >= beta:
                return value
            alpha = max(alpha, value)
        
        return value

    def min_value(self, state, alpha, beta, depth, ghost_index):
        """
        Arguments:
        ----------
        - `state`: the current game state.
        - `depth`: the biggest autorized depth before evaluation.
        - `ghost_index`: the index of the ghost agent.

        Returns:
        ----------
        The min utility value of the successor nodes.
        """

        if self.cutoff_test(state, depth):
            return self.eval_state(state)
        
        # Initialize value
        value = math.inf

        ghost_successors = state.generateGhostSuccessors(ghost_index)
        for ghost_successor in ghost_successors:
            if ghost_index > 1:
                value = min(value, self.min_value(ghost_successor[0], alpha, beta, depth, ghost_index-1))
            else:
                value = min(value, self.max_value(ghost_successor[0], alpha, beta, depth-1, self.nb_ghosts))

            if value <= alpha:
                return value
            beta = min(beta, value)

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
        next_move = self.alphabeta_decision(state, self.depth, self.nb_ghosts)
        return next_move
