"""
An AI player for Othello. 
"""

import random
import sys
import time

# You can use the functions in othello_shared to write your AI
from othello_shared import find_lines, get_possible_moves, get_score, play_move

cache = {}

def eprint(*args, **kwargs): #you can use this for debugging, as it will print to sterr and not stdout
    print(*args, file=sys.stderr, **kwargs)

    
# Method to compute utility value of terminal state
def compute_utility(board, color):
    #color 0-empty
    #color 1-black
    #color 2-white
    black_score, white_score = get_score(board)
    if color == 1:
        utility = black_score - white_score
    elif color == 2:
        utility = white_score - black_score
    return utility

# Better heuristic value of board
def compute_heuristic(board, color): 
    '''
    #idea:
    1.general position - mobility_score
    -Use get possible move function to find number of possible moves
    2.corner position - corner_score
    -some corner position are hard to flip so it should have higher score
    -some corner position are easy to flip so it should have lower/negative score
    3.edge position - edge_score
    -edge position usually are hard to flip so it should have higher score
    '''
    
    score = 0
    d = len(board)-1
    
    #mobility score
    mobility_score = len(get_possible_moves(board, color))
    
    #check for edge which are not the corner, they are rlatively difficult to reverse
    edge_score = 0
    for i in range(2, d - 1):
        if board[i][0] == color or board[i][d] == color or board[0][i] == color or board[d][i] == color: 
            edge_score += 1
    
    #check for corner
    corner_score = 0
    if board[0][d] == color or board[0][0] == color or board[d][0] == color or board[d][d] == color:
        corner_score += 10
    if (board[1][0] == color or board[0][1] == color or board[d-1][0] == color or board[d][1] == color or board[0][d-1] == color or board[1][d] == color or board[d-1][d] == color or board[d][d-1] == color):
        corner_score -= 2
    if board[1][1] == color or board[d-1][1] == color or board[1][d-1] == color or board[d-1][d-1] == color:
        corner_score -= 5
    
    score = compute_utility(board, color) + edge_score + corner_score + mobility_score
    return score
   

############ MINIMAX ###############################
def minimax_min_node(board, color, limit, caching = 0):
    if caching == 1 and (board, color) in cache:
        return cache[(board, color)]
    
    if limit == 0:
        return (None, compute_utility(board, color))
    
    possible_moves = get_possible_moves(board, 3 - color)
    if possible_moves == []:
        score = compute_utility(board, color)
        if caching==1:
            cache[(board, color)] = (None, score)
        return (None, score)
    
    
    best_move = None
    best_score = float('inf')
    
    for move in possible_moves:
        new_board = play_move(board, 3-color, move[0],move[1])
        new_move, new_score = minimax_max_node(new_board, color, limit-1, caching)
        if new_score < best_score:
            best_score = new_score
            best_move = move
    
    if caching == 1:
        cache[(board, color)] = best_move, best_score     
    return (best_move, best_score)

def minimax_max_node(board, color, limit, caching = 0): #returns highest possible utility
    if caching == 1 and (board, color) in cache:
        return cache[(board, color)]
    
    if limit == 0:
       return (None, compute_utility(board, color))
    
    possible_moves = get_possible_moves(board,  color)
    if possible_moves == []:
        score = compute_utility(board, color)
        if caching==1:
            cache[(board, color)] = (None, score)
        return (None, score)
    
    best_move = None
    best_score = float('-inf')
    
    for move in possible_moves:
        new_board = play_move(board, color, move[0],move[1])
        new_move, new_score = minimax_min_node(new_board, color, limit-1, caching)
        if new_score > best_score:
            best_score = new_score
            best_move = move
    
    if caching == 1:
        cache[(board, color)] = best_move, best_score     
    return (best_move, best_score)

def select_move_minimax(board, color, limit, caching = 0):
    """
    Given a board and a player color, decide on a move. 
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.  

    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic 
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.    
    """
    return minimax_max_node(board, color, limit, caching)[0]
    
