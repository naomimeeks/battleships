import pygame
import random
import numpy as np
import time

# --- INIT ---
pygame.init()
pygame.mixer.init()

# --- Sounds ---
explosion_sound = pygame.mixer.Sound("Ship_Explosion.wav")
droplet_sound = pygame.mixer.Sound("WaterDropletEchoed.wav")
victory_sound = pygame.mixer.Sound("Cartoon_Success_Trumpet.wav")
defeat_sound = pygame.mixer.Sound("Cartoon_Failure_Trumpet.wav")

# --- Colors ---
light_blue = pygame.Color(173, 216, 253)
dark_blue = pygame.Color(0, 0, 173)
red = pygame.Color(200, 0, 0)
green = pygame.Color(0, 255, 0)
pink = pygame.Color(255, 105, 180)
yellow = pygame.Color(255, 255, 0)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
preview_color = pygame.Color(144, 238, 144)
invalid_color = pygame.Color(255, 99, 71)

# --- Settings ---
rows, cols = 9, 9
square_size = 40
gap_size = 5
margin = 50
board_spacing = 80
max_columns = 2

font = pygame.font.SysFont("arial", 20)
big_font = pygame.font.SysFont("arial", 32)

board_width = cols * (square_size + gap_size)
board_height = rows * (square_size + gap_size)
screen_width = margin * 2 + max_columns * board_width + (max_columns - 1) * board_spacing
screen_height = margin * 2 + 2 * board_height + board_spacing
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Multiplayer Battleship")

# --- Button ---
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
# --- Square ---
class Square:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, square_size, square_size)
        self.colour = dark_blue
        self.is_ship = False
        self.been_clicked = False

    def draw(self, screen, reveal=False, highlight_color=None):
        colour = self.colour
        if reveal and self.is_ship and not self.been_clicked:
            colour = pink
        if highlight_color:
            colour = highlight_color
        pygame.draw.rect(screen, colour, self.rect)
        pygame.draw.rect(screen, black, self.rect, 1)

    def click(self):
        self.been_clicked = True
        self.colour = red if self.is_ship else green
        return self.is_ship

# --- Board ---
class Board:
    def __init__(self, x_indent, y_indent, name):
        self.name = name
        self.x_indent = x_indent
        self.y_indent = y_indent
        self.grid = self.create()

    def create(self):
        grid = np.empty((rows, cols), dtype=object)
        for r in range(rows):
            for c in range(cols):
                x = self.x_indent + c * (square_size + gap_size)
                y = self.y_indent + r * (square_size + gap_size)
                grid[r, c] = Square(x, y)
        return grid

    def draw(self, screen, reveal_ships=False, highlight=False, preview=None, valid_preview=True):
        for r in range(rows):
            for c in range(cols):
                square = self.grid[r, c]
                highlight_color = None
                if preview and (r, c) in preview:
                    highlight_color = preview_color if valid_preview else invalid_color
                square.draw(screen, reveal=reveal_ships, highlight_color=highlight_color)

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
                    return self.grid[r, c].click()
        return None

    def has_ships_remaining(self):
        for row in self.grid:
            for square in row:
                if square.is_ship and not square.been_clicked:
                    return True
        return False

    def valid_ship_position(self, r, c, size, orientation):
        if orientation == "H":
            if c + size > cols:
                return False
            return all(not self.grid[r, c+i].is_ship for i in range(size))
        else:
            if r + size > rows:
                return False
            return all(not self.grid[r+i, c].is_ship for i in range(size))

    def place_ship(self, r, c, size, orientation):
        for i in range(size):
            rr = r + i if orientation == "V" else r
            cc = c + i if orientation == "H" else c
            self.grid[rr, cc].is_ship = True

