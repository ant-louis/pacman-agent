from pacman_module.game import Agent
from pacman_module.pacman import Directions
from pacman_module.util import manhattanDistance
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
        self.depth = 4

    def __cutoff_test(self, state, depth):
        """
        Arguments:
        ----------
        - `state`: the current game state.
        - `depth`: the biggest autorized depth before evaluation.

        Returns:
        ----------
        Returns true if the state is terminal or the maximal depth
        is reached.
        """
        return state.isWin() or state.isLose() or depth == 0

    def __eval_state(self, state):
        """Returns a custum utility value of the state.
        Arguments:
        ----------
        - `state`: the current game state.

        Returns:
        ----------
        The custom utility value at a given state.
        """
        current_score = state.getScore()
        pacman_pos = state.getPacmanPosition()
        ghost_list = state.getGhostPositions()
        food_list = state.getFood().asList()

        # If pacman wins the game
        if state.isWin() or state.isLose():
            return current_score

        # Get the distance from pacman to the closest food
        food_dist = [manhattanDistance(pacman_pos, food_pos) for food_pos in
                     food_list]
        closest_food = min(food_dist)
        # Get the distances from pacman to the closest ghost
        ghost_dist = [manhattanDistance(pacman_pos, ghost_pos) for ghost_pos in
                      ghost_list]
        closest_ghost = min(ghost_dist)
        # Get the number of foods left
        nb_foods_left = state.getNumFood()

        # Compute score
        score = (1 * current_score -
                 1.5 * (1./closest_ghost) -
                 1.5 * closest_food -
                 6 * nb_foods_left)

        return score

    def __max_value(self, state, alpha, beta, depth, ghost_index):
        """
        Arguments:
        ----------
        - `state`: the current game state.
        - `alpha`: the value of the best (i.e., highest-value) choice we have
        found so far at any choice point along the path for MAX.
        - `beta`: the value of the best (i.e., lowest-value) choice we have
        found so far at any choice point along the path for MIN.
        - `depth`: the biggest autorized depth before evaluation.
        - `ghost_index`: the index of the ghost agent.

        Returns:
        ----------
        The max utility value of the successor nodes.
        """
        # Check cutoff
        if self.__cutoff_test(state, depth):
            return self.__eval_state(state)

        # Initialize value
        value = - math.inf

        successors = state.generatePacmanSuccessors()
        for succ in successors:
            value = max(value, self.__min_value(succ[0], alpha, beta,
                                                depth-1, ghost_index))
            if value >= beta:
                return value
            alpha = max(alpha, value)

        return value

    def __min_value(self, state, alpha, beta, depth, ghost_index):
        """
        Arguments:
        ----------
        - `state`: the current game state.
        - `alpha`: the value of the best (i.e., highest-value) choice we have
        found so far at any choice point along the path for MAX.
        - `beta`: the value of the best (i.e., lowest-value) choice we have
        found so far at any choice point along the path for MIN.
        - `depth`: the biggest autorized depth before evaluation.
        - `ghost_index`: the index of the ghost agent.

        Returns:
        ----------
        The min utility value of the successor nodes.
        """
        # Check cutoff
        if self.__cutoff_test(state, depth):
            return self.__eval_state(state)

        # Initialize value
        value = math.inf

        successors = state.generateGhostSuccessors(ghost_index)
        for succ in successors:
            if ghost_index > 1:
                value = min(value, self.__min_value(succ[0], alpha, beta,
                                                    depth, ghost_index-1))
            else:
                value = min(value, self.__max_value(succ[0], alpha, beta,
                                                    depth-1, self.nb_ghosts))
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
        alpha = - math.inf
        beta = math.inf
        best_value = - math.inf
        best_action = Directions.WEST

        # Get the number of ghosts in the layout
        self.nb_ghosts = state.getNumAgents() - 1

        successors = state.generatePacmanSuccessors()
        for next_state, next_action in successors:
            value = self.__min_value(next_state, alpha, beta, self.depth,
                                     self.nb_ghosts)
            if value > best_value:
                best_value = value
                best_action = next_action
            alpha = max(alpha, best_value)

        return best_action
