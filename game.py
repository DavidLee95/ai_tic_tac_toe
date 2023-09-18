import pygame
import sys
import numpy as np
import functions as fn
import time

# Initialize pygame
pygame.init()

# Create constants
WIDTH = 700
HEIGHT = 700
BACKGROUND_COLOR = (51,153,255)
LINE_COLOR = (255,255,255)
O_COLOR = (255,255,51)
X_COLOR = (51,255,51)
BLACK = (0,0,0)

# Assign the screen size 
screen = pygame.display.set_mode((WIDTH,HEIGHT))

# Add title to the game
pygame.display.set_caption( "AI TIC TAC TOE")

# Initialize board by filling all the spaces as 0's
board = np.zeros((3,3))

# Initialize the figure that the user will play with
user_figure = None

# Function to draw the 4 board lines
def draw_board():
    pygame.draw.line(screen, LINE_COLOR, (110,270), (590,270), 10)
    pygame.draw.line(screen, LINE_COLOR, (270,110), (270,590), 10)
    pygame.draw.line(screen, LINE_COLOR, (110,430), (590,430), 10)
    pygame.draw.line(screen, LINE_COLOR, (430,110), (430,590), 10)

# Function to draw the figures in the board
def draw_figures(board):
    for i in range(3):
        for j in range(3):
            if board[i][j] == 100:
                pygame.draw.line( screen, X_COLOR, (i * 165 + 135, j * 165 + 135), (i * 165 + 235, j * 165 + 235), 15)
                pygame.draw.line( screen, X_COLOR, (i * 165 + 235, j * 165 + 135), (i * 165 + 135, j * 165 + 235), 15)
            if board[i][j] == 90:
                pygame.draw.circle( screen, O_COLOR, (i * 165 + 190,j * 170 + 180), 60, 15 )

# Function to draw the line to show the winner
def draw_winner_line(winner, first, second, third):

    # Assign the correct color
    if winner == 90:
        line_color = O_COLOR
    if winner == 100:
        line_color = X_COLOR
    
    # Draw the line only if there are winners
    if winner != None:
        # Check the rows
        if first == (0,0) and second == (1,0) and third == (2,0):
            pygame.draw.line(screen, line_color, (110,180), (590,180), 10)
        elif first == (0,1) and second == (1,1) and third == (2,1):
            pygame.draw.line(screen, line_color, (110,350), (590,350), 10)
        elif first == (0,2) and second == (1,2) and third == (2,2):
            pygame.draw.line(screen, line_color, (110,520), (590,520), 10)

        # Check the columns
        elif first == (0,0) and second == (0,1) and third == (0,2):
            pygame.draw.line(screen, line_color, (190,110), (190,590), 10)
        elif first == (1,0) and second == (1,1) and third == (1,2):
            pygame.draw.line(screen, line_color, (355,110), (355,590), 10)
        elif first == (2,0) and second == (2,1) and third == (2,2):
            pygame.draw.line(screen, line_color, (520,110), (520,590), 10)
        
        # Check diagonals
        elif first == (0,0) and second == (1,1) and third == (2,2):
            pygame.draw.line(screen, line_color, (110,110), (590,590), 10)
        elif first == (0,2) and second == (1,1) and third == (2,0):
            pygame.draw.line(screen, line_color, (590,110), (110,590), 10)

# Show text on the top
def show_upper_text(message):
    font = pygame.font.Font(None, 50)
    text = font.render(message, True, BLACK)
    text_rect = text.get_rect(center=(WIDTH/2, HEIGHT - 650))
    screen.blit(text, text_rect)

# Show text below the show_upper_text position
def show_upper_text2(message):
    font = pygame.font.Font(None, 30)
    text = font.render(message, True, BLACK)
    text_rect = text.get_rect(center=(WIDTH/2, HEIGHT - 615))
    screen.blit(text, text_rect)

