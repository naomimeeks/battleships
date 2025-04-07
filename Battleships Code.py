import random
import tkinter as tk
import pygame
import numpy as np  # this is to use 2D arrays
pygame.init() # initialise pygame

### Generally methods go at the top and you call them at the bottom ###
### ____ New Code etc etc ____ ###
        
light_blue = pygame.Color(173, 216, 253)
dark_blue = pygame.Color(0, 0, 173)
red = pygame.Color(200, 0, 0)
pink = pygame.Color(255, 105, 180)
green = pygame.Color(0, 255, 0)
screen_width = 1500
screen_height = 1000
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Battleships")


# Square class stores information about the square like size
class Square:
    # using init and self.foo means that different instances of the same class can have different values
    def __init__(self, x, y, colour, square_size, x_indent, y_indent):
        self.x = x + x_indent
        self.y = y + y_indent
        self.colour = colour
        self.size = square_size
        self.is_ship = False
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        

    # draws each small square
    def draw(self):
        pygame.draw.rect(screen, self.colour, self.rect, 0)
        pygame.display.update()
        return()

    # checks if given co ordinates are inside the square
    def is_clicked(self, x, y):
        return self.rect.collidepoint(x, y)

    # changes colour of square
    def change_colour(self, new_colour):
        self.colour = new_colour
        return()

    # gets colour of square
    def get_colour(self):
        return(self.colour)

    # makes square a ship
    def make_ship(self):
        self.is_ship = True
        return()


class Board:
    def __init__(self, rows, cols, square_colour, square_size, x_indent, y_indent):
        self.rows = rows
        self.cols = cols
        self.square_size = square_size
        self.square_colour = square_colour
        self.x_indent = x_indent
        self.y_indent = y_indent
        self.board = self.create()

    # creates a 2D array of squares
    def create(self):
        board = np.empty((self.rows, self.cols), dtype=object)
        for i in range(self.rows):
            for j in range(self.cols):
                board[i, j] = Square(j * self.square_size, i * self.square_size, self.square_colour, self.square_size, self.x_indent, self.y_indent)
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
    
    # Checks if the clicked pixel are within the board's bounds
    def is_in_bounds(self, x, y):
        board_left = self.x_indent
        board_right = self.x_indent + self.cols * self.square_size
        board_top = self.y_indent
        board_bottom = self.y_indent + self.rows * self.square_size
        
        # Check if the (x, y) coordinate is within the board's rectangle
        return board_left <= x < board_right and board_top <= y < board_bottom
    
    # Gets a given place in a board's square colour
    def get_square_colour(self, row, col):
        return(self.board[row, col].get_colour())
        
    # changes colour of square given row and col in array
    def change_square_colour(self, row, col, new_colour):
        if row is not None and col is not None:
            self.board[row, col].change_colour(new_colour)
            pygame.display.update()
        else:
            print ("foo")
        return

    def place_ship(self, ship_size):
        size = self.board.shape[0]
        while True:
            orientation = random.choice(['horizontal', 'vertical'])
            if orientation == 'horizontal':
                row = random.randint(0, size - 1)
                col = random.randint(0, size - ship_size)
                if all(self.board[row][col+i].get_colour() == dark_blue for i in range(ship_size)):
                    for i in range(ship_size):
                        self.board[row][col+i].make_ship()
                        self.board[row][col+i].change_colour(pink)
                    return
            else:
                row = random.randint(0, size - ship_size)
                col = random.randint(0, size - 1)
                if all(self.board[row+i][col].get_colour() == dark_blue for i in range(ship_size)):
                    for i in range(ship_size):
                        self.board[row+i][col].make_ship()
                        self.board[row+i][col].change_colour(pink)
                    return
                
    def place_ships(self, num_ships):
        ship_sizes = [2, 3, 4, 5]        
        for ship_size in ship_sizes:
            self.place_ship(ship_size)

    def select_random_square(self):
        # Get the number of rows and columns in the board
        row = random.randint(0, self.rows - 1)
        col = random.randint(0, self.cols - 1)       
        selected_square = self.board[row, col]       
        return selected_square
            

###########################################################################################
# computer chooses a random square and it changes to a different colour on the board
def computers_turn(player_board):
    random_square = player_board.select_random_square()
    if(random_square.is_ship):
        random_square.change_colour(red)
    else:
        random_square.change_colour(green)
    pygame.display.update()

# ___ getting GUI to run ___ #

# Fill the screen with light blue
screen.fill(light_blue)
pygame.display.update()

# creating and initialising the computer's (guessing) board
computer_board = Board(10, 10, dark_blue, 50, 50, 50)
computer_board.create()
computer_board.place_ships(3)
computer_board.draw()

# creating and initialising the player's board
boats_board = Board(10, 10, dark_blue, 50, 600, 50)
boats_board.create()
boats_board.place_ships(3)
boats_board.draw()


# Means that clicking the X will close the window
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False            
        # if you click on a square, it changes colour to red
        # if you click on a ship, it changes the colour to green
        if event.type == pygame.MOUSEBUTTONDOWN:           
            mouse_x, mouse_y = pygame.mouse.get_pos()
            row = computer_board.row_clicked(mouse_x, mouse_y)
            col = computer_board.col_clicked(mouse_x, mouse_y)
            # checks if click is on the board
            if (computer_board.is_in_bounds(mouse_x, mouse_y)):
                if(computer_board.board[row, col].is_ship):
                    computer_board.change_square_colour(row, col, red)
                    computer_board.draw()
                else:
                    computer_board.change_square_colour(row, col, green)
                    computer_board.draw()
            # time for the computer to go
            computers_turn(boats_board)
            boats_board.draw()
                                                           
pygame.quit()








