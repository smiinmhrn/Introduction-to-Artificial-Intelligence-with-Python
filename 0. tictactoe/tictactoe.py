"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    if all(cell == EMPTY for row in board for cell in row):
        return X
    
    X_count = sum(row.count("X") for row in board)
    O_count = sum(row.count("O") for row in board)

    if X_count > O_count:
        return O
    else:
        return X
    
    raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actiones = set()
    
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == EMPTY:
                actiones.add((i, j))

    return actiones

    raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise ValueError("Invalid move: Action is not possible")
    
    i, j = action
    if player(board) == X:
        board[i][j] = X
    else:
        board[i][j] = O

    return copy_board(board)  # Return a new board, not the mutated one


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(len(board)):

        # check the row 
        if all(element == X for element in board[i]):
            return X
        elif all(element == O for element in board[i]):
            return O

        # check the column
        if all(element == X for element in [row[i] for row in board]):
            return X
        elif all(element == O for element in [row[i] for row in board]):
            return O
        
    # check the main Diameter
    if all(element == X for element in [board[i][i] for i in range(len(board))]):
        return X
    elif all(element == O for element in [board[i][i] for i in range(len(board))]):
        return O
        
    # check the anti Diameter
    if all(element == X for element in [board[i][len(board)-i-1] for i in range(len(board))]):
        return X
    elif all(element == O for element in [board[i][len(board)-i-1] for i in range(len(board))]):
        return O
    
    return None

    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if len(actions(board)) == 0 or winner(board) == X or winner(board) == O:
        return True
    else:
        return False
    
    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    result = winner(board)

    if result == X:
        return 1
    elif result == O:
        return -1
    else:
        return 0
    
    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    def max_value(board):
        if terminal(board):
            return utility(board), None
        score = -math.inf
        best_action = None
        for action in actions(board):
            value, _ = min_value(result(copy_board(board), action))
            if value > score:
                score = value
                best_action = action
        return score, best_action

    def min_value(board):
        if terminal(board):
            return utility(board), None
        score = math.inf
        best_action = None
        for action in actions(board):
            value, _ = max_value(result(copy_board(board), action))
            if value < score:
                score = value
                best_action = action
        return score, best_action

    current_player = player(board)
    if terminal(board):
        return None

    if current_player == X:
        _, best_action = max_value(board)
    else:
        _, best_action = min_value(board)

    return best_action


def copy_board(board):
    """
    Returns a copy of the board to avoid mutating the original board.
    """
    return [row.copy() for row in board]
