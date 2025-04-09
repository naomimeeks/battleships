import pygame
import random
import time

pygame.init()

# --- Constants ---
CELL_SIZE = 50
GRID_SIZE = 10
MARGIN = 20
BOARD_GAP = 100
LABEL_SPACE = 40
SCREEN_WIDTH = GRID_SIZE * CELL_SIZE * 2 + BOARD_GAP + MARGIN * 2 + LABEL_SPACE * 2
SCREEN_HEIGHT = GRID_SIZE * CELL_SIZE + MARGIN * 2 + LABEL_SPACE + 100

# --- Colours ---
WHITE = (255, 255, 255)
BLUE = (0, 120, 215)
GREY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# --- Fonts ---
font = pygame.font.SysFont("arial", 24)
big_font = pygame.font.SysFont("arial", 32)

# --- Create window ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Battleship with Player Names")

# --- Functions ---
def create_board(size):
    return [['O' for _ in range(size)] for _ in range(size)]

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

def draw_text(text, x, y, color=BLACK, center=False, font_override=None):
    f = font_override if font_override else font
    img = f.render(text, True, color)
    if center:
        rect = img.get_rect(center=(x, y))
        screen.blit(img, rect)
    else:
        screen.blit(img, (x, y))

def draw_board(board, offset_x, offset_y, reveal_ships=False, show_labels=True):
    letters = 'ABCDEFGHIJ'
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x = offset_x + col * CELL_SIZE
            y = offset_y + row * CELL_SIZE
            cell = board[row][col]

            colour = BLUE
            if cell == 'X':
                colour = RED
            elif cell == 'M':
                colour = GREY
            elif cell == 'S' and reveal_ships:
                colour = GREEN

            pygame.draw.rect(screen, colour, (x, y, CELL_SIZE - 2, CELL_SIZE - 2))

    if show_labels:
        # X Axis (A–J)
        for col in range(GRID_SIZE):
            label = letters[col]
            x = offset_x + col * CELL_SIZE + CELL_SIZE // 2
            draw_text(label, x, offset_y - 20, center=True)

        # Y Axis (1–10)
        for row in range(GRID_SIZE):
            label = str(row + 1)
            y = offset_y + row * CELL_SIZE + CELL_SIZE // 2
            draw_text(label, offset_x - 20, y, center=True)

def input_names():
    player1_name = ''
    player2_name = ''
    input_active = True
    current_input = 1

    while input_active:
        screen.fill(WHITE)
        draw_text("Enter Player 1 Name:", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80, center=True, font_override=big_font)
        draw_text(player1_name or "_", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40, center=True, font_override=big_font)

        draw_text("Enter Player 2 Name:", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20, center=True, font_override=big_font)
        draw_text(player2_name or "_", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60, center=True, font_override=big_font)

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

# --- Get usernames before starting the game ---
player_name, enemy_name = input_names()

# --- Game Setup ---
player_board = create_board(GRID_SIZE)
computer_board = create_board(GRID_SIZE)
computer_view = create_board(GRID_SIZE)

for size in [3, 4, 5]:
    place_ship(player_board, size)
    place_ship(computer_board, size)

# --- Game State ---
start_time = time.time()
points = 0

# --- Main Game Loop ---
running = True
while running:
    screen.fill(WHITE)

    # Board positions
    board_y = MARGIN + 100  # Adjusted to leave space for usernames
    player_x = MARGIN + LABEL_SPACE
    enemy_x = player_x + GRID_SIZE * CELL_SIZE + BOARD_GAP

    # --- Draw Boards ---
    draw_board(player_board, player_x, board_y, reveal_ships=True)
    draw_board(computer_view, enemy_x, board_y, reveal_ships=False)

    # --- Draw Time and Points ---
    elapsed_time = int(time.time() - start_time)
    draw_text(f"Time: {elapsed_time}s", SCREEN_WIDTH - 180, 10)
    draw_text(f"Points: {points}", SCREEN_WIDTH - 180, 35)

    # --- Draw Player Names ---
    draw_text(player_name, player_x + GRID_SIZE * CELL_SIZE // 2, board_y - 60, center=True, font_override=big_font)
    draw_text(enemy_name, enemy_x + GRID_SIZE * CELL_SIZE // 2, board_y - 60, center=True, font_override=big_font)

    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if enemy_x <= mx < enemy_x + GRID_SIZE * CELL_SIZE and board_y <= my < board_y + GRID_SIZE * CELL_SIZE:
                col = (mx - enemy_x) // CELL_SIZE
                row = (my - board_y) // CELL_SIZE

                if computer_view[row][col] == 'O':
                    if computer_board[row][col] == 'S':
                        computer_view[row][col] = 'X'
                        computer_board[row][col] = 'X'
                        points += 10
                    else:
                        computer_view[row][col] = 'M'

    pygame.display.flip()

pygame.quit()
