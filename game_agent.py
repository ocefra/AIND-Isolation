"""This file contains all the classes you must complete for this project.

You can use the test cases in agent_test.py to help during development, and
augment the test suite with your own test cases to further test your code.

You must test your agent's strength against a set of agents with known
relative strength using tournament.py and include the results in your report.
"""
import random
import operator


class Timeout(Exception):
    """Subclass base exception for code clarity."""
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    # Heuristic 1
    num_squares = game.width * game.height
    num_blanks = len(game.get_blank_spaces())

    center = (int(game.height / 2), int(game.width / 2))

    own_position = game.get_player_location(player)
    opp_position = game.get_player_location(game.get_opponent(player))

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

    score = float(own_moves - opp_moves)

    # If early game, try to stay in the middle.
    if num_blanks > 0.8 * num_squares:
        dist_to_center = tuple(abs(own_coord - center_coord) \
                               for own_coord, center_coord in zip(own_position, center))
        manhattan_dist_to_center = sum(dist_to_center)
        return score + 1 / manhattan_dist_to_center if manhattan_dist_to_center else score + 2

    # If mid game, try to stay close to the opponent.
    elif num_blanks > 0.1 * num_squares:
        dist_to_opp = tuple(abs(own_coord - opp_coord) \
                            for own_coord, opp_coord in zip(own_position, opp_position))
        manhattan_dist_to_opp = sum(dist_to_opp)
        return score + 1 / manhattan_dist_to_opp

    # If late game, simply try to maximise the player's open move advantage.
    else:
        return score


    # ***************************************************************************************************
    # # Heuristic 2: maximise the player's advantage while minimising the opponent's number of open moves.
    # own_moves = len(game.get_legal_moves(player))
    # opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    # return (own_moves - opp_moves) / opp_moves**2 if opp_moves else float("inf")
    # ***************************************************************************************************


    # ***************************************************************************************************
    # # Heuristic 3
    # opponent = game.get_opponent(player)
    #
    # own_moves = game.get_legal_moves(player) # player's legal moves
    # opp_moves = game.get_legal_moves(opponent) # opponent's legal moves
    # opp_all_moves = game.get_l_shaped_moves(opponent) # opponent's L-shaped-placed squares (free or not)
    # own_position = game.get_player_location(player) # player's location
    #
    # # What is the player's advantage in terms on number of open moves? We want to maximise it.
    # advantage = len(own_moves) - len(opp_moves)
    #
    # # Is the player blocking the opponent? If yes, add a bonus. For an equal number of extra moves,
    # # this favours a position where the player blocks the opponent.
    # blocking = 1 * (own_position in opp_all_moves)
    # # blocking = 2 * (own_position in opp_all_moves)
    #
    # # Can the opponent block the player on the next move? If yes, penalise this.
    # shared_moves = set(own_moves).intersection(set(opp_moves))
    # blockable = 1 * (len(shared_moves) != 0)
    #
    # # Try different versions.
    # # return float(10 * advantage + 4 * blocking - 2 * blockable)
    # # return float(advantage + 2 * blocking)
    # # return float(advantage - blockable)
    # # return float(advantage + blocking - blockable)
    # return float(advantage - blockable + 2 * blocking)
    # # return float((advantage - blockable + 2 * blocking)**2)
    # ***************************************************************************************************



    # ***************************************************************************************************
    # OTHER HEURISTICS

    # Heuristic 4
    # own_moves = len(game.get_legal_moves(player))
    # opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    # return (own_moves / (2 * opp_moves)) if opp_moves else float("inf")



    # # Heuristic 5: stay close to the opponent, while also looking for a position with as many open moves
    # # as possible: the score is an additive combination of the number of available moves and the closeness
    # # between the player and the opponent.
    # own_position = game.get_player_location(player)
    # opp_position = game.get_player_location(game.get_opponent(player))
    #
    # delta = tuple(abs(own_coord - opp_coord) for own_coord, opp_coord in zip(own_position, opp_position))
    # # dist = max(delta)
    # # score = 1 / dist
    # manhattan_dist = sum(delta)
    #
    # own_moves = len(game.get_legal_moves(player))
    # opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    # # score += float(own_moves - opp_moves)
    # score = float(own_moves - opp_moves) - manhattan_dist
    #
    # return score



    # # Heuristic 6: favour positions which share no moves with the opponent.
    # # This includes, but is not limited to, partitions.
    # own_moves = game.get_legal_moves(player)
    # opp_moves = game.get_legal_moves(game.get_opponent(player))
    # shared_moves = set(own_moves).intersection(opp_moves)
    # return float(len(own_moves) - len(opp_moves) - 2 * len(shared_moves))



    # # Heuristic 7: stay close to the centre.
    # own_moves = len(game.get_legal_moves(player))
    # opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    # score = float(own_moves - opp_moves)
    #
    # own_position = game.get_player_location(player)
    # center = (int(game.height / 2), int(game.width / 2))
    # dist_to_center = tuple(abs(own_coord - center_coord) \
    #                        for own_coord, center_coord in zip(own_position, center))
    # manhattan_dist_to_center = sum(dist_to_center)
    # score += score - manhattan_dist_to_center
    #
    # return score



    # # Heuristic 8
    # own_moves = len(game.get_legal_moves(player))
    # opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    # return (own_moves - opp_moves) / opp_moves if opp_moves else float("inf")
    # ***************************************************************************************************


    raise NotImplementedError


