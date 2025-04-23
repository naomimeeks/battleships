import random
import time
import tkinter as tk
import pygame
import numpy as np  # this is to use 2D arrays
pygame.init() # initialise pygame

### Generally methods go at the top and you call them at the bottom ###
### ____ New Code etc etc ____ ###

# Colours        
light_blue = pygame.Color(173, 216, 253)
dark_blue = pygame.Color(0, 0, 173)
red = pygame.Color(200, 0, 0)
pink = pygame.Color(255, 105, 180)
green = pygame.Color(0, 255, 0)
light_grey = pygame.Color(200, 200, 200)
purple = pygame.Color(128, 0, 128)

# Variables
#background_image = pygame.image.load('background.png')
pygame.display.set_caption("Battleships")
rows = 9
cols = 9
square_size = 50
gap_size = 5
board_spacing = 100
margin = 50

# calculate board size
board_width = cols * (square_size + gap_size)
board_height = rows * (square_size + gap_size)

# calculate screen size
screen_width = margin * 2 + board_width * 2 + board_spacing
screen_height = margin * 2 + board_height + 50

# Fonts
font = pygame.font.SysFont("arial", 24)
big_font = pygame.font.SysFont("arial", 32)
bold_font = pygame.font.SysFont("arial", 28, bold=True)

screen = pygame.display.set_mode((screen_width, screen_height))

# Keeps track of which screen is currently active: "game" or "settings"
current_screen = "game"

