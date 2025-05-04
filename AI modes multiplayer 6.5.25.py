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
        self.place_ships()

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

mode_selected = False
player_names = []
boards = []
num_players = 0
vs_computer = False
turn = 0
winner = None
ai_pending = False



# === AI Difficulty Selection ===
def get_difficulty():
    easy_btn = Button("Easy", screen_width//2 - 100, 180, 200, 60)
    med_btn = Button("Medium", screen_width//2 - 100, 260, 200, 60)
    hard_btn = Button("Hard", screen_width//2 - 100, 340, 200, 60)

    while True:
        screen.fill(light_blue)
        draw_text_center("Select Computer Difficulty", screen, 100)
        easy_btn.draw(screen)
        med_btn.draw(screen)
        hard_btn.draw(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if easy_btn.is_clicked(pos):
                    return "easy"
                elif med_btn.is_clicked(pos):
                    return "medium"
                elif hard_btn.is_clicked(pos):
                    return "hard"

last_hits = []

def computer_turn_easy(player_board):
    player_board.click_random()

def computer_turn_medium(player_board):
    global last_hits
    candidates = []
    for square in last_hits:
        r, c = square
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = r+dr, c+dc
            if 0 <= nr < rows and 0 <= nc < cols:
                target = player_board.grid[nr][nc]
                if not target.been_clicked:
                    candidates.append((nr, nc))

    if candidates:
        r, c = random.choice(candidates)
    else:
        unclicked = [(r, c) for r in range(rows) for c in range(cols)
                     if not player_board.grid[r][c].been_clicked]
        r, c = random.choice(unclicked)

    target = player_board.grid[r][c]
    target.click()
    if target.is_ship:
        last_hits.append((r, c))


def computer_turn_hard(player_board):
    global last_hits

    def get_line_targets():
        if len(last_hits) < 2:
            return []
        r1, c1 = last_hits[0]
        r2, c2 = last_hits[1]
        dr = r2 - r1
        dc = c2 - c1
        targets = []
        for direction in [1, -1]:
            nr = last_hits[-1][0] + dr * direction
            nc = last_hits[-1][1] + dc * direction
            if 0 <= nr < rows and 0 <= nc < cols:
                sq = player_board.grid[nr][nc]
                if not sq.been_clicked:
                    targets.append((nr, nc))
        return targets

    def get_adjacent_targets():
        candidates = []
        for r, c in last_hits:
            for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                nr, nc = r+dr, c+dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    sq = player_board.grid[nr][nc]
                    if not sq.been_clicked:
                        candidates.append((nr, nc))
        return candidates

    def probability_map():
        probs = np.zeros((rows, cols))
        ship_sizes = [2, 3, 4]
        for ship_len in ship_sizes:
            for r in range(rows):
                for c in range(cols - ship_len + 1):
                    if all(not player_board.grid[r][c+i].been_clicked for i in range(ship_len)):
                        for i in range(ship_len):
                            probs[r][c+i] += 1
            for c in range(cols):
                for r in range(rows - ship_len + 1):
                    if all(not player_board.grid[r+i][c].been_clicked for i in range(ship_len)):
                        for i in range(ship_len):
                            probs[r+i][c] += 1
        return probs

    def all_adjacent_clicked(r, c):
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = r+dr, c+dc
            if 0 <= nr < rows and 0 <= nc < cols:
                sq = player_board.grid[nr][nc]
                if sq.is_ship and not sq.been_clicked:
                    return False
        return True

    # If in destroy mode (tracking ship)
    if last_hits:
        # Keep attacking around until entire ship is sunk
        candidates = get_line_targets()
        if not candidates:
            candidates = get_adjacent_targets()

        if candidates:
            r, c = random.choice(candidates)
            target = player_board.grid[r][c]
            target.click()
            if target.is_ship:
                last_hits.append((r, c))
            else:
                # Miss - do nothing yet, keep hits
                pass

        # Check if all known hits are fully destroyed
        if all(all_adjacent_clicked(r, c) for r, c in last_hits):
            last_hits = []

    else:
        # Hunt mode: fire based on probability
        probs = probability_map()
        max_prob = np.max(probs)
        best_choices = [(r, c) for r in range(rows) for c in range(cols)
                        if not player_board.grid[r][c].been_clicked and probs[r][c] == max_prob]
        r, c = random.choice(best_choices)
        target = player_board.grid[r][c]
        target.click()
        if target.is_ship:
            last_hits = [(r, c)]


def get_board_position(index):
    col = index % 2
    row = index // 2
    x = margin + col * (board_width + board_spacing)
    y = margin + row * (board_height + board_spacing)
    return x, y


running = True
in_menu = True
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
                            difficulty = get_difficulty()
                        else:
                            num_players = i + 1
                        result = get_player_names(num_players if not vs_computer else 1)
                        if result is None:
                            break
                        player_names = result
                        if vs_computer:
                            player_names.append("Computer")
                        boards = []
                        for j, name in enumerate(player_names):
                            x, y = get_board_position(j)
                            boards.append(Board(x, y, name))
                        in_menu = False
                        winner = None
                        turn = 0
                        ai_pending = False
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

        if vs_computer and turn == 1:
            pygame.time.delay(500)
            if difficulty == "easy":
                computer_turn_easy(boards[0])
            elif difficulty == "medium":
                computer_turn_medium(boards[0])
            else:
                computer_turn_hard(boards[0])
            if not boards[0].has_ships_remaining():
                winner = player_names[1]
            else:
                turn = 0
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
