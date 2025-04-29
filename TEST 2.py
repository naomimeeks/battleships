import pygame
import random
import numpy as np

pygame.init()

light_blue = pygame.Color(173, 216, 253)
dark_blue = pygame.Color(0, 0, 173)
red = pygame.Color(200, 0, 0)
green = pygame.Color(0, 255, 0)
pink = pygame.Color(255, 105, 180)
yellow = pygame.Color(255, 255, 0)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)

rows, cols = 9, 9
square_size = 40
gap_size = 5
margin = 50
board_spacing = 80

font = pygame.font.SysFont("arial", 20)
big_font = pygame.font.SysFont("arial", 32)

class Square:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, square_size, square_size)
        self.colour = dark_blue
        self.is_ship = False
        self.been_clicked = False

    def draw(self, screen, reveal=False):
        colour = self.colour
        if reveal and self.is_ship and not self.been_clicked:
            colour = pink
        pygame.draw.rect(screen, colour, self.rect)

    def click(self):
        self.been_clicked = True
        if self.is_ship:
            self.colour = red
        else:
            self.colour = green

class Board:
    def __init__(self, x_indent, y_indent, name):
        self.name = name
        self.x_indent = x_indent
        self.y_indent = y_indent
        self.grid = np.empty((rows, cols), dtype=object)
        for r in range(rows):
            for c in range(cols):
                x = x_indent + c * (square_size + gap_size)
                y = y_indent + r * (square_size + gap_size)
                self.grid[r, c] = Square(x, y)

    def place_ships(self):
        ship_sizes = [2, 3, 4]
        for size in ship_sizes:
            placed = False
            while not placed:
                orientation = random.choice(["H", "V"])
                r, c = random.randint(0, rows - 1), random.randint(0, cols - 1)
                if orientation == "H" and c + size <= cols:
                    if all(not self.grid[r, c+i].is_ship for i in range(size)):
                        for i in range(size):
                            self.grid[r, c+i].is_ship = True
                        placed = True
                elif orientation == "V" and r + size <= rows:
                    if all(not self.grid[r+i, c].is_ship for i in range(size)):
                        for i in range(size):
                            self.grid[r+i, c].is_ship = True
                        placed = True

    def draw(self, screen, reveal_ships=False, highlight=False):
        for r in range(rows):
            for c in range(cols):
                self.grid[r, c].draw(screen, reveal=reveal_ships)
        text = font.render(self.name, True, black)
        screen.blit(text, (self.x_indent + board_width//2 - text.get_width()//2, self.y_indent - 30))

        if highlight:
            outline_rect = pygame.Rect(
                self.x_indent - 3,
                self.y_indent - 3,
                cols * (square_size + gap_size) - gap_size + 6,
                rows * (square_size + gap_size) - gap_size + 6
            )
            pygame.draw.rect(screen, yellow, outline_rect, 4)

    def handle_click(self, x, y):
        for r in range(rows):
            for c in range(cols):
                if self.grid[r, c].rect.collidepoint(x, y) and not self.grid[r, c].been_clicked:
                    self.grid[r, c].click()
                    return True
        return False

    def has_ships_remaining(self):
        for row in self.grid:
            for square in row:
                if square.is_ship and not square.been_clicked:
                    return True
        return False

    def click_random(self):
        unclicked = [s for row in self.grid for s in row if not s.been_clicked]
        if unclicked:
            random.choice(unclicked).click()

class Button:
    def __init__(self, text, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text

    def draw(self, screen):
        pygame.draw.rect(screen, black, self.rect, 2)
        label = font.render(self.text, True, black)
        label_rect = label.get_rect(center=self.rect.center)
        screen.blit(label, label_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

def draw_text_center(text, screen, y):
    rendered = big_font.render(text, True, black)
    rect = rendered.get_rect(center=(screen_width // 2, y))
    screen.blit(rendered, rect)

def get_player_names(n):
    names = []
    input_active = True
    current_name = ""
    back_button = Button("Back", screen_width - 110, 10, 100, 40)

    while input_active:
        screen.fill(light_blue)
        draw_text_center(f"Enter name for Player {len(names)+1}", screen, screen_height // 2 - 40)
        draw_text_center(current_name or "_", screen, screen_height // 2 + 10)
        back_button.draw(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.is_clicked(pygame.mouse.get_pos()):
                    return None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if current_name:
                        names.append(current_name)
                        current_name = ""
                        if len(names) == n:
                            input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    current_name = current_name[:-1]
                else:
                    if len(current_name) < 12:
                        current_name += event.unicode
    return names

def get_placement_mode():
    random_btn = Button("Random Placement", screen_width//2 - 220, screen_height//2, 200, 60)
    manual_btn = Button("Manual Placement", screen_width//2 + 20, screen_height//2, 200, 60)

    while True:
        screen.fill(light_blue)
        draw_text_center("Choose Ship Placement Mode", screen, screen_height//2 - 80)
        random_btn.draw(screen)
        manual_btn.draw(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if random_btn.is_clicked(pos):
                    return "random"
                elif manual_btn.is_clicked(pos):
                    return "manual"

def is_valid_ship_placement(board, r, c, size, orientation):
    try:
        if orientation == "H":
            if c + size > cols:
                return False
            return all(not board.grid[r, c+i].is_ship for i in range(size))
        else:
            if r + size > rows:
                return False
            return all(not board.grid[r+i, c].is_ship for i in range(size))
    except IndexError:
        return False

def manual_ship_placement(board, player_name):
    ship_sizes = [2, 3, 4]
    current_orientation = "H"
    ship_index = 0

    while ship_index < len(ship_sizes):
        size = ship_sizes[ship_index]
        screen.fill(light_blue)
        board.draw(screen, reveal_ships=True)
        draw_text_center(f"{player_name}: Place ship of size {size}", screen, 30)
        draw_text_center("Press 'R' to rotate | Click to place", screen, screen_height - 30)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    current_orientation = "V" if current_orientation == "H" else "H"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                for r in range(rows):
                    for c in range(cols):
                        square = board.grid[r, c]
                        if square.rect.collidepoint(x, y):
                            if is_valid_ship_placement(board, r, c, size, current_orientation):
                                for i in range(size):
                                    if current_orientation == "H":
                                        board.grid[r, c + i].is_ship = True
                                    else:
                                        board.grid[r + i, c].is_ship = True
                                ship_index += 1
                            break

def get_board_position(index):
    col = index % 2
    row = index // 2
    x = margin + col * (board_width + board_spacing)
    y = margin + row * (board_height + board_spacing)
    return x, y

board_width = cols * (square_size + gap_size)
board_height = rows * (square_size + gap_size)
screen_width = 2 * margin + board_width * 2 + board_spacing
screen_height = 2 * margin + board_height * 2
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Multiplayer Battleships")

menu_buttons = [
    Button("1 vs Computer", screen_width//2 - 200, 100, 180, 100),
    Button("1v1", screen_width//2 + 20, 100, 180, 100),
    Button("1v1v1", screen_width//2 - 200, 250, 180, 100),
    Button("1v1v1v1", screen_width//2 + 20, 250, 180, 100),
]
back_button = Button("Back", screen_width - 110, 10, 100, 40)
main_menu_button = Button("Main Menu", screen_width // 2 - 75, screen_height // 2 + 60, 150, 40)

running = True
in_menu = True
player_names = []
boards = []
num_players = 0
vs_computer = False
turn = 0
winner = None
placement_mode = "random"

while running:
    screen.fill(light_blue)

    if in_menu:
        draw_text_center("Choose Game Mode", screen, 40)
        for button in menu_buttons:
            button.draw(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for i, btn in enumerate(menu_buttons):
                    if btn.is_clicked(pos):
                        if i == 0:
                            num_players = 2
                            vs_computer = True
                        else:
                            num_players = i + 1
                        result = get_player_names(num_players if not vs_computer else 1)
                        if result is None:
                            break
                        player_names = result
                        if vs_computer:
                            player_names.append("Computer")
                        placement_mode = get_placement_mode()
                        boards = []
                        for j, name in enumerate(player_names):
                            x, y = get_board_position(j)
                            board = Board(x, y, name)
                            if vs_computer and name == "Computer":
                                board.place_ships()
                            elif placement_mode == "manual":
                                manual_ship_placement(board, name)
                            else:
                                board.place_ships()
                            boards.append(board)
                        in_menu = False
                        winner = None
                        turn = 0
    elif winner:
        screen.fill(light_blue)
        draw_text_center(f"Congratulations {winner} Wins!", screen, screen_height // 2 - 30)
        main_menu_button.draw(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if main_menu_button.is_clicked(pygame.mouse.get_pos()):
                    in_menu = True
                    winner = None
    else:
        screen.fill(light_blue)
        for i, board in enumerate(boards):
            board.draw(screen, reveal_ships=(i == turn), highlight=(i == turn))

        draw_text_center(f"{player_names[turn]}'s Turn - Click an opponent's board", screen, screen_height - 40)
        back_button.draw(screen)
        pygame.display.flip()

        if vs_computer and player_names[turn] == "Computer":
            pygame.time.delay(500)
            boards[0].click_random()
            if not boards[0].has_ships_remaining():
                winner = "Computer"
            else:
                turn = (turn + 1) % len(player_names)
            continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.is_clicked(pygame.mouse.get_pos()):
                    in_menu = True
                    continue
                x, y = pygame.mouse.get_pos()
                for i, board in enumerate(boards):
                    if i != turn:
                        if board.handle_click(x, y):
                            eliminated = [b for b in boards if not b.has_ships_remaining()]
                            if len(eliminated) == len(boards) - 1:
                                for i, b in enumerate(boards):
                                    if b.has_ships_remaining():
                                        winner = player_names[i]
                                        break
                            else:
                                turn = (turn + 1) % len(player_names)
                            break

pygame.quit()