# Show the available figures
def show_figure_options():
    font = pygame.font.Font(None, 50)
    text_x = font.render("Choose X", True, BLACK)
    text_o = font.render("Choose O", True, BLACK)
    background_x = pygame.Rect(WIDTH/4 -85, HEIGHT - 80, 175, 60)
    background_o = pygame.Rect(3*(WIDTH/4) - 85, HEIGHT - 80, 170, 60)
    text_x_rect = text_x.get_rect(center=(WIDTH/4, HEIGHT - 50))
    text_o_rect = text_o.get_rect(center=(3*(WIDTH/4), HEIGHT - 50))
    pygame.draw.rect(screen, (255,255,255), background_x)
    pygame.draw.rect(screen, (255,255,255), background_o)
    screen.blit(text_x, text_x_rect)
    screen.blit(text_o, text_o_rect)

# Show the option to play again
def play_again():
    font = pygame.font.Font(None, 50)
    text = font.render("Play again", True, BLACK)
    background = pygame.Rect(WIDTH/2 - 175/2, HEIGHT - 80, 175, 60)
    text_rect = text.get_rect(center=(WIDTH/2, HEIGHT - 50))
    pygame.draw.rect(screen, (255,255,255), background)
    screen.blit(text, text_rect)


# Main loop
while True:

    # Set the background color
    screen.fill(BACKGROUND_COLOR)

    # Draw the board lines
    draw_board()

    # Draw the figures in the board
    draw_figures(board)

    # Check the player's turn
    player_turn = fn.player(board)

    # Tell user to choose a figure
    if user_figure == None:
        # Ask the user to choose a turn
        show_upper_text("Choose X or O to start the game")
        show_upper_text2("(X will be the first one to play)")
        show_figure_options()

    # If the user has already chosen a turn
    else:
        # If the game has not ended
        if not fn.terminal(board):
            # Dipslay whose turn it is
            if user_figure == player_turn:
                show_upper_text("It is the user's turn to play")
            else:
                show_upper_text("It is the AI's turn to play")
        # If the game has ended
        else:
            # If nobody has won
            if fn.winner(board) == None:
                show_upper_text("The game is a tie")
            # If the user won
            elif fn.winner(board) == user_figure:
                show_upper_text("Congratulations, the user has won the game!")
            # If the AI won
            else:
                show_upper_text("Sorry, the AI has won the game!")

            # Draw the winner's line if the game is not a tie
            game_result = fn.winner_line(board)
            if game_result != None:
                draw_winner_line(game_result[0], game_result[1], game_result[2], game_result[3])

            # Give the option to play again
            play_again()

    # Game logic
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        # Assign the user a figure
        if user_figure == None:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Get coordinate values
                x_coord = event.pos[0]
                y_coord = event.pos[1]
                # Assign the user a figure
                user_figure = fn.assign_figure(x_coord, y_coord)
        
        # If the user has already chosen a figure
        else:
            # If the game has not ended
            if not fn.terminal(board):
                # If it is the player's turn
                if fn.player(board) == user_figure:
                    # Logic for the user's actions
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        # Get coordinate values
                        x_coord = event.pos[0]
                        y_coord = event.pos[1]
                        # Convert the coordinates to i and j
                        clicked = fn.coordinate_converter(x_coord, y_coord)

                        # Do nothing if the user clicked outside the board
                        if clicked[0] + clicked[1] > 49:
                            pass
                        elif board[clicked[0]][clicked[1]] == 0:
                            # Check who's turn it is
                            if fn.player(board) == 'X':
                                # "X" wil be represented by 100 in the board
                                board = fn.mark_board(100, clicked[0], clicked[1], board)
                            elif fn.player(board) == 'O':
                                # "O" will be represented by 90 in the board
                                board = fn.mark_board(90, clicked[0], clicked[1], board)

                # Logic for the AI's actions
                elif fn.player(board) != user_figure:
                    # Wait 1 second
                    time.sleep(1)
                    action = fn.minimax(board)
                    # Check who's turn it is
                    if fn.player(board) == 'X':
                        # "X" wil be represented by 100 in the board
                        board = fn.mark_board(100, action[0], action[1], board)
                    elif fn.player(board) == 'O':
                        # "O" will be represented by 90 in the board
                        board = fn.mark_board(90, action[0], action[1], board)

            # If the game has ended and the user wants to play again:
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Get coordinate values
                    x_coord = event.pos[0]
                    y_coord = event.pos[1]
                    if fn.play_again(x_coord, y_coord):
                        # Initialize board again
                        board = np.zeros((3,3))
                        # Do not assign the user a figure
                        user_figure = None

    pygame.display.update()