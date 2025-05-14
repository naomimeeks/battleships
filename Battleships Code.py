# Battleship Game - Full Version with Sound, Scores, and Time (Game Logic Restored)

import pygame
import random
import numpy as np
import time

pygame.init()
pygame.mixer.init()

# --- Sounds (updated based on available files) ---
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

# --- Settings ---
rows, cols = 9, 9
square_size = 40
gap_size = 5
margin = 50
board_spacing = 80

font = pygame.font.SysFont("arial", 20)
big_font = pygame.font.SysFont("arial", 32)

board_width = cols * (square_size + gap_size)
board_height = rows * (square_size + gap_size)
screen_width = 2 * margin + board_width * 2 + board_spacing
screen_height = 2 * margin + board_height
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Multiplayer Battleships")

# Lives
heart_img = pygame.image.load("Red_Heart.png").convert_alpha()
heart_img = pygame.transform.scale(heart_img, (20, 20))
# --- Classes ---
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
        pygame.draw.rect(screen, black, self.rect, 1)

    def click(self):
        self.been_clicked = True
        self.colour = red if self.is_ship else green

class Board:
    def __init__(self, x_indent, y_indent, name):
        self.name = name
        self.x_indent = x_indent
        self.y_indent = y_indent
        self.grid = self.create()
        self.ships = []
        self.place_ships()

    def create(self):
        grid = np.empty((rows, cols), dtype=object)
        for r in range(rows):
            for c in range(cols):
                x = self.x_indent + c * (square_size + gap_size)
                y = self.y_indent + r * (square_size + gap_size)
                grid[r, c] = Square(x, y)
        return grid

    def draw(self, screen, reveal_ships=False, highlight=False):
        for r in range(rows):
            for c in range(cols):
                self.grid[r, c].draw(screen, reveal=reveal_ships)

        text = font.render(self.name, True, black)
        screen.blit(text, (self.x_indent + board_width//2 - text.get_width()//2, self.y_indent - 30))

        for i in range(3):
            heart_y = self.y_indent + i * 30 + 20

            if self.name == "Player 1":
                heart_x = self.x_indent - 70
            else:
                heart_x = self.x_indent + board_width + 10

            screen.blit(heart_img, (heart_x, heart_y))

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
                    return self.grid[r, c].is_ship
        return None

    def has_ships_remaining(self):
        for row in self.grid:
            for square in row:
                if square.is_ship and not square.been_clicked:
                    return True
        return False

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

    def click_random(self):
        unclicked = [s for row in self.grid for s in row if not s.been_clicked]
        if unclicked:
            target = random.choice(unclicked)
            target.click()
            return target.is_ship
        return None

# --- Utility ---
def draw_text_center(text, screen, y):
    rendered = big_font.render(text, True, black)
    rect = rendered.get_rect(center=(screen_width // 2, y))
    screen.blit(rendered, rect)


# Intro screen buttons
intro_buttons = [
    Button("Play", screen_width // 2 - 90, 200, 180, 60),
    Button("Settings", screen_width // 2 - 90, 280, 180, 60),
    Button("Quit", screen_width // 2 - 90, 360, 180, 60)  
]

# Setting button on intro screen
settings_buttons = [
    Button("Toggle Sound", screen_width // 2 - 90, 200, 180, 60),
    Button("Theme: Light", screen_width // 2 - 90, 280, 180, 60),
    Button("Back", screen_width - 110, 10, 100, 40)
]

menu_back_button = Button("Back", screen_width - 120, 5, 100, 40)

# --- Menu and Game Loop ---
menu_buttons = [
    Button("1 vs Computer", screen_width//2 - 200, 100, 180, 100),
    Button("1v1", screen_width//2 + 20, 100, 180, 100)
]
back_button = Button("Back", screen_width - 120, 5, 100, 40)
main_menu_button = Button("Main Menu", screen_width // 2 - 75, screen_height // 2 + 60, 150, 40)

def get_player_names(n):
    names = []
    current_name = ""
    input_active = True

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

def get_board_position(index):
    col = index % 2
    row = index // 2
    x = margin + col * (board_width + board_spacing)
    y = margin
    return x, y

player_names = []
boards = []
player_scores = []
vs_computer = False
turn = 0
winner = None
in_menu = True

sound_enabled = True
game_state = "intro"  # intro → menu → game → winner → settings
game_state = "intro"  # Tracks whether we're on the intro, menu, game, or winner screen

start_time = time.time()

running = True
while running:
    if game_state == "settings":
        screen.fill(light_blue)
        draw_text_center("Settings", screen, 60)

        for button in settings_buttons:
            button.draw(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if settings_buttons[0].is_clicked(pos):  # Toggle Sound
                    sound_enabled = not sound_enabled
                    print("Sound:", "On" if sound_enabled else "Off")
                elif settings_buttons[1].is_clicked(pos):  # Theme (placeholder)
                    print("Theme button clicked (placeholder)")
                elif settings_buttons[2].is_clicked(pos):  # Back
                    game_state = "intro"
        continue


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for i, btn in enumerate(menu_buttons):
                    if btn.is_clicked(pos):
                        vs_computer = (i == 0)
                        result = get_player_names(1 if vs_computer else 2)
                        if result is None:
                            break
                        player_names = result
                        if vs_computer:
                            player_names.append("Computer")
                        boards = []
                        player_scores = [0 for _ in player_names]
                        for j, name in enumerate(player_names):
                            x, y = get_board_position(j)
                            boards.append(Board(x, y, name))
                        in_menu = False
                        winner = None
                        turn = 0
                        start_time = time.time()

    elif winner:
        screen.fill(light_blue)
        draw_text_center(f"{winner} Wins!", screen, screen_height // 2 - 30)
        main_menu_button.draw(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if main_menu_button.is_clicked(pygame.mouse.get_pos()):
                    in_menu = True
                    winner = None

    elif game_state == "game":
        screen.fill(light_blue)
        for i, board in enumerate(boards):
            board.draw(screen, reveal_ships=(i == turn), highlight=(i == turn))

        draw_text_center(f"{player_names[turn]}'s Turn", screen, screen_height - 30)
        score_text = " | ".join([f"{name}: {score}" for name, score in zip(player_names, player_scores)])
        draw_text_center(score_text, screen, 20)
        elapsed_time = int(time.time() - start_time)
        time_text = font.render(f"Time: {elapsed_time}s", True, black)
        screen.blit(time_text, (screen_width - time_text.get_width() - 10, screen_height - time_text.get_height() - 10))
        back_button.draw(screen)
        pygame.display.flip()


    if game_state == "intro":
        screen.fill(light_blue)
        draw_text_center("BATTLESHIPS", screen, 100)
        for button in intro_buttons:
            button.draw(screen)
        pygame.display.flip()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:

                pos = pygame.mouse.get_pos()
                if intro_buttons[0].is_clicked(pos):  # Play
                    game_state = "menu" 
                    in_menu = True
                elif intro_buttons[1].is_clicked(pos):  # Settings
                    game_state = "settings"
                elif intro_buttons[2].is_clicked(pos):  # Quit
                    running = False
        continue


 

    if game_state == "menu":
        screen.fill(light_blue)
        draw_text_center("Choose Game Mode", screen, 40)
        for button in menu_buttons:
            button.draw(screen)
        menu_back_button.draw(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for i, btn in enumerate(menu_buttons):
                    if btn.is_clicked(pos):
                        vs_computer = (i == 0)
                        result = get_player_names(1 if vs_computer else 2)
                        if result is None:
                            break
                        player_names = result
                        if vs_computer:
                            player_names.append("Computer")
                        boards = []
                        player_scores = [0 for _ in player_names]
                        for j, name in enumerate(player_names):
                            x, y = get_board_position(j)
                            boards.append(Board(x, y, name))
                        in_menu = False
                        winner = None
                        turn = 0
                        start_time = time.time()
                        game_state = "game"
            if menu_back_button.is_clicked(pos):
                game_state = "intro"

    elif winner:
        screen.fill(light_blue)
        draw_text_center(f"{winner} Wins!", screen, screen_height // 2 - 30)
        main_menu_button.draw(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if main_menu_button.is_clicked(pygame.mouse.get_pos()):
                    in_menu = True
                    winner = None
                    game_state = "intro"
     
    else:
        screen.fill(light_blue)
        for i, board in enumerate(boards):
            board.draw(screen, reveal_ships=(i == turn), highlight=(i == turn))

        draw_text_center(f"{player_names[turn]}'s Turn", screen, screen_height - 30)
        score_text = " | ".join([f"{name}: {score}" for name, score in zip(player_names, player_scores)])
        draw_text_center(score_text, screen, 20)
        elapsed_time = int(time.time() - start_time)
        time_text = font.render(f"Time: {elapsed_time}s", True, black)
        screen.blit(time_text, (screen_width - time_text.get_width() - 10, screen_height - time_text.get_height() - 10))

        back_button.draw(screen)
        pygame.display.flip()

        if vs_computer and turn == 1:
            pygame.time.delay(500)
            hit = boards[0].click_random()
            if hit:
                explosion_sound.play()
                player_scores[1] += 3
            else:
                droplet_sound.play()
            if not boards[0].has_ships_remaining():
                winner = player_names[1]
                victory_sound.play()
            else:
                turn = 0   
            continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.is_clicked(pygame.mouse.get_pos()):
                    in_menu = True
                    break
                x, y = pygame.mouse.get_pos()
                for i, board in enumerate(boards):
                    if i != turn:
                        hit = board.handle_click(x, y)
                        if hit is not None:
                            if hit:
                                explosion_sound.play()
                                player_scores[turn] += 3
                            else:
                                droplet_sound.play()
                            if not board.has_ships_remaining():
                                winner = player_names[turn]
                                victory_sound.play()
                            else:
                                turn = (turn + 1) % len(player_names)
                            break


pygame.quit()
