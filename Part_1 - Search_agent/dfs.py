from pacman_module.game import Agent
from pacman_module.pacman import Directions
from pacman_module.util import Stack


class PacmanAgent(Agent):
    """
    This PacmanAgent class solves the Pacman game using the Depth
    First Search algorithm 
    """

    def __init__(self, args):
        """
        Arguments:
        ----------
        - `args`: Namespace of arguments from command-line prompt.
        """
        self.args = args
        self.nextactions = list()  # List to contain the final list of actions

    def construct_path(self, state, meta):
        """
        Given a pacman state and a dictionnary, produces a backtrace of
        the actions taken to find the food dot, using the recorded
        meta dictionary.
        Arguments:
        ----------
        - `state`: the current game state.
        - `meta`: a dictionnary containing the path information
            from one node to another.
        Return:
        -------
        - A list of legal moves as defined in `game.Directions`
        """
        action_list = list()

        # Continue until you reach root meta data (i.e. (None, None))
        while meta[state][0] is not None:
            state, action = meta[state]
            action_list.append(action)

        return action_list

    def compute_tree(self, state):
        """
        Given a pacman state, computes a path from that state to a state
        where pacman has eaten all the food dots.
        Arguments:
        ----------
        - `state`: the current game state.
        Return:
        -------
        - A list of legal moves as defined in `game.Directions`
        """
        fringe = Stack()  # a stack
        visited = set()  # an empty set to maintain visited nodes

        # a dictionary to maintain path information :
        # key -> (parent state, action to reach child)
        meta = dict()
        meta[state] = (None, None)

        # Append root
        fringe.push(state)

        # While not empty
        while not fringe.isEmpty():
            # Pick one available state
            current_node = fringe.pop()

            # If all food dots found, stop and compute a path
            if current_node.isWin():
                return self.construct_path(current_node, meta)

            # Get info on current node
            curr_pos = current_node.getPacmanPosition()
            curr_food = current_node.getFood()

            if (hash(curr_pos), hash(curr_food)) not in visited:
                # Add the current node to the visited set
                visited.add((hash(curr_pos), hash(curr_food)))

                # For each successor of the current node
                successors = current_node.generatePacmanSuccessors()
                for next_node, next_action in successors:
                    # Get info on successor
                    next_pos = next_node.getPacmanPosition()
                    next_food = next_node.getFood()

                    # Check if it was already visited
                    if (hash(next_pos), hash(next_food)) not in visited:
                        # If not, update meta and put the successor on the fringe
                        meta[next_node] = (current_node, next_action)
                        fringe.push(next_node)

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
            self.nextactions = self.compute_tree(state)

        return self.nextactions.pop()