############ ALPHA-BETA PRUNING #####################
def alphabeta_min_node(board, color, alpha, beta, limit, caching=0, ordering=0):
    
    best_score = float('inf')
    best_move = None
    new_moves = []
    
    if caching == 1 and (board, color) in cache:
        return cache[(board, color)]
    
    if limit == 0:
        return (None, compute_utility(board, color))
    
    possible_moves = get_possible_moves(board, 3 - color)
    if possible_moves == []:
        score = compute_utility(board, color)
        if caching==1:
            cache[(board, color)] = (None, score)
        return (None, score)
    
    for move in possible_moves:
        new_board = play_move(board, 3 - color, move[0], move[1])
        new_moves.append(( compute_utility(new_board, color),move, new_board))
    if ordering:
        new_moves.sort(key=lambda x: x[0], reverse=True)

    for n in new_moves:
        n_board = n[2]
        new_move, new_score = alphabeta_max_node(n_board, color, alpha, beta, limit-1, caching, ordering)
        
        if new_score < best_score:
            best_score = new_score
            best_move = n[1]
        
        beta = min(best_score, beta)
        if beta <= alpha:
            break

    if caching:
        cache[(board, color)] = (best_move, best_score)

    return (best_move, best_score)


def alphabeta_max_node(board, color, alpha, beta, limit, caching=0, ordering=0):
    
    best_score = float('-inf')
    best_move = None
    new_moves = []
    
    if caching == 1 and (board, color) in cache:
        return cache[(board, color)]
    
    if limit == 0:
        return (None, compute_utility(board, color))
    
    possible_moves = get_possible_moves(board,color)
    if possible_moves == []:
        score = compute_utility(board, color)
        if caching==1:
            cache[(board, color)] = (None, score)
        return (None, score)
        
    for move in possible_moves:
        new_board = play_move(board, color, move[0], move[1])
        new_moves.append(( compute_utility(new_board, color),move, new_board))
    if ordering:
        new_moves.sort(key=lambda x: x[0], reverse=True)

    for n in new_moves:
        n_board = n[2]
        new_move, new_score = alphabeta_min_node(n_board, color, alpha, beta, limit-1, caching, ordering)
        
        if new_score > best_score:
            best_score = new_score
            best_move = n[1]
        
        alpha = max(best_score, alpha)
        if beta <= alpha:
            break
    if caching:
        cache[(board, color)] = (best_move, best_score)

    return (best_move, best_score)
    

def select_move_alphabeta(board, color, limit, caching = 0, ordering = 0):
    """
    Given a board and a player color, decide on a move. 
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.  

    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic 
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.    
    If ordering is ON (i.e. 1), use node ordering to expedite pruning and reduce the number of state evaluations. 
    If ordering is OFF (i.e. 0), do NOT use node ordering to expedite pruning and reduce the number of state evaluations. 
    """
    alpha = float('-inf')
    beta = float('inf')
    return alphabeta_max_node(board, color,alpha, beta, limit, caching, ordering )[0]

####################################################
def run_ai():
    """
    This function establishes communication with the game manager.
    It first introduces itself and receives its color.
    Then it repeatedly receives the current score and current board state
    until the game is over.
    """
    print("Othello AI") # First line is the name of this AI
    arguments = input().split(",")
    
    color = int(arguments[0]) #Player color: 1 for dark (goes first), 2 for light. 
    limit = int(arguments[1]) #Depth limit
    minimax = int(arguments[2]) #Minimax or alpha beta
    caching = int(arguments[3]) #Caching 
    ordering = int(arguments[4]) #Node-ordering (for alpha-beta only)

    if (minimax == 1): eprint("Running MINIMAX")
    else: eprint("Running ALPHA-BETA")

    if (caching == 1): eprint("State Caching is ON")
    else: eprint("State Caching is OFF")

    if (ordering == 1): eprint("Node Ordering is ON")
    else: eprint("Node Ordering is OFF")

    if (limit == -1): eprint("Depth Limit is OFF")
    else: eprint("Depth Limit is ", limit)

    if (minimax == 1 and ordering == 1): eprint("Node Ordering should have no impact on Minimax")

    while True: # This is the main loop
        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        # The first number is the score for player 1 (dark), the second for player 2 (light)
        next_input = input()
        status, dark_score_s, light_score_s = next_input.strip().split()
        dark_score = int(dark_score_s)
        light_score = int(light_score_s)

        if status == "FINAL": # Game is over.
            print
        else:
            board = eval(input()) # Read in the input and turn it into a Python
                                  # object. The format is a list of rows. The
                                  # squares in each row are represented by
                                  # 0 : empty square
                                  # 1 : dark disk (player 1)
                                  # 2 : light disk (player 2)

            # Select the move and send it to the manager
            if (minimax == 1): #run this if the minimax flag is given
                movei, movej = select_move_minimax(board, color, limit, caching)
            else: #else run alphabeta
                movei, movej = select_move_alphabeta(board, color, limit, caching, ordering)
            
            print("{} {}".format(movei, movej))

if __name__ == "__main__":
    run_ai()
