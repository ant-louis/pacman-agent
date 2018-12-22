from pacman_module.game import Agent
from pacman_module.pacman import Directions, GhostRules
import numpy as np
from pacman_module import util
import copy


class BeliefStateAgent(Agent):
    def __init__(self, args):
        """
        Arguments:
        ----------
        - `args`: Namespace of arguments from command-line prompt.
        """
        self.args = args
        """
            Variables to use in 'updateAndFetBeliefStates' method.
            Initialization occurs in 'get_action' method.
        """
        # Current list of belief states over ghost positions
        self.beliefGhostStates = None
        # Grid of walls (assigned with 'state.getWalls()' method)
        self.walls = None
        # Uniform distribution size parameter 'w'
        # for sensor noise (see instructions)
        self.w = self.args.w
        # Probability for 'leftturn' ghost to take 'EAST' action
        # when 'EAST' is legal (see instructions)
        self.p = self.args.p
        # Initialization variable
        self._initialized = False

    def updateAndGetBeliefStates(self, evidences):
        """
        Given a list of (noised) distances from pacman to ghosts,
        returns a list of belief states about ghosts positions

        Arguments:
        ----------
        - `evidences`: list of (noised) ghost positions at state x_{t}
          where 't' is the current time step

        Return:
        -------
        - A list of Z belief states at state x_{t} about ghost positions
          as N*M numpy matrices of probabilities
          where N and M are respectively width and height
          of the maze layout and Z is the number of ghosts.

        N.B. : [0,0] is the bottom left corner of the maze
        """
        beliefStates = self.beliefGhostStates.copy()

        # If first call, compute T and B
        if not self._initialized:
            self._init_all()

        # Compute the belief ghost states
        for i, evidence in enumerate(evidences):
            # Reshape beliefStates to a 1D vector
            f = beliefStates[i].reshape(-1, 1, order='F')

            # Compute observation matrix
            index = self._get_cell(evidence[0], evidence[1])
            O = np.diag(self._B[:, index])

            # Compute the product and normalize it
            f = np.matmul(self._T.transpose(), f)
            f = np.matmul(O, f)
            f = f/sum(f)

            # Transform beliefStates to a matrix
            beliefStates[i] = f.reshape(self._width, self._height, order='F')

        self.beliefGhostStates = beliefStates
        return beliefStates

    def _computeNoisyPositions(self, state):
        """
            Compute a noisy position from true ghosts positions.
            XXX: DO NOT MODIFY THAT FUNCTION !!!
            Doing so will result in a 0 grade.
        """
        positions = state.getGhostPositions()
        w = self.args.w
        w2 = 2*w+1
        div = float(w2 * w2)
        new_positions = []
        for p in positions:
            (x, y) = p
            dist = util.Counter()
            for i in range(x - w, x + w + 1):
                for j in range(y - w, y + w + 1):
                    dist[(i, j)] = 1.0 / div
            dist.normalize()
            new_positions.append(util.chooseFromDistribution(dist))
        return new_positions

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

        """
           XXX: DO NOT MODIFY THAT FUNCTION !!!
                Doing so will result in a 0 grade.
        """

        # XXX : You shouldn't care on what is going on below.
        # Variables are specified in constructor.
        if self.beliefGhostStates is None:
            self.beliefGhostStates = state.getGhostBeliefStates()
        if self.walls is None:
            self.walls = state.getWalls()
        return self.updateAndGetBeliefStates(
            self._computeNoisyPositions(state))

    def _init_all(self):
        """
        Initialize the width, the height, the transition
        matrix and the sensor matrix.
        """
        self._width = self.walls.width
        self._height = self.walls.height
        self._size = self._height * self._width
        self._T = self._compute_transition_matrix()
        self._B = self._compute_sensor_matrix()
        self._initialized = True

    def _compute_transition_matrix(self):
        """
        Compute the transition matrix T such that
        T(i,j) = P(x_{t} = j | x_{t+1} = i).

        Return:
        -------
        - The transition matrix T as a (N*M)*(N*M) numpy matrix
        where N and M are respectively width and height
        of the maze layout.
        """
        size = self._size
        T = np.zeros((size, size))

        for cell in range(size):
            # Get the coordinates of the cell
            x, y = self._get_coord(cell)

            # If it's a wall, continue
            if self.walls[x][y]:
                continue

            # Get the legal actions in that cell
            actions = self._get_legal_actions(x, y)
            nb_actions = len(actions)

            # If going east is not legal
            if Directions.EAST not in actions:
                # Probabilities are uniformly distributed
                for action in actions:
                    next_cell = self._get_next_cell(cell, action)
                    T[cell][next_cell] = 1/nb_actions
            # If going east is legal, bigger probability for east action
            else:
                next_cell = self._get_next_cell(cell, Directions.EAST)
                T[cell][next_cell] = self.p + (1-self.p)/nb_actions
                actions.remove(Directions.EAST)
                for action in actions:
                    next_cell = self._get_next_cell(cell, action)
                    T[cell][next_cell] = 1/nb_actions
        return T

    def _compute_sensor_matrix(self):
        """
        Compute the sensor matrix B such that
        B(i,j) = P(e_{t} = j | x_{t} = i).

        Return:
        -------
        - The sensor matrix B as a (N*M)*(N*M) numpy matrix
        where N and M are respectively width and height
        of the maze layout.
        """
        size = self._size
        B = np.zeros((size, size))

        w = self.w
        W = 2*w + 1
        prob = 1/W**2

        for cell in range(size):
            # Get the coordinates of the cell
            x, y = self._get_coord(cell)

            # For each cell in a square of side W around (x,y)
            for i in range(x-w, x+w+1):
                for j in range(y-w, y+w+1):
                    # If the cell is in the grid
                    if self._in_grid(i, j):
                        # Attribute it the uniform probability
                        evidence = self._get_cell(i, j)
                        B[cell][evidence] = prob
        return B

    def _in_grid(self, x, y):
        """
        Given a coordinate (x,y), returns a boolean indicating
        if that coordinate is in the the maze layout.

        Arguments:
        ----------
        - `x`: coordinate on the X axis
        - `y`: coordinate on the Y axis

        Return:
        -------
        - True is the coordinate (x,y) is in the maze layout,
        False otherwise.
        """
        N = self._width
        M = self._height
        if x < 0 or x >= N or y < 0 or y >= M:
            return False
        return True

    def _get_cell(self, x, y):
        """
        Given a coordinate (x,y) of a N*M matrix where N and M are
        respectively width and height of the maze layout, returns
        the corresponding cell index in a 1D N*M array.

        Arguments:
        ----------
        - `x`: coordinate on the X axis between [0, N]
        - `y`: coordinate on the Y axis between [0, M]

        Return:
        -------
        - An index i such that 0 <= i <= N*M
        """
        return y * self._width + x

    def _get_coord(self, cell):
        """
        Given a cell index of a 1D N*M array, where N and M are
        respectively width and height of the maze layout, returns
        the corresponding coordinate (x,y) in a  N*M matrix.

        Arguments:
        ----------
        - `cell`: index between [0, N*M]

        Return:
        -------
        - A coordinate (x,y) such that 0 <= x <= N and 0 <= y <= M.
        """
        N = self._width
        x = cell % N
        y = (cell-x)//N
        return (x, y)

    def _get_legal_actions(self, x, y):
        """
        Given a coordinate (x,y) in a N*M matrix where N and M are
        respectively width and height of the maze layout, returns
        a list of the legal actions in that coordinate.

        Arguments:
        ----------
        - `x`: coordinate on the X axis
        - `y`: coordinate on the Y axis

        Return:
        -------
        - A list of the legal actions as defined in `game.Directions`.
        """
        actions = []

        # Check east
        if self._in_grid(x+1, y) and not self.walls[x+1][y]:
            actions.append(Directions.EAST)
        # Check west
        if self._in_grid(x-1, y) and not self.walls[x-1][y]:
            actions.append(Directions.WEST)
        # Check north
        if self._in_grid(x, y+1) and not self.walls[x][y+1]:
            actions.append(Directions.NORTH)
        # Check south
        if self._in_grid(x, y-1) and not self.walls[x][y-1]:
            actions.append(Directions.SOUTH)

        return actions

    def _get_next_cell(self, cell, action):
        """
        Given a cell index in a 1D N*M array where N and M are
        respectively width and height of the maze layout, returns
        the next cell index corresponding to a given action.

        Arguments:
        ----------
        - `cell`: index between [0, N*M]
        - `action`: an action as defined in `game.Directions`

        Return:
        -------
        - An index between [0, N*M] after executing the action.
        """
        # Get cell coordinates
        x, y = self._get_coord(cell)

        # Update it depending on the action
        if action == Directions.EAST:
            x += 1
        elif action == Directions.WEST:
            x -= 1
        elif action == Directions.NORTH:
            y += 1
        elif action == Directions.SOUTH:
            y -= 1

        # Return the cell index of new coordinates
        return self._get_cell(x, y)