# --- Utils ---
def draw_text_center(text, screen, y):
    rendered = big_font.render(text, True, black)
    rect = rendered.get_rect(center=(screen_width // 2, y))
    screen.blit(rendered, rect)

def get_player_names(n):
    names = []
    current_name = ""
    input_active = True
    while input_active:
        screen.fill(light_blue)
        draw_text_center(f"Enter name for Player {len(names)+1}", screen, screen_height // 2 - 40)
        draw_text_center(current_name or "_", screen, screen_height // 2 + 10)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and current_name:
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

def get_board_position(index, total):
    col = index % max_columns
    row = index // max_columns
    x = margin + col * (board_width + board_spacing)
    y = margin + row * (board_height + board_spacing)
    return x, y
# --- Game Setup ---
menu_buttons = [
    Button("1 vs Computer", screen_width//2 - 320, 100, 150, 60),
    Button("1v1", screen_width//2 - 160, 100, 150, 60),
    Button("1v1v1", screen_width//2, 100, 150, 60),
    Button("1v1v1v1", screen_width//2 + 160, 100, 150, 60)
]
main_menu_button = Button("Main Menu", screen_width // 2 - 75, screen_height // 2 + 60, 150, 40)

# Game state
player_names = []
boards = []
player_scores = []
alive = []
placing_index = 0
orientation = "H"
ship_sizes = [2, 3, 4]
current_ship = 0
turn = 0
winner = None
placing_phase = False
running = True
in_menu = True
vs_computer = False
ai_difficulty = None
start_time = time.time()

# --- Main Loop ---
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
                        num_players = [1, 2, 3, 4][i]
                        vs_computer = (i == 0)
                        if vs_computer:
                            # Difficulty buttons
                            difficulty_buttons = [
                                Button("Easy", screen_width//2 - 200, 250, 120, 60),
                                Button("Medium", screen_width//2 - 60, 250, 120, 60),
                                Button("Hard", screen_width//2 + 80, 250, 120, 60)
                            ]
                            choosing = True
                            while choosing:
                                screen.fill(light_blue)
                                draw_text_center("Select AI Difficulty", screen, 150)
                                for b in difficulty_buttons:
                                    b.draw(screen)
                                pygame.display.flip()
                                for e in pygame.event.get():
                                    if e.type == pygame.QUIT:
                                        pygame.quit(); exit()
                                    elif e.type == pygame.MOUSEBUTTONDOWN:
                                        pos = pygame.mouse.get_pos()
                                        for b in difficulty_buttons:
                                            if b.is_clicked(pos):
                                                ai_difficulty = b.text.lower()
                                                choosing = False
                        result = get_player_names(1 if vs_computer else num_players)
                        if result is None:
                            break
                        player_names = result + (["Computer"] if vs_computer else [])
                        boards = [Board(*get_board_position(i, len(player_names)), name) for i, name in enumerate(player_names)]
                        player_scores = [0 for _ in player_names]
                        alive = [True for _ in player_names]
                        in_menu = False
                        placing_phase = True
                        placing_index = 0
                        current_ship = 0
    elif winner:
        draw_text_center(f"{winner} Wins!", screen, screen_height // 2 - 30)
        main_menu_button.draw(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if main_menu_button.is_clicked(pygame.mouse.get_pos()):
                    winner = None
                    in_menu = True

    elif placing_phase:
        board = boards[placing_index]
        size = ship_sizes[current_ship]
        mouse_x, mouse_y = pygame.mouse.get_pos()
        preview_cells = []

        row = col = None
        for r in range(rows):
            for c in range(cols):
                if board.grid[r, c].rect.collidepoint(mouse_x, mouse_y):
                    row, col = r, c
                    break

        valid = False
        if row is not None:
            valid = board.valid_ship_position(row, col, size, orientation)
            preview_cells = [(row+i if orientation == "V" else row, col+i if orientation == "H" else col) for i in range(size)]

        board.draw(screen, reveal_ships=True, highlight=True, preview=preview_cells, valid_preview=valid)
        draw_text_center("Press R to rotate ship", screen, margin // 2)
        draw_text_center(f"{player_names[placing_index]}: Place ship of size {size}", screen, board_height * 2 + margin)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                orientation = "V" if orientation == "H" else "H"
            elif event.type == pygame.MOUSEBUTTONDOWN and valid:
                board.place_ship(row, col, size, orientation)
                current_ship += 1
                if current_ship == len(ship_sizes):
                    current_ship = 0
                    placing_index += 1
                    if vs_computer and placing_index == 1:
                        boards[1].place_ship(0, 0, 2, "H")
                        boards[1].place_ship(2, 2, 3, "V")
                        boards[1].place_ship(5, 5, 4, "H")
                        placing_index += 1
                    if placing_index >= len(player_names):
                        placing_phase = False
                        start_time = time.time()

    else:
        for i, board in enumerate(boards):
            if alive[i]:
                board.draw(screen, reveal_ships=(i == turn), highlight=(i == turn))
        draw_text_center(f"{player_names[turn]}'s Turn", screen, screen_height - 60)
        draw_text_center("Time: " + str(int(time.time() - start_time)) + "s", screen, screen_height - 30)
        draw_text_center(" | ".join([f"{n}: {s}" for n, s in zip(player_names, player_scores)]), screen, 20)
        pygame.display.flip()

        if not alive[turn]:
            turn = (turn + 1) % len(player_names)
            continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                for i, board in enumerate(boards):
                    if i != turn and alive[i]:
                        hit = board.handle_click(x, y)
                        if hit is not None:
                            if hit:
                                explosion_sound.play()
                                player_scores[turn] += 3
                            else:
                                droplet_sound.play()
                            if not board.has_ships_remaining():
                                alive[i] = False
                                if alive.count(True) == 1:
                                    winner = player_names[alive.index(True)]
                                    victory_sound.play()
                            turn = (turn + 1) % len(player_names)
                            while not alive[turn]:
                                turn = (turn + 1) % len(player_names)
                            break

pygame.quit()
