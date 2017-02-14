"""This file contains all the classes you must complete for this project.

You can use the test cases in agent_test.py to help during development, and
augment the test suite with your own test cases to further test your code.

You must test your agent's strength against a set of agents with known
relative strength using tournament.py and include the results in your report.
"""
import random
import operator 
import math

# Board width and height
width = 7
height = 7

# Board position heuristics used by ID_AggStart_2 player
BP = [[0.5 if 1<i<width-2 and 1<j<height-2 
                     else 0 if 0<i<width-1 and 0<j<height-1 else -0.5
                     for i in range(width)] 
                     for j in range(height)]
BP[0][0] = BP[0][width-1] = BP[height-1][0] = BP[height-1][width-1] = -1
                     
class Timeout(Exception):
    """Subclass base exception for code clarity."""
    pass

def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    ----------
    float
        The heuristic value of the current game state to the specified player.
    """
    # Choose the ID_AggStart_2 by default
    return aggstart_2_score(game, player)
    
def aggstart_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    ----------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")
    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    open_spaces = len(game.get_blank_spaces())
    return float(own_moves - opp_moves*(3*open_spaces/49))
    
def modmid_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    ----------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")
        
    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    open_spaces = len(game.get_blank_spaces())
    return float(own_moves*(1-open_spaces/49) - opp_moves*(open_spaces/49))
    
def aggstart_2_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    ----------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")
    own_moves = len(game.get_legal_moves(player))
    own_pos = game.get_player_location(player)
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    opp_pos = game.get_player_location(game.get_opponent(player))
    open_spaces = len(game.get_blank_spaces())
    return float(own_moves - opp_moves*(open_spaces/49*3) + BP[own_pos[0]][own_pos[1]] - BP[opp_pos[0]][opp_pos[1]])
    
        
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
        depth of one (1) would only explore the immediate successors of the
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

    def __init__(self, search_depth=3, score_fn=aggstart_score,
                 iterative=True, method='alphabeta', timeout=5.):
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
        ----------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """

        self.time_left = time_left

        # Return if there are no legal moves left
        if not legal_moves:
            return (-1, -1)
 
        move = (-1,-1)

        if self.iterative:
            # Iterative deepening variable    
            iter_depth = 0
            while True:
                last_move = move
                iter_depth += 1
                try:
                    # Try to evaluate the minimax/alpha-beta algorithm before the timer expires
                    if self.method == 'minimax':
                        value, move = self.minimax(game, iter_depth)
                    elif self.method == 'alphabeta':
                        value, move = self.alphabeta(game, iter_depth)
                    else:
                        raise ValueError("Invalid method!")
                        
                    # Check if the end game was found
                    if value == float("inf"):
                        break
                    # If the game is inevitably lost, try to perform the last good movement found and pray! 
                    if value == -float("inf"):
                        move = last_move
                        break
                except Timeout:
                    # Timeout reached; end iterative deepening
                    break
        else:
            try:
                # Try to evaluate the minimax/alpha-beta algorithm before the timer expires
                if self.method == 'minimax':
                    value, move = self.minimax(game, self.search_depth)
                elif self.method == 'alphabeta':
                    value, move = self.alphabeta(game, self.search_depth)
                else:
                    raise ValueError("Invalid method!")

            except Timeout:
                print("TIMEOUT")
                # Timeout reached
                pass
        # Return the best move from the last completed search iteration
        return move
        
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
        
        actual_depth: int
            The current depth in the search tree
        
        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        ----------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()
        
        # Get all possible legal moves for the actual player
        legal_moves = game.get_legal_moves(game.active_player)
        
        # Stop if maximum depth was reached or there are no legal moves left
        if depth == 0 or not legal_moves:
            return self.score(game,self), (-1,-1)
        
        # Initiate the best move variable
        best_move = (-1,-1)
        
        # Set upper/lower bound for value
        if maximizing_player:
            # Lower bound
            value = float("-inf")
        else:
            # Upper bound
            value = float("inf")
        
        # Update the value and best move using the recursive minimax algorithm
        for move in legal_moves:
            # Alternate max and min layers using "maximizing_player"
            result, _ = self.minimax(game.forecast_move(move), depth-1,
                                     not maximizing_player)
            if maximizing_player:
                value, best_move = max((value, best_move), (result, move),
                                        key=operator.itemgetter(0))
            else:
                value, best_move = min((value, best_move), (result, move),
                                        key=operator.itemgetter(0))
        # If it foresees a defeat, try to choose a good move using minimax with depth 1.
        if value == float("-inf"):
            best_move = max([self.score(game.forecast_move(move),self),move] for move in legal_moves)[1]
        # Return the utility value of the current node and the next best move
        return value, best_move
        
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
        ----------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()
        
        # Get all possible legal moves for the active player
        legal_moves = game.get_legal_moves(game.active_player)
        
        # Stop if maximum depth was reached or there are no legal moves left
        if depth == 0 or not legal_moves:
            return self.score(game,self), (-1,-1)
        
        # Set upper/lower bound for value
        if maximizing_player:
            # Lower bound
            value = float("-inf")
        else:
            # Upper bound
            value = float("inf")
        
        # Initiate the best move variable
        best_move = (-1,-1)
        
        # Update the value and best move using the recursive alpha-beta algorithm
        for move in legal_moves:
            result, _ = self.alphabeta(game.forecast_move(move), depth-1, alpha, 
                                           beta, not maximizing_player)
            # Alternate max and min layers using "maximizing_player"
            if maximizing_player:
                value, best_move = max((value, best_move), (result, move), 
                                        key=operator.itemgetter(0))
                # Test if it can prune the next node
                if value >= beta:
                    return value, best_move
                # Update the alpha value
                alpha = max(alpha,value)
            else:
                value, best_move = min((value, best_move), (result, move), 
                                        key=operator.itemgetter(0))
                # Test if it can prune the next node
                if value <= alpha:
                    return value, best_move
                # Update the beta value
                beta = min(beta,value)
        # If it foresees a defeat, try to choose a good move using minimax with depth 1.
        if value == float("-inf"):
            _, best_move = max([self.score(game.forecast_move(move),self),move] for move in legal_moves)[1]
        # Return the utility value of the current node and the next best move
        return value, best_move