class CustomPlayer:
    """Game-playing agent that chooses a move using your evaluation function
    and a depth-limited minimax algorithm with alpha-beta pruning. You must
    finish and test this player to make sure it properly uses minimax and
    alpha-beta to return a good move before the search time limit expires.

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    iterative : boolean (optional)
        Flag indicating whether to perform fixed-depth search (False) or
        iterative deepening search (True).

    method : {'minimax', 'alphabeta'} (optional)
        The name of the search method to use in get_move().

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """

    def __init__(self, search_depth=3, score_fn=custom_score,
                 iterative=True, method='minimax', timeout=15.):
        self.search_depth = search_depth
        self.iterative = iterative
        self.score = score_fn
        self.method = method
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

    def get_move(self, game, legal_moves, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.
        This function must perform iterative deepening if self.iterative=True,
        and it must use the search method (minimax or alphabeta) corresponding
        to the self.method value.
        **********************************************************************
        NOTE: If time_left < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************
        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).
        legal_moves : list<(int, int)>
            A list containing legal moves. Moves are encoded as tuples of pairs
            of ints defining the next (row, col) for the agent to occupy.
        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.
        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """

        self.time_left = time_left

        # Perform any required initializations, including selecting an initial
        # move from the game board (i.e., an opening book), or returning
        # immediately if there are no legal moves
        if not legal_moves:
            return (-1, -1)

        # The best move is initially the one that scores best on the score function.
        score, best_move = max((self.score(game, self), move) for move in legal_moves)

        # Choosing a first move. This has no effect when running tournament.py, since starting positions
        # are random. It is however useful in real tournaments.
        # If this is the player's first move (either as player 1 or as player 2)
        if game.move_count <= 1:
            # pick the center square if it is free
            center = (int(game.height / 2), int(game.width / 2))
            if center in game.get_blank_spaces():
                return center
            # or the best available move if the center is taken.
            else:
                return best_move

        else:
            # Is the player the maximizing player, i.e. the active player in the current game?
            maximizing_player = game.active_player == game.__player_1__

        # try:
        #     # The search method call (alpha beta or minimax) should happen in
        #     # here in order to avoid timeout. The try/except block will
        #     # automatically catch the exception raised by the search method
        #     # when the timer gets close to expiring
        #     pass

            try:
                # If iterative, increment depth each time.
                if self.iterative:
                    depth = 1
                    while True:
                        if self.time_left() < self.TIMER_THRESHOLD:
                            raise Timeout()
                        # To avoid duplicating code (same code for minimax and alphabeta),
                        # create a string which includes the name of the method as variable,
                        # and evaluate it using `eval`.
                        _, best_move = eval('self.' + self.method + '(game, depth, maximizing_player)')
                        depth += 1
                # If not iterative, do a depth-limited search using either minimax or alphabeta.
                else:
                    _, best_move = eval('self.' + self.method + '(game, self.search_depth, maximizing_player)')
                    return best_move

            except Timeout:
                # Handle any actions required at timeout, if necessary
                # Return the best move found in the last search iteration performed.
                return best_move

        raise NotImplementedError

    def minimax(self, game, depth, maximizing_player=True):
        """Implement the minimax search algorithm as described in the lectures.
        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state
        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting
        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)
        Returns
        -------
        float
            The score for the current search branch
        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves
        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        no_legal_move = (-1, -1)
        legal_moves = game.get_legal_moves()

        if not depth or not legal_moves:
            return self.score(game, self), no_legal_move

        # The function to apply for choosing the best move depends on whether we are at a MAX or a MIN node.
        fn = max if maximizing_player else min

        # If depth is 1, return the best next move.
        if depth == 1:
            return fn((self.score(game.forecast_move(move), self), move) for move in legal_moves)
        # If depth is greater than 1, recurse.
        else:
            (best_score, move), best_move = fn((self.minimax(game.forecast_move(move),
                                                             depth - 1, maximizing_player), move) \
                                               for move in legal_moves)
            return best_score, best_move

        raise NotImplementedError

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
        """Implement minimax search with alpha-beta pruning as described in the
        lectures.
        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state
        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting
        alpha : float
            Alpha limits the lower bound of search on minimizing layers
        beta : float
            Beta limits the upper bound of search on maximizing layers
        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)
        Returns
        -------
        float
            The score for the current search branch
        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves
        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        no_legal_move = (-1, -1)
        legal_moves = game.get_legal_moves()

        if not depth or not legal_moves:
            return self.score(game, self), no_legal_move

        best_move = no_legal_move
        best_score = float("-inf") if maximizing_player else float("inf")

        # Variables for the parts of the computation which differ between MAX and MIN nodes.
        max_or_min = 'max' if maximizing_player else 'min'
        comparison_op = operator.gt if maximizing_player else operator.lt
        param = {'max': alpha, 'min': beta}
        fn = max if maximizing_player else min

        # Expand node.
        for legal_move in legal_moves:
            score, move = self.alphabeta(game.forecast_move(legal_move), depth - 1,
                                         param['max'], param['min'], not maximizing_player)
            if comparison_op(score, best_score):
                best_score, best_move = score, legal_move
            # Update param (alpha if MAX, beta if MIN).
            param[max_or_min] = fn(param[max_or_min], best_score)

            if param['min'] <= param['max']:
                break
        return best_score, best_move

        raise NotImplementedError
