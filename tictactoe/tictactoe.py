"""
Tic Tac Toe Player
"""

import math
import copy
import random

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
    if sum([row.count(None) for row in board])%2 == 0:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()

    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))

    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    tmpBoard = copy.deepcopy(board)
    try:
        if tmpBoard[action[0]][action[1]] != EMPTY:
            raise IndexError
        else:
            tmpBoard[action[0]][action[1]] = player(tmpBoard)
            return tmpBoard
    except IndexError:
        print('Spot occupied')


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    
    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != EMPTY:
        return board[0][2]

    for row in board:
        xcount = row.count(X)
        ocount = row.count(O)
        if xcount == 3:
            return X
        if ocount == 3:
            return O

    columns = []

    for i in range(len(board)):
        column = [row[i] for row in board]
        columns.append(column)

    for i in columns:
        x_count = i.count(X)
        o_count = i.count(O)
        if x_count == 3:
            return X
        if o_count == 3:
            return O

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None: return True
    return len(actions(board)) == 0


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X: return 1
    if winner(board) == O: return -1
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board) == None:
        return None

    bestMoves = []
    alpha = -math.inf
    beta = math.inf

    if player(board) == X:
        v = -math.inf
        for action in actions(board):
            move = min_value(result(board, action), alpha, beta)
            if move > v:
                v = move
                bestMoves = [action]
            elif move == v:
                bestMoves.append(action)

    else:
        v = math.inf
        for action in actions(board):
            move = max_value(result(board, action), alpha, beta)
            if move < v:
                v = move
                bestMoves = [action]
            elif move == v:
                bestMoves.append(action)

    return random.choice(bestMoves)

def max_value(board, alpha, beta):
    """
    Returns the maximum value for the current player on the board.
    """
    v = -math.inf
    if terminal(board):
        return utility(board)

    for action in actions(board):
        v = max(v, min_value(result(board, action), alpha, beta))
        alpha = max(alpha, v)
        if beta <= alpha:  
            break 
    return v

def min_value(board, alpha, beta):
    """
    Returns the minimum value for the current player on the board.
    """
    v = math.inf
    if terminal(board):
        return utility(board)
    
    for action in actions(board):
        v = min(v, max_value(result(board, action), alpha, beta))
        beta = min(beta, v)
        if beta <= alpha:
            break
    return v
