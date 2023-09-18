import math
import copy
import numpy as np

# Convert the game coordinates into board coordinates
def coordinate_converter(x_coord, y_coord):
    
    # Starting positions where the lines were drawn
    range = [110,270,430]

    # Assign a non-existent board value if the user clicks outside the board
    i_coord = 50
    j_coord = 50

    # Get the i coordinate from 0 to 2
    for i, value in enumerate(range):
        if value <= x_coord <= value + 159:
            i_coord = i
            
    # Get the j coordinate from 0 to 2
    for i, value in enumerate(range):
        if value <= y_coord <= value + 159:
            j_coord = i
    
    return i_coord,j_coord

# Mark the figure in the board
def mark_board(player, i, j, board):
    board[i][j] = player
    return board

# Detect and assign the user's figure (X or O)
def assign_figure(x_coord, y_coord):

    # Click on the X button
    if 90 <= x_coord <= 265 and 620 <= y_coord <= 680:
        return 'X'
    # Click on the O button 
    if 440 <= x_coord <= 610 and 620 <= y_coord <= 680:
        return 'O'
    else:
        return None

# Play again
def play_again(x_coord, y_coord):

    # Click on the X button
    if 262.5 <= x_coord <= 437.5 and 620 <= y_coord <= 680:
        return True
    else:
        return False

# Return the winner's positions if there is one
def winner_line(board):

    # Check the rows and colums for the winner, and return the winner and the positions if there is a winner
    for i in range(3):
        # Check rows
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] != 0:
            return (board[i][0],(i,0),(i,1),(i,2))
        # Check columns
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] != 0:
            return (board[0][i],(0,i),(1,i),(2,i))

    # Check diagonals for the winner, and return the winner and the positions if there is a winner
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != 0:
        return (board[0][0],(0,0),(1,1),(2,2))
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != 0:
        return (board[0][2],(0,2),(1,1),(2,0))

    # Return None in case there are no winners
    return None

# Check who the current player is
def player(board):

    # Count how many None's are in the board
    count = np.sum(board == 0)

    # If the number of 0's is odd, it is X's turn 
    if count % 2 == 1:
        turn = 'X'
    # If the number of 0's is even, it is O's turn
    else:
        turn = 'O'

    return turn

# Check all the actions that the AI can take
def actions(board):

    # Declare a variable to contain the set of all possible actions
    possible_actions = set()

    # Add all the spaces in the board that are empty as possible actions
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                possible_actions.add((i, j))
    #Return a None if there are no possible actions
    if len(possible_actions) == 0:
        possible_actions = None

    return possible_actions

# Check how the board would look like if a certain action on the current board is taken
def result(board, action):
    
    # Create a new board and update it according to the action
    new_board = copy.deepcopy(board)
    if player(board) == 'X':
        new_board[action[0]][action[1]] = 100
    else:
        new_board[action[0]][action[1]] = 90

    return new_board

# Check if there is a winner
def winner(board):

    # Check the rows and colums for the winner, and return the winner if there is one
    for i in range(3):
        # Check rows
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] != 0:
            return board[i][0]
        # Check columns
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] != 0:
            return board[0][i]

    # Check diagonals for the winner, and return the winner if there is one
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != 0:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != 0:
        return board[0][2]

    # Return None in case there are no winners
    return None

# Check if the game has ended
def terminal(board):

    # Count how many None's are in the board
    count = np.sum(board == 0)
    
    # If there is a winner or there are no more empty places, the game stops
    if winner(board) != None or count == 0:
        return True
    else: 
        return False

# Check who has won the game
def utility(board):

    # Check the winner and return it
    if winner(board) == 100:
        return 1
    elif winner(board) == 90:
        return -1
    else:
        return 0

# Minimax function for the AI
def minimax(board):
    
    # Return none if the game is over
    if terminal(board):
        return None
    
    # Initialize the set of all possible actions
    possible_actions = actions(board)
    # Array to store the values of each probable action
    final_values = []
    
    # For X, the goal will be to maximize the result
    if player(board) == 'X':
       for action in possible_actions:
           outcome = result(board,action)
           value = minvalue(outcome)
           final_values.append(value)
       # Search the possible action with the highest value
       reference = -1    
       index = 0
       for i, value in enumerate(final_values):
           if value > reference:
               reference = value
               index = i

    # For O, the goal will be to minimize the result
    else: 
       for action in possible_actions:
           outcome = result(board,action)
           value = maxvalue(outcome)
           final_values.append(value)
       # Search the possible action with the lowest value
       reference = 1    
       index = 0
       for i, value in enumerate(final_values):
           if value < reference:
               reference = value
               index = i
    
    # Convert the set to a list
    actions_list = list(possible_actions)

    # Return the action to be taken
    return actions_list[index]
    

# Max function for the minimax
def maxvalue(board):
    # Return the winner if the board is terminal
    if terminal(board):
        return utility(board)
    # Set initial value to the lowest possible
    v = -math.inf
    for action in actions(board):
        # Choose the highest value
        v = max(v, minvalue(result(board,action)))
    return v

# Min function for the minimax
def minvalue(board):
    # Return the winner if the board is terminal
    if terminal(board):
        return utility(board) 
    # Set initial value to the highest possible 
    v = math.inf
    for action in actions(board):
        # Choose the lowest value
        v = min(v, maxvalue(result(board,action)))
    return v