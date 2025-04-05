import random
import tkinter as tk
import pygame
import numpy as np  # this is to use 2D arrays
# initialise pygame
pygame.init()

### Generally methods go at the top and you call them at the bottom ###

# Set up the display

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



### ____ New Code etc etc ____ ###
        
light_blue = pygame.Color(173, 216, 253)
dark_blue = pygame.Color(0, 0, 173)
mid_blue = pygame.Color(0, 0, 205)
screen_width = 1500
screen_height = 1000
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Test Window")


# Square class stores information about the square like size
class Square:
    # using init and self.foo means that different instances of the same class can have different values
    def __init__(self, x, y, colour, square_size):
        self.x = x
        self.y = y
        self.colour = colour
        self.size = square_size
        

    # draws each small square
    def draw(self):
        pygame.draw.rect(screen, self.colour, [self.x, self.y , 50, 50], 10)
        pygame.display.update()
        return()

    # checks if given co ordinates are inside the square
    def is_clicked(self, x, y):
        return (self.x <= x <= (self.x + self.size) and self.y <= y <= (self.y + self.size))

    # changes colour of square
    def change_colour(self, new_colour):
        self.colour = new_colour
        return()



class Board:
    def __init__(self, rows, cols, square_colour, square_size):
        self.rows = rows
        self.cols = cols
        self.square_size = square_size
        self.square_colour = square_colour
        self.board = self.create()

##    def get_board(self):
##        return (self.board)

    # creates a 2D array of squares
    def create(self):
        board = np.empty((self.rows, self.cols), dtype=object)
        for i in range(self.rows):
            for j in range(self.cols):
                board[i, j] = Square(j * self.square_size, i * self.square_size, self.square_colour, self.square_size)
        return (board)  


    # draws entire board
    def draw(self):
        for row in range(self.board.shape[0]):
            for col in range(self.board.shape[1]):
                self.board[row, col].draw()
        return

    # gets row position of clicked square in array given coordinates
    def row_clicked(self, x, y):
        for row in range (self.board.shape[0]):
            for col in range (self.board.shape[1]):
                if self.board[row,col].is_clicked(x, y):
                    return(row)
        return None
    
    # gets col position of clicked square in array given coordinates
    def col_clicked(self, x, y):
        for row in range (self.board.shape[0]):
            for col in range (self.board.shape[1]):
                if self.board[row,col].is_clicked(x, y):
                    return(col)
        return None
        
    # changes colour of square given row and col in array
    def change_square_colour(self, row, col, new_colour):
        if row is not None and col is not None:
            self.board[row, col].change_colour(mid_blue)
            pygame.display.update()
        else:
            print ("foo")
        return


# ___ getting GUI to run ___ #

# Fill the screen with light blue
screen.fill(light_blue)
pygame.display.update()

board1 = Board(10, 10, dark_blue, 40)
board1.create()
board1.draw()


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:           
            mouse_x, mouse_y = pygame.mouse.get_pos()
            row = board1.row_clicked(mouse_x, mouse_y)
            col = board1.col_clicked(mouse_x, mouse_y)
            board1.change_square_colour(row, col, mid_blue)
            board1.draw()
                                                

pygame.quit()

#play_battleship()