# quit button class
class Button:
    def __init__(self, text, x, y, width, height, font, bg_color, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.bg_color = bg_color
        self.text_color = text_color
        self.text_surf = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def draw(self, surface):
        pygame.draw.rect(surface, self.bg_color, self.rect)
        surface.blit(self.text_surf, self.text_rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

# Square class stores information about the square like size
class Square:
    # using init and self.foo means that different instances of the same class can have different values
    def __init__(self, x, y, colour, square_size, x_indent, y_indent):
        # Now that coordinates are precomputed correctly, we just assign them
        self.x = x
        self.y = y
        self.colour = colour
        self.size = square_size
        self.is_ship = False
        self.been_clicked = False
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        

    # draws each small square
    def draw(self):
        pygame.draw.rect(screen, self.colour, self.rect, 0)
        return()

    # checks if given co ordinates are inside the square
    def is_clicked(self, x, y):
        return self.rect.collidepoint(x, y)

    # changes colour of square
    def change_colour(self, new_colour):
        self.colour = new_colour
        #self.been_clicked = True
        return()

    # gets colour of square
    def get_colour(self):
        return(self.colour)

    # makes square a ship
    def make_ship(self):
        self.is_ship = True
        return()


class Board:
    def __init__(self, rows, cols, square_colour, square_size, x_indent, y_indent, name):
        self.rows = rows
        self.cols = cols
        self.square_size = square_size
        self.square_colour = square_colour
        self.x_indent = x_indent
        self.y_indent = y_indent
        self.board = self.create()
        self.name = name

    # creates a 2D array of squares
    def create(self):
        board = np.empty((self.rows, self.cols), dtype=object)
        for row in range(self.rows):
            for col in range(self.cols):
                # Calculate the actual pixel positions using column and row
                # This ensures consistent spacing with the defined gap
                x = self.x_indent + col * (self.square_size + gap_size)
                y = self.y_indent + row * (self.square_size + gap_size)
                board[row, col] = Square(x, y, self.square_colour, self.square_size, 0, 0)
        return (board)  


    # draws entire board
    def draw(self):
        # draws column labels
        for col in range(self.cols):
            label = chr(ord('A') + col)
            x = self.x_indent + col * (self.square_size + 5) + self.square_size // 2
            y = self.y_indent - 25
            draw_text(label, x, y, color='black', center=True)

        # draws row labels
        for row in range(self.rows):
            label = str(row + 1)
            x = self.x_indent - 25
            y = self.y_indent + row * (self.square_size + 5) + self.square_size // 2
            draw_text(label, x, y, color='black', center=True)

        # draws squares
        for row in range(self.board.shape[0]):
            for col in range(self.board.shape[1]):
                self.board[row, col].draw()
        return

    # gets the coordinates for a clicked square
    def get_clicked_position(self, x, y):
        for row in range(self.board.shape[0]):
            for col in range(self.board.shape[1]):
                if self.board[row, col].is_clicked(x, y):
                    return row, col
        return None, None
    
    # Checks if the clicked pixel are within the board's bounds
    def is_in_bounds(self, x, y):
        board_left = self.x_indent
        board_right = self.x_indent + self.cols * (self.square_size + 5)
        board_top = self.y_indent
        board_bottom = self.y_indent + self.rows * (self.square_size + 5)
        
        # Check if the (x, y) coordinate is within the board's rectangle
        return board_left <= x < board_right and board_top <= y < board_bottom
    
    # Gets a given place in a board's square colour
    def get_square_colour(self, row, col):
        return(self.board[row, col].get_colour())
        
    # changes colour of square given row and col in array
    def change_square_colour(self, row, col, new_colour):
        if row is not None and col is not None:
            self.board[row, col].change_colour(new_colour)
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
                    return
            else:
                row = random.randint(0, size - ship_size)
                col = random.randint(0, size - 1)
                if all(self.board[row+i][col].get_colour() == dark_blue for i in range(ship_size)):
                    for i in range(ship_size):
                        self.board[row+i][col].make_ship()
                    return
                
    def place_ships(self, num_ships):
        ship_sizes = [2, 3, 4, 5]        
        for ship_size in ship_sizes:
            self.place_ship(ship_size)

    def draw_ships(self):
        for row in range(self.board.shape[0]):
            for col in range(self.board.shape[1]):
                if(self.board[row,col].is_ship):
                    self.board[row][col].change_colour(pink)
        return

    def select_random_square(self):
        # Get the number of rows and columns in the board
        row = random.randint(0, self.rows - 1)
        col = random.randint(0, self.cols - 1)       
        selected_square = self.board[row, col]       
        return selected_square

class Player:
    def __init__(self, rows, cols, square_colour, square_size, x_indent, y_indent, name, num_ships):
        self.rows = rows
        self.cols = cols
        self.square_colour = square_colour
        self.square_size = square_size
        self.x_indent = x_indent
        self.y_indent = y_indent
        self.name = name
        self.num_ships = num_ships
        self.board = Board(rows,cols, square_colour, square_size, x_indent, y_indent,name)
        self.board.create()
        self.board.place_ships(num_ships)
        self.board.draw()

###########################################################################################
# computer chooses a random square and it changes to a different colour on the board
def computers_turn(player_board):
    random_square = player_board.select_random_square()
    while (random_square.been_clicked):
        random_square = player_board.select_random_square()
    if(random_square.is_ship):
        random_square.change_colour(red)
        random_square.been_clicked = True
    else:
        random_square.change_colour(green)
        random_square.been_clicked = True
    pygame.display.update()


def draw_text(text, x, y, color='black', center=False, font_override=None):
    f = font_override if font_override else font
    img = f.render(text, True, color)
    if center:
        rect = img.get_rect(center=(x, y))
        screen.blit(img, rect)
    else:
        screen.blit(img, (x, y))

def input_names():
    player1_name = ''
    player2_name = ''
    input_active = True
    current_input = 1

    while input_active:
        screen.fill(light_blue)
        draw_text("Enter Player 1 Name:", screen_width // 2, screen_height // 2 - 80, center=True, font_override=big_font)
        draw_text(player1_name or "_", screen_width // 2, screen_height // 2 - 40, center=True, font_override=big_font)

        draw_text("Enter Player 2 Name:", screen_width // 2, screen_height // 2 + 20, center=True, font_override=big_font)
        draw_text(player2_name or "_", screen_width // 2, screen_height // 2 + 60, center=True, font_override=big_font)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if current_input == 1:
                        player1_name = player1_name[:-1]
                    elif current_input == 2:
                        player2_name = player2_name[:-1]
                elif event.key == pygame.K_RETURN:
                    if current_input == 1 and player1_name:
                        current_input = 2
                    elif current_input == 2 and player2_name:
                        input_active = False
                else:
                    char = event.unicode
                    if char.isprintable():
                        if current_input == 1 and len(player1_name) < 12:
                            player1_name += char
                        elif current_input == 2 and len(player2_name) < 12:
                            player2_name += char
    return player1_name, player2_name

# ___ getting GUI to run ___ #

player_name, enemy_name = input_names()

# quick random try at putting in a png background
#background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
#screen.blit(background_image, (-40, -40))
screen.fill(light_blue)
pygame.display.update()

left_board_indent = margin
right_board_indent = margin + board_width + board_spacing
y_indent = margin + 50 

# creating and initialising the computer's (guessing) board and player's board
computer = Player(rows, cols, dark_blue, square_size, left_board_indent, y_indent, enemy_name, 3)
player = Player(rows, cols, dark_blue, square_size, right_board_indent, y_indent, player_name, 3)


# Main Settings button shown in top-right corner during gameplay
settings_button = Button("Settings", screen_width - 120, 10, 100, 40, font, purple, (255, 255, 255))

# Buttons that are shown only on the settings screen
settings_quit_button = Button("Quit", screen_width // 2 - 50, screen_height // 2 - 40, 100, 40, font, red, (255, 255, 255))
settings_main_menu_button = Button("Main Menu", screen_width // 2 - 50, screen_height // 2 + 110, 100, 40, font, light_grey, (255, 255, 255))
settings_restart_button = Button("Restart Game", screen_width // 2 - 60, screen_height // 2 + 10, 120, 40, font, green, (255, 255, 255))
settings_back_button = Button("Back", screen_width // 2 - 50, screen_height // 2 + 60, 100, 40, font, dark_blue, (255, 255, 255))

# restarts the game by resetting the boards and placing new ships

def restart_game():
    global computer_board, boats_board
    global computer_board, boats_board, start_time
    # reset the timer when game restarts
    start_time = time.time()
    screen.fill(light_blue)
    computer_board = Board(rows, cols, dark_blue, square_size, left_board_indent, y_indent, enemy_name)
    boats_board = Board(rows, cols, dark_blue, square_size, right_board_indent, y_indent, player_name)
    computer_board.create()
    boats_board.create()
    computer_board.place_ships(3)
    boats_board.place_ships(3)
    boats_board.draw_ships()
    computer_board.draw()
    boats_board.draw()


# record the start time of the game
start_time = time.time()  
    

# Means that clicking the X will close the window
running = True
while running:
    for event in pygame.event.get():
        # drawing based on current screen 
        if current_screen == "game":
            screen.fill(light_blue)
            computer.board.draw()
            player.board.draw()
            settings_button.draw(screen)
            # calculate and display how long the player has been playing
            elapsed_time = int(time.time() - start_time)
            draw_text(f"Time Survived: {elapsed_time}s", 20, 10, color='red', font_override=bold_font)

        elif current_screen == "settings":
            screen.fill(light_blue)
            draw_text("Settings", screen_width // 2, screen_height // 2 - 100, center=True, font_override=big_font)
            settings_quit_button.draw(screen)
            settings_restart_button.draw(screen)
            settings_back_button.draw(screen)
            settings_main_menu_button.draw(screen)

        pygame.display.update()  
        # if you click on a square, it changes colour to red
        # if you click on a ship, it changes the colour to green
        if event.type == pygame.MOUSEBUTTONDOWN:           
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
            # If the game screen is active, respond to the Settings button
            if current_screen == "game":
                if settings_button.is_clicked((mouse_x, mouse_y)):
                    current_screen = "settings"  # switch to settings screen
                    continue

            # Handle settings screen button clicks
            elif current_screen == "settings":
                if settings_quit_button.is_clicked((mouse_x, mouse_y)):
                    running = False  # Quit the game
                    break
                elif settings_restart_button.is_clicked((mouse_x, mouse_y)):
                    restart_game()       # Restart game logic
                    current_screen = "game"  # return to game screen
                    continue
                elif settings_back_button.is_clicked((mouse_x, mouse_y)):
                    current_screen = "game"  # just go back without restarting
                    continue
                elif settings_main_menu_button.is_clicked((mouse_x, mouse_y)):
                    # Go back to the main menu: re-input names and restart game
                    player_name, enemy_name = input_names()  # Go through name entry again
                    restart_game()  # Recreate boards and ships
                    current_screen = "game"  # Return to gameplay screen
                    continue
                    
            row, col = computer.board.get_clicked_position(mouse_x, mouse_y)
            # checks if click is on the board
            if (row is not None and col is not None and computer.board.board[row,col].been_clicked == False):
                if(computer.board.board[row, col].is_ship):
                    computer.board.change_square_colour(row, col, red)
                    computer.board.draw()
                else:
                    computer.board.change_square_colour(row, col, green)
                    computer.board.draw()
                # time for the computer to go
                computers_turn(player.board)
                player.board.draw()

        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()

pygame.quit()







