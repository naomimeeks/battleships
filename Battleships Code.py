import random
import tkinter as tk
import pygame
import numpy as np  # this is to use 2D arrays
# initialise pygame
pygame.init()

### Generally methods go at the top and you call them at the bottom ###

# Set up the display
lightBlue = pygame.Color(173,216,253)
darkBlue = pygame.Color(0,0,173)
screenWidth = 1500
screenHeight = 1000
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Test Window")

def place_ship(board, ship_size):
    size = len(board)
    while True:
        orientation = random.choice(['horizontal', 'vertical'])
        if orientation == 'horizontal':
            row = random.randint(0, size - 1)
            col = random.randint(0, size - ship_size)
            if all(board[row][col+i] == 'O' for i in range(ship_size)):
                for i in range(ship_size):
                    board[row][col+i] = 'S'
                return
        else:
            row = random.randint(0, size - ship_size)
            col = random.randint(0, size - 1)
            if all(board[row+i][col] == 'O' for i in range(ship_size)):
                for i in range(ship_size):
                    board[row+i][col] = 'S'
                return

def play_battleship():
    size = 10
    num_ships = 3
    ship_sizes = [3, 4, 5]
    
    player_board = create_board(size)
    computer_board = create_board(size)
    computer_view = create_board(size)
    
    for ship_size in ship_sizes:
        place_ship(player_board, ship_size)
        place_ship(computer_board, ship_size)
    
    player_ships = sum(row.count('S') for row in player_board)
    computer_ships = sum(row.count('S') for row in computer_board)

    
    while player_ships > 0 and computer_ships > 0:
        print("Your board:")
        print_board(player_board)
        print("Your guesses:")
        print_board(computer_view)
        
        # Player's turn
        while True:
            try:
                row = int(input("Enter row (0-9): "))
                col = int(input("Enter column (0-9): "))
                if 0 <= row < size and 0 <= col < size and computer_view[row][col] == 'O':
                    break
                print("Invalid input. Try again.")
            except ValueError:
                print("Invalid input. Try again.")
        
        if computer_board[row][col] == 'S':
            print("Hit!")
            computer_view[row][col] = 'X'
            computer_board[row][col] = 'X'
            computer_ships -= 1
        else:
            print("Miss!")
            computer_view[row][col] = 'M'
        
        # Computer's turn
        while True:
            row, col = random.randint(0, size-1), random.randint(0, size-1)
            if player_board[row][col] != 'X' and player_board[row][col] != 'M':
                break
        
        print(f"\nComputer guesses: {row}, {col}")
        if player_board[row][col] == 'S':
            print("Computer hit your ship!")
            player_board[row][col] = 'X'
            player_ships -= 1
        else:
            print("Computer missed!")
            player_board[row][col] = 'M'
        
        print(f"\nYour ships remaining: {player_ships}")
        print(f"Computer ships remaining: {computer_ships}\n")
    
    if player_ships == 0:
        print("Game over! The computer won.")
    else:
        print("Congratulations! You won!")


cellSize = 40
rows, cols = 10, 10

# create board
def createBoard(rows, cols):
    return np.full((rows,cols), 0)
    
# draws each small square
def drawSquare(x,y):
    pygame.draw.rect(screen, darkBlue, [x, y , 50, 50], 10)
    pygame.display.update()
    return()

# draws entire board
def drawBoard(board):
    for row in range(board.shape[0]):
        for col in range(board.shape[1]):
            x = (col * cellSize) + 50
            y = (row *cellSize) + 50
            drawSquare(x,y)

# --- getting GUI to run --- 

# Fill the screen with light blue
screen.fill(lightBlue)
pygame.display.update()

board1 = createBoard(10,10)
drawBoard(board1)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            
            mouse_x, mouse_y = pygame.mouse.get_pos()
            col = mouse_x // cellSize
            row = mouse_y // cellSize
            if 0 <= row < rows and 0 <= col < cols:
                board1[row][col] = 1 - board1[row][col]

pygame.quit()

#play_battleship()








