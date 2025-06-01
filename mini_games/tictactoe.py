# MysteryIsland/mini_games/tictactoe.py
# tictactoe.py

import pygame
import random
import math


BOARD_ROWS = 3
BOARD_COLS = 3
LINE_WIDTH = 4

def tictactoe_game(screen, inventory, screen_manager, victory_imgs):
    WIDTH, HEIGHT = screen.get_size()
    SQUARE_SIZE = 0
    offset_x = 0
    offset_y = 0

    x_image = pygame.image.load("../MysteryIsland/icons/x_img.png").convert_alpha()
    o_image = pygame.image.load("../MysteryIsland/icons/o_img.png").convert_alpha()
    background_image = pygame.image.load("../MysteryIsland/icons/screen_tictactoe.png").convert()
    defeat_image = pygame.image.load("../MysteryIsland/icons/defeattictactoe.png").convert()
    victory_bg_image = pygame.image.load("../MysteryIsland/icons/screen_restictac.png").convert()

    def update_sizes():
        nonlocal WIDTH, HEIGHT, SQUARE_SIZE, offset_x, offset_y
        WIDTH, HEIGHT = screen.get_size()
        SQUARE_SIZE = min(WIDTH, HEIGHT) // 4
        total_board_width = SQUARE_SIZE * BOARD_COLS
        total_board_height = SQUARE_SIZE * BOARD_ROWS
        offset_x = (WIDTH - total_board_width) // 2
        offset_y = (HEIGHT - total_board_height) // 2

    def draw_background():
        scaled_bg = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
        screen.blit(scaled_bg, (0, 0))

    def draw_board():
        draw_background()
        line_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        transparent = (* (23, 145, 135), 0)
        for i in range(1, BOARD_ROWS):
            y = offset_y + i * SQUARE_SIZE
            pygame.draw.line(line_surface, transparent, (offset_x, y), (offset_x + SQUARE_SIZE * BOARD_COLS, y), LINE_WIDTH)
        for i in range(1, BOARD_COLS):
            x = offset_x + i * SQUARE_SIZE
            pygame.draw.line(line_surface, transparent, (x, offset_y), (x, offset_y + SQUARE_SIZE * BOARD_ROWS), LINE_WIDTH)
        screen.blit(line_surface, (0, 0))

    def draw_figures(board):
        for r in range(BOARD_ROWS):
            for c in range(BOARD_COLS):
                cell = board[r][c]
                if cell:
                    img = o_image if cell == 'O' else x_image
                    scaled = pygame.transform.smoothscale(img, (SQUARE_SIZE, SQUARE_SIZE))
                    screen.blit(scaled, (offset_x + c * SQUARE_SIZE, offset_y + r * SQUARE_SIZE))

    def check_win(board, player):
        for i in range(BOARD_ROWS):
            if all(board[i][j] == player for j in range(BOARD_COLS)): return True
            if all(board[j][i] == player for j in range(BOARD_ROWS)): return True
        if all(board[i][i] == player for i in range(BOARD_ROWS)): return True
        if all(board[i][BOARD_COLS - 1 - i] == player for i in range(BOARD_ROWS)): return True
        return False

    def is_board_full(board):
        return all(board[r][c] != '' for r in range(BOARD_ROWS) for c in range(BOARD_COLS))

    def minimax(board, depth, is_maximizing):
        if check_win(board, 'O'): return 1
        if check_win(board, 'X'): return -1
        if is_board_full(board): return 0
        if is_maximizing:
            best = -math.inf
            for r in range(BOARD_ROWS):
                for c in range(BOARD_COLS):
                    if board[r][c] == '':
                        board[r][c] = 'O'
                        score = minimax(board, depth + 1, False)
                        board[r][c] = ''
                        best = max(best, score)
            return best
        else:
            best = math.inf
            for r in range(BOARD_ROWS):
                for c in range(BOARD_COLS):
                    if board[r][c] == '':
                        board[r][c] = 'X'
                        score = minimax(board, depth + 1, True)
                        board[r][c] = ''
                        best = min(best, score)
            return best

    def ai_move(board):
        if random.random() < 0.3:
            empties = [(r, c) for r in range(BOARD_ROWS) for c in range(BOARD_COLS) if board[r][c] == '']
            if empties:
                r, c = random.choice(empties)
                board[r][c] = 'O'
        else:
            best_score = -math.inf
            best_move = None
            for r in range(BOARD_ROWS):
                for c in range(BOARD_COLS):
                    if board[r][c] == '':
                        board[r][c] = 'O'
                        score = minimax(board, 0, False)
                        board[r][c] = ''
                        if score > best_score:
                            best_score = score
                            best_move = (r, c)
            if best_move:
                board[best_move[0]][best_move[1]] = 'O'

    def play_one_round():
        nonlocal screen
        update_sizes()
        board = [['' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
        game_over = False
        player_turn = True

        while True:
            draw_board()
            draw_figures(board)
            pygame.display.update()

            if game_over:
                pygame.time.delay(1000)
                if check_win(board, 'X') or (not check_win(board, 'O') and is_board_full(board)):
                    return True
                return False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if screen_manager.is_fullscreen:
                            screen = screen_manager.toggle_fullscreen()
                            update_sizes()
                        else:
                            return "exit"
                    elif event.key == pygame.K_F11:
                        screen = screen_manager.toggle_fullscreen()
                        update_sizes()
                if player_turn and event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    row = (my - offset_y) // SQUARE_SIZE
                    col = (mx - offset_x) // SQUARE_SIZE
                    if 0 <= row < BOARD_ROWS and 0 <= col < BOARD_COLS and board[row][col] == '':
                        board[row][col] = 'X'
                        if check_win(board, 'X'):
                            game_over = True
                        else:
                            player_turn = False

            if not player_turn and not game_over:
                pygame.time.delay(300)
                ai_move(board)
                if check_win(board, 'O'):
                    game_over = True
                player_turn = True

            if is_board_full(board) and not game_over:
                game_over = True

    # --- Основная логика ---
    wins = 0
    for _ in range(3):
        res = play_one_round()
        if res == "exit":
            return False
        if res:
            wins += 1

    '''draw_background()
    pygame.display.update()'''

    def show_centered_text(bg_image, title, subtitle, color=(255, 255, 255)):
        bg_scaled = pygame.transform.scale(bg_image, screen.get_size())
        screen.blit(bg_scaled, (0, 0))
        font_title = pygame.font.SysFont("arial", 48, bold=True)
        font_sub = pygame.font.SysFont("arial", 32)

        title_surf = font_title.render(title, True, color)

        title_rect = title_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40))

        # Разбить текст подзаголовка по предложениям
        lines = [line.strip() for line in subtitle.split('.') if line.strip()]
        font_sub = pygame.font.SysFont("arial", 32)
        line_spacing = 40
        start_y = HEIGHT // 2 + 20

        for i, line in enumerate(lines):
            line += '.'  # добавить точку обратно
            line_surf = font_sub.render(line, True, color)
            line_rect = line_surf.get_rect(center=(WIDTH // 2, start_y + i * line_spacing))
            screen.blit(line_surf, line_rect)

        screen.blit(title_surf, title_rect)

        pygame.display.flip()

        # ждём нажатия
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                    waiting = False


    if wins == 0:
        defeat_scaled = pygame.transform.scale(defeat_image, (WIDTH, HEIGHT))
        screen.blit(defeat_scaled, (0, 0))
        pygame.display.update()
        # ждём, пока игрок нажмёт клавишу
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                    waiting = False
        return False

    elif wins == 1:
        inventory.add("ветки")
        show_centered_text(victory_bg_image, "Вы выиграли один раунд", "Получены ветки для костра.")
    elif wins == 2:
        inventory.add("жильё")
        show_centered_text(victory_bg_image, "Вы выиграли два раунда", "Получены ветки для костра. Построено жильё из веток.")
    else:
        inventory.add("фрукты")
        show_centered_text(victory_bg_image, "Вы выиграли все раунды", "Получены ветки для костра. Построено жильё из веток. Обезьяны угостили вас фруктами.")

    #show_victory_sequence(screen, victory_imgs)
    return True


'''def show_victory_sequence(screen, imgs):
    screen_width, screen_height = screen.get_size()
    fade_surface = pygame.Surface((screen_width, screen_height))
    fade_surface.fill((0, 0, 0))

    for img in imgs:
        scaled_img = pygame.transform.scale(img, (screen_width, screen_height))
        for alpha in range(0, 256, 15):
            screen.blit(scaled_img, (0, 0))
            fade_surface.set_alpha(255 - alpha)
            screen.blit(fade_surface, (0, 0))
            pygame.display.flip()
            pygame.time.delay(30)

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                    waiting = False

        for alpha in range(0, 256, 15):
            screen.blit(scaled_img, (0, 0))
            fade_surface.set_alpha(alpha)
            screen.blit(fade_surface, (0, 0))
            pygame.display.flip()
            pygame.time.delay(30)

'''


'''import pygame
import random
import math
from game1.mini_games.common.ui import show_message

BOARD_ROWS = 3
BOARD_COLS = 3
LINE_WIDTH = 4

def tictactoe_game(screen, inventory, screen_manager, victory_imgs):
    # Инициализация размеров
    WIDTH, HEIGHT = screen.get_size()
    SQUARE_SIZE = 0
    offset_x = 0
    offset_y = 0

    # Загрузка изображений крестика, нолика и фона
    x_image = pygame.image.load("C:/Users/bel31/PycharmProjects/pythonProject/MysteryIsland/icons/x_img.png").convert_alpha()
    o_image = pygame.image.load("C:/Users/bel31/PycharmProjects/pythonProject/MysteryIsland/icons/o_img.png").convert_alpha()
    background_image = pygame.image.load(
        "C:/Users/bel31/PycharmProjects/pythonProject/MysteryIsland/icons/screen_tictactoe.png"
    ).convert()

    def update_sizes():
        nonlocal WIDTH, HEIGHT, SQUARE_SIZE, offset_x, offset_y
        WIDTH, HEIGHT = screen.get_size()
        SQUARE_SIZE = min(WIDTH, HEIGHT) // 4
        total_board_width = SQUARE_SIZE * BOARD_COLS
        total_board_height = SQUARE_SIZE * BOARD_ROWS
        offset_x = (WIDTH - total_board_width) // 2
        offset_y = (HEIGHT - total_board_height) // 2

    def draw_background():
        """Отрисовать фон-изображение на весь экран."""
        scaled_bg = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
        screen.blit(scaled_bg, (0, 0))

    def draw_board():
        """Нарисовать фон + сетку."""
        draw_background()
        line_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        transparent = (* (23, 145, 135), 0)  # LINE_COLOR + нулевая альфа

        # горизонтальные линии
        for i in range(1, BOARD_ROWS):
            y = offset_y + i * SQUARE_SIZE
            pygame.draw.line(
                line_surface, transparent,
                (offset_x, y),
                (offset_x + SQUARE_SIZE * BOARD_COLS, y),
                LINE_WIDTH
            )
        # вертикальные линии
        for i in range(1, BOARD_COLS):
            x = offset_x + i * SQUARE_SIZE
            pygame.draw.line(
                line_surface, transparent,
                (x, offset_y),
                (x, offset_y + SQUARE_SIZE * BOARD_ROWS),
                LINE_WIDTH
            )

        screen.blit(line_surface, (0, 0))

    def draw_figures(board):
        """Нарисовать крестики и нолики."""
        for r in range(BOARD_ROWS):
            for c in range(BOARD_COLS):
                cell = board[r][c]
                if cell:
                    img = o_image if cell == 'O' else x_image
                    scaled = pygame.transform.smoothscale(img, (SQUARE_SIZE, SQUARE_SIZE))
                    screen.blit(scaled, (offset_x + c * SQUARE_SIZE, offset_y + r * SQUARE_SIZE))

    def check_win(board, player):
        # строки и столбцы
        for i in range(BOARD_ROWS):
            if all(board[i][j] == player for j in range(BOARD_COLS)):
                return True
            if all(board[j][i] == player for j in range(BOARD_ROWS)):
                return True
        # диагонали
        if all(board[i][i] == player for i in range(BOARD_ROWS)):
            return True
        if all(board[i][BOARD_COLS - 1 - i] == player for i in range(BOARD_ROWS)):
            return True
        return False

    def is_board_full(board):
        return all(board[r][c] != '' for r in range(BOARD_ROWS) for c in range(BOARD_COLS))

    def minimax(board, depth, is_maximizing):
        if check_win(board, 'O'):
            return 1
        if check_win(board, 'X'):
            return -1
        if is_board_full(board):
            return 0

        if is_maximizing:
            best = -math.inf
            for r in range(BOARD_ROWS):
                for c in range(BOARD_COLS):
                    if board[r][c] == '':
                        board[r][c] = 'O'
                        score = minimax(board, depth + 1, False)
                        board[r][c] = ''
                        best = max(best, score)
            return best
        else:
            best = math.inf
            for r in range(BOARD_ROWS):
                for c in range(BOARD_COLS):
                    if board[r][c] == '':
                        board[r][c] = 'X'
                        score = minimax(board, depth + 1, True)
                        board[r][c] = ''
                        best = min(best, score)
            return best

    def ai_move(board):
        # 30% случайный ход
        if random.random() < 0.3:
            empties = [(r, c) for r in range(BOARD_ROWS) for c in range(BOARD_COLS) if board[r][c] == '']
            if empties:
                r, c = random.choice(empties)
                board[r][c] = 'O'
        else:
            best_score = -math.inf
            best_move = None
            for r in range(BOARD_ROWS):
                for c in range(BOARD_COLS):
                    if board[r][c] == '':
                        board[r][c] = 'O'
                        score = minimax(board, 0, False)
                        board[r][c] = ''
                        if score > best_score:
                            best_score = score
                            best_move = (r, c)
            if best_move:
                board[best_move[0]][best_move[1]] = 'O'

    def play_one_round():
        nonlocal screen
        update_sizes()
        board = [['' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
        game_over = False
        player_turn = True

        while True:
            draw_board()
            draw_figures(board)
            pygame.display.update()

            if game_over:
                pygame.time.delay(1000)
                # возврат True = игрок выиграл или ничья, False = проигрыш
                if check_win(board, 'X') or (not check_win(board, 'O') and is_board_full(board)):
                    return True
                return False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if screen_manager.is_fullscreen:
                            screen = screen_manager.toggle_fullscreen()
                            update_sizes()
                        else:
                            return "exit"
                    elif event.key == pygame.K_F11:
                        screen = screen_manager.toggle_fullscreen()
                        update_sizes()

                if player_turn and event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    row = (my - offset_y) // SQUARE_SIZE
                    col = (mx - offset_x) // SQUARE_SIZE
                    if 0 <= row < BOARD_ROWS and 0 <= col < BOARD_COLS and board[row][col] == '':
                        board[row][col] = 'X'
                        if check_win(board, 'X'):
                            game_over = True
                        else:
                            player_turn = False

            if not player_turn and not game_over:
                pygame.time.delay(300)
                ai_move(board)
                if check_win(board, 'O'):
                    game_over = True
                player_turn = True

            if is_board_full(board) and not game_over:
                game_over = True

    # — Основная логика: три раунда —
    wins = 0
    for _ in range(3):
        res = play_one_round()
        if res == "exit":
            return False
        if res:
            wins += 1

    # Показ результата поверх фонового изображения
    draw_background()
    if wins == 0:
        show_message(screen, "Вы проиграли все раунды", "На вас напали обезьяны!", color=(200, 0, 0))
        return False
    elif wins == 1:
        inventory.add("ветки")
        show_message(screen, "Вы выиграли один раунд", "Получены ветки для костра")
    elif wins == 2:
        inventory.add("жильё")
        show_message(screen, "Вы выиграли два раунда", "Построено жильё из веток")
    else:
        inventory.add("фрукты")
        show_message(screen, "Вы выиграли все раунды", "Обезьяны угостили вас фруктами!")

    show_victory_sequence(screen, victory_imgs)
    return True


def show_victory_sequence(screen, imgs):
    screen_width, screen_height = screen.get_size()
    fade_surface = pygame.Surface((screen_width, screen_height))
    fade_surface.fill((0, 0, 0))

    for img in imgs:
        scaled_img = pygame.transform.scale(img, (screen_width, screen_height))
        # fade-in
        for alpha in range(0, 256, 15):
            screen.blit(scaled_img, (0, 0))
            fade_surface.set_alpha(255 - alpha)
            screen.blit(fade_surface, (0, 0))
            pygame.display.flip()
            pygame.time.delay(30)

        # ждём ввода для перехода
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                    waiting = False

        # fade-out
        for alpha in range(0, 256, 15):
            screen.blit(scaled_img, (0, 0))
            fade_surface.set_alpha(alpha)
            screen.blit(fade_surface, (0, 0))
            pygame.display.flip()
            pygame.time.delay(30)
'''

'''
все хорошо, но решили переделать экраны в конце(экраны результатов).......

import pygame
import random
import math
from game1.mini_games.common.ui import show_message

BOARD_ROWS = 3
BOARD_COLS = 3
LINE_WIDTH = 4
SPACE = 20

BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)  # не используется, но оставлю для справки
CROSS_COLOR = (84, 84, 84)      # тоже для справки

def tictactoe_game(screen, inventory, screen_manager, victory_imgs):
    WIDTH, HEIGHT = screen.get_size()
    SQUARE_SIZE = 0
    offset_x = 0
    offset_y = 0

    # Загрузка изображений крестика и нолика
    x_image = pygame.image.load("C:/Users/bel31/PycharmProjects/pythonProject/MysteryIsland/icons/x_img.png").convert_alpha()
    o_image = pygame.image.load("C:/Users/bel31/PycharmProjects/pythonProject/MysteryIsland/icons/o_img.png").convert_alpha()

    # Загрузка фонового изображения
    background_image = pygame.image.load("C:/Users/bel31/PycharmProjects/pythonProject/MysteryIsland/icons/screen_tictactoe.png").convert()

    def update_sizes():
        nonlocal WIDTH, HEIGHT, SQUARE_SIZE, offset_x, offset_y
        WIDTH, HEIGHT = screen.get_size()
        SQUARE_SIZE = min(WIDTH, HEIGHT) // 4
        total_board_width = SQUARE_SIZE * BOARD_COLS
        total_board_height = SQUARE_SIZE * BOARD_ROWS
        offset_x = (WIDTH - total_board_width) // 2
        offset_y = (HEIGHT - total_board_height) // 2

    def draw_board():
        # Вместо заливки цветом отрисовываем фон
        scaled_bg = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
        screen.blit(scaled_bg, (0, 0))

        line_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        transparent_color = (*LINE_COLOR, 0)  # прозрачность линий

        for i in range(1, BOARD_ROWS):
            pygame.draw.line(line_surface, transparent_color,
                             (offset_x, offset_y + i * SQUARE_SIZE),
                             (offset_x + SQUARE_SIZE * BOARD_COLS, offset_y + i * SQUARE_SIZE),
                             LINE_WIDTH)
            pygame.draw.line(line_surface, transparent_color,
                             (offset_x + i * SQUARE_SIZE, offset_y),
                             (offset_x + i * SQUARE_SIZE, offset_y + SQUARE_SIZE * BOARD_ROWS),
                             LINE_WIDTH)

        screen.blit(line_surface, (0, 0))


    def draw_figures(board):
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                x = offset_x + col * SQUARE_SIZE
                y = offset_y + row * SQUARE_SIZE
                if board[row][col] == 'O':
                    scaled_o = pygame.transform.smoothscale(o_image, (SQUARE_SIZE, SQUARE_SIZE))
                    screen.blit(scaled_o, (x, y))
                elif board[row][col] == 'X':
                    scaled_x = pygame.transform.smoothscale(x_image, (SQUARE_SIZE, SQUARE_SIZE))
                    screen.blit(scaled_x, (x, y))

    def check_win(board, player):
        for row in board:
            if all(cell == player for cell in row):
                return True
        for col in range(BOARD_COLS):
            if all(board[row][col] == player for row in range(BOARD_ROWS)):
                return True
        if all(board[i][i] == player for i in range(BOARD_ROWS)):
            return True
        if all(board[i][BOARD_COLS - 1 - i] == player for i in range(BOARD_ROWS)):
            return True
        return False

    def is_board_full(board):
        return all(board[r][c] != '' for r in range(BOARD_ROWS) for c in range(BOARD_COLS))

    def minimax(board, depth, is_maximizing):
        if check_win(board, 'O'): return 1
        if check_win(board, 'X'): return -1
        if is_board_full(board): return 0

        if is_maximizing:
            best = -math.inf
            for r in range(BOARD_ROWS):
                for c in range(BOARD_COLS):
                    if board[r][c] == '':
                        board[r][c] = 'O'
                        score = minimax(board, depth + 1, False)
                        board[r][c] = ''
                        best = max(best, score)
            return best
        else:
            best = math.inf
            for r in range(BOARD_ROWS):
                for c in range(BOARD_COLS):
                    if board[r][c] == '':
                        board[r][c] = 'X'
                        score = minimax(board, depth + 1, True)
                        board[r][c] = ''
                        best = min(best, score)
            return best

    def ai_move(board):
        if random.random() < 0.3:
            empty = [(r, c) for r in range(BOARD_ROWS) for c in range(BOARD_COLS) if board[r][c] == '']
            if empty:
                r, c = random.choice(empty)
                board[r][c] = 'O'
        else:
            best_score = -math.inf
            move = None
            for r in range(BOARD_ROWS):
                for c in range(BOARD_COLS):
                    if board[r][c] == '':
                        board[r][c] = 'O'
                        score = minimax(board, 0, False)
                        board[r][c] = ''
                        if score > best_score:
                            best_score = score
                            move = (r, c)
            if move:
                board[move[0]][move[1]] = 'O'

    def play_one_round():
        nonlocal screen
        update_sizes()
        board = [['' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
        game_over = False
        player_turn = True

        while True:
            draw_board()
            draw_figures(board)
            pygame.display.update()

            if game_over:
                pygame.time.delay(1000)
                if check_win(board, 'X') or (not check_win(board, 'O') and is_board_full(board)):
                    return True
                else:
                    return False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if screen_manager.is_fullscreen:
                            screen = screen_manager.toggle_fullscreen()
                            update_sizes()
                        else:
                            return "exit"
                    elif event.key == pygame.K_F11:
                        screen = screen_manager.toggle_fullscreen()
                        update_sizes()

                if player_turn and event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    row = (y - offset_y) // SQUARE_SIZE
                    col = (x - offset_x) // SQUARE_SIZE
                    if 0 <= row < BOARD_ROWS and 0 <= col < BOARD_COLS:
                        if board[row][col] == '':
                            board[row][col] = 'X'
                            if check_win(board, 'X'):
                                game_over = True
                            else:
                                player_turn = False

            if not player_turn and not game_over:
                pygame.time.delay(300)
                ai_move(board)
                if check_win(board, 'O'):
                    game_over = True
                player_turn = True

            if is_board_full(board) and not game_over:
                game_over = True

    # --- Основная логика 3 попыток ---
    wins = 0
    for i in range(3):
        result = play_one_round()
        if result == "exit":
            return False
        elif result:
            wins += 1

    if wins == 0:
        show_message(screen, "Вы проиграли все раунды", "На вас напали обезьяны!", color=(200, 0, 0))
        return False
    elif wins == 1:
        inventory.add("ветки")
        show_message(screen, "Вы выиграли один раунд", "Получены ветки для костра")
    elif wins == 2:
        inventory.add("жильё")
        show_message(screen, "Вы выиграли два раунда", "Построено жильё из веток")
    else:
        inventory.add("фрукты")
        show_message(screen, "Вы выиграли все раунды", "Обезьяны угостили вас фруктами!")

    show_victory_sequence(screen, victory_imgs)
    return True


def show_victory_sequence(screen, imgs):
    screen_width, screen_height = screen.get_size()
    fade_surface = pygame.Surface((screen_width, screen_height))
    fade_surface.fill((0, 0, 0))

    for img in imgs:
        scaled_img = pygame.transform.scale(img, (screen_width, screen_height))
        # fade-in
        for alpha in range(0, 256, 15):
            screen.blit(scaled_img, (0, 0))
            fade_surface.set_alpha(255 - alpha)
            screen.blit(fade_surface, (0, 0))
            pygame.display.flip()
            pygame.time.delay(30)

        # ждём нажатия клавиши или мыши для перехода к следующему изображению
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    waiting = False

        # fade-out
        for alpha in range(0, 256, 15):
            screen.blit(scaled_img, (0, 0))
            fade_surface.set_alpha(alpha)
            screen.blit(fade_surface, (0, 0))
            pygame.display.flip()
            pygame.time.delay(30)

'''

'''import pygame
import random
import math
from game1.mini_games.common.ui import show_message

BOARD_ROWS = 3
BOARD_COLS = 3
LINE_WIDTH = 4
CIRCLE_WIDTH = 10
CROSS_WIDTH = 15
SPACE = 20

BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (84, 84, 84)

def tictactoe_game(screen, inventory, screen_manager, victory_imgs):
    WIDTH, HEIGHT = screen.get_size()
    SQUARE_SIZE = 0
    offset_x = 0
    offset_y = 0
    def update_sizes():
        nonlocal WIDTH, HEIGHT, SQUARE_SIZE, offset_x, offset_y
        WIDTH, HEIGHT = screen.get_size()
        SQUARE_SIZE = min(WIDTH, HEIGHT) // 4  # уменьшенный размер
        total_board_width = SQUARE_SIZE * BOARD_COLS
        total_board_height = SQUARE_SIZE * BOARD_ROWS
        offset_x = (WIDTH - total_board_width) // 2
        offset_y = (HEIGHT - total_board_height) // 2

    def draw_board():
        screen.fill(BG_COLOR)
        for i in range(1, BOARD_ROWS):
            pygame.draw.line(screen, LINE_COLOR,
                             (offset_x, offset_y + i * SQUARE_SIZE),
                             (offset_x + SQUARE_SIZE * BOARD_COLS, offset_y + i * SQUARE_SIZE),
                             LINE_WIDTH)
            pygame.draw.line(screen, LINE_COLOR,
                             (offset_x + i * SQUARE_SIZE, offset_y),
                             (offset_x + i * SQUARE_SIZE, offset_y + SQUARE_SIZE * BOARD_ROWS),
                             LINE_WIDTH)

    def draw_figures(board):
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                center = (offset_x + col * SQUARE_SIZE + SQUARE_SIZE // 2,
                          offset_y + row * SQUARE_SIZE + SQUARE_SIZE // 2)
                if board[row][col] == 'O':
                    pygame.draw.circle(screen, CIRCLE_COLOR, center, SQUARE_SIZE // 3, CIRCLE_WIDTH)
                elif board[row][col] == 'X':
                    start1 = (offset_x + col * SQUARE_SIZE + SPACE, offset_y + row * SQUARE_SIZE + SPACE)
                    end1 = (offset_x + col * SQUARE_SIZE + SQUARE_SIZE - SPACE,
                            offset_y + row * SQUARE_SIZE + SQUARE_SIZE - SPACE)
                    start2 = (offset_x + col * SQUARE_SIZE + SPACE,
                              offset_y + row * SQUARE_SIZE + SQUARE_SIZE - SPACE)
                    end2 = (offset_x + col * SQUARE_SIZE + SQUARE_SIZE - SPACE,
                            offset_y + row * SQUARE_SIZE + SPACE)
                    pygame.draw.line(screen, CROSS_COLOR, start1, end1, CROSS_WIDTH)
                    pygame.draw.line(screen, CROSS_COLOR, start2, end2, CROSS_WIDTH)

    def check_win(board, player):
        for row in board:
            if all(cell == player for cell in row):
                return True
        for col in range(BOARD_COLS):
            if all(board[row][col] == player for row in range(BOARD_ROWS)):
                return True
        if all(board[i][i] == player for i in range(BOARD_ROWS)):
            return True
        if all(board[i][BOARD_COLS - 1 - i] == player for i in range(BOARD_ROWS)):
            return True
        return False

    def is_board_full(board):
        return all(board[r][c] != '' for r in range(BOARD_ROWS) for c in range(BOARD_COLS))

    def minimax(board, depth, is_maximizing):
        if check_win(board, 'O'): return 1
        if check_win(board, 'X'): return -1
        if is_board_full(board): return 0

        if is_maximizing:
            best = -math.inf
            for r in range(BOARD_ROWS):
                for c in range(BOARD_COLS):
                    if board[r][c] == '':
                        board[r][c] = 'O'
                        score = minimax(board, depth + 1, False)
                        board[r][c] = ''
                        best = max(best, score)
            return best
        else:
            best = math.inf
            for r in range(BOARD_ROWS):
                for c in range(BOARD_COLS):
                    if board[r][c] == '':
                        board[r][c] = 'X'
                        score = minimax(board, depth + 1, True)
                        board[r][c] = ''
                        best = min(best, score)
            return best

    def ai_move(board):
        if random.random() < 0.3:
            empty = [(r, c) for r in range(BOARD_ROWS) for c in range(BOARD_COLS) if board[r][c] == '']
            if empty:
                r, c = random.choice(empty)
                board[r][c] = 'O'
        else:
            best_score = -math.inf
            move = None
            for r in range(BOARD_ROWS):
                for c in range(BOARD_COLS):
                    if board[r][c] == '':
                        board[r][c] = 'O'
                        score = minimax(board, 0, False)
                        board[r][c] = ''
                        if score > best_score:
                            best_score = score
                            move = (r, c)
            if move:
                board[move[0]][move[1]] = 'O'

    def play_one_round():
        nonlocal screen
        update_sizes()
        board = [['' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
        game_over = False
        player_turn = True

        while True:
            draw_board()
            draw_figures(board)
            pygame.display.update()

            if game_over:
                pygame.time.delay(1000)
                if check_win(board, 'X') or (not check_win(board, 'O') and is_board_full(board)):
                    return True
                else:
                    return False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if screen_manager.is_fullscreen:
                            screen = screen_manager.toggle_fullscreen()
                            update_sizes()
                        else:
                            return "exit"
                    elif event.key == pygame.K_F11:
                        screen = screen_manager.toggle_fullscreen()
                        update_sizes()

                if player_turn and event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    row = (y - offset_y) // SQUARE_SIZE
                    col = (x - offset_x) // SQUARE_SIZE
                    if 0 <= row < BOARD_ROWS and 0 <= col < BOARD_COLS:
                        if board[row][col] == '':
                            board[row][col] = 'X'
                            if check_win(board, 'X'):
                                game_over = True
                            else:
                                player_turn = False

            if not player_turn and not game_over:
                pygame.time.delay(300)
                ai_move(board)
                if check_win(board, 'O'):
                    game_over = True
                player_turn = True

            if is_board_full(board) and not game_over:
                game_over = True

    # --- Основная логика 3 попыток ---
    wins = 0
    for i in range(3):
        result = play_one_round()
        if result == "exit":
            return False
        elif result:
            wins += 1

    if wins == 0:
        show_message(screen, "Вы проиграли все раунды", "На вас напали обезьяны!", color=(200, 0, 0))
        return False
    elif wins == 1:
        inventory.add("ветки")
        show_message(screen, "Вы выиграли один раунд", "Получены ветки для костра")
    elif wins == 2:
        inventory.add("жильё")
        show_message(screen, "Вы выиграли два раунда", "Построено жильё из веток")
    else:
        inventory.add("фрукты")
        show_message(screen, "Вы выиграли все раунды", "Обезьяны угостили вас фруктами!")

    show_victory_sequence(screen, victory_imgs)
    return True


def show_victory_sequence(screen, imgs):
    screen_width, screen_height = screen.get_size()
    fade_surface = pygame.Surface((screen_width, screen_height))
    fade_surface.fill((0, 0, 0))

    for img in imgs:
        scaled_img = pygame.transform.scale(img, (screen_width, screen_height))
        # fade-in
        for alpha in range(0, 256, 15):
            screen.blit(scaled_img, (0, 0))
            fade_surface.set_alpha(255 - alpha)
            screen.blit(fade_surface, (0, 0))
            pygame.display.flip()
            pygame.time.delay(30)

        # ждём нажатия клавиши или мыши для перехода к следующему изображению
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    waiting = False

        # fade-out
        for alpha in range(0, 256, 15):
            screen.blit(scaled_img, (0, 0))
            fade_surface.set_alpha(alpha)
            screen.blit(fade_surface, (0, 0))
            pygame.display.flip()
            pygame.time.delay(30)
'''
'''
полностью готова но с одним раундом
import pygame
import sys
import random
import math

BOARD_ROWS = 3
BOARD_COLS = 3
LINE_WIDTH = 4
CIRCLE_WIDTH = 10
CROSS_WIDTH = 15
SPACE = 20

BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (84, 84, 84)


def tictactoe_game(screen, inventory, screen_manager):
    WIDTH, HEIGHT = screen.get_size()
    SQUARE_SIZE = 0
    offset_x = 0
    offset_y = 0

    def update_sizes():
        nonlocal WIDTH, HEIGHT, SQUARE_SIZE, offset_x, offset_y
        WIDTH, HEIGHT = screen.get_size()
        margin_ratio = 0.1  # 10% отступы по краям
        max_board_width = WIDTH * (1 - margin_ratio * 2)
        max_board_height = HEIGHT * (1 - margin_ratio * 2)

        square_w = max_board_width / BOARD_COLS
        square_h = max_board_height / BOARD_ROWS
        SQUARE_SIZE = int(min(square_w, square_h))

        offset_x = (WIDTH - SQUARE_SIZE * BOARD_COLS) // 2
        offset_y = (HEIGHT - SQUARE_SIZE * BOARD_ROWS) // 2

    update_sizes()
    

    board = [['' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    game_over = False
    player_turn = True

    def draw_board():
        screen.fill(BG_COLOR)
        # Рисуем линии с учётом смещений
        for i in range(1, BOARD_ROWS):
            pygame.draw.line(screen, LINE_COLOR,
                             (offset_x, offset_y + i * SQUARE_SIZE),
                             (offset_x + SQUARE_SIZE * BOARD_COLS, offset_y + i * SQUARE_SIZE),
                             LINE_WIDTH)
            pygame.draw.line(screen, LINE_COLOR,
                             (offset_x + i * SQUARE_SIZE, offset_y),
                             (offset_x + i * SQUARE_SIZE, offset_y + SQUARE_SIZE * BOARD_ROWS),
                             LINE_WIDTH)

    def draw_figures():
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                center = (offset_x + col * SQUARE_SIZE + SQUARE_SIZE // 2,
                          offset_y + row * SQUARE_SIZE + SQUARE_SIZE // 2)
                if board[row][col] == 'O':
                    pygame.draw.circle(screen, CIRCLE_COLOR, center, SQUARE_SIZE // 3, CIRCLE_WIDTH)
                elif board[row][col] == 'X':
                    start1 = (offset_x + col * SQUARE_SIZE + SPACE, offset_y + row * SQUARE_SIZE + SPACE)
                    end1 = (offset_x + col * SQUARE_SIZE + SQUARE_SIZE - SPACE,
                            offset_y + row * SQUARE_SIZE + SQUARE_SIZE - SPACE)
                    start2 = (offset_x + col * SQUARE_SIZE + SPACE,
                              offset_y + row * SQUARE_SIZE + SQUARE_SIZE - SPACE)
                    end2 = (offset_x + col * SQUARE_SIZE + SQUARE_SIZE - SPACE,
                            offset_y + row * SQUARE_SIZE + SPACE)
                    pygame.draw.line(screen, CROSS_COLOR, start1, end1, CROSS_WIDTH)
                    pygame.draw.line(screen, CROSS_COLOR, start2, end2, CROSS_WIDTH)

    def check_win(player):
        for row in board:
            if all(cell == player for cell in row):
                return True
        for col in range(BOARD_COLS):
            if all(board[row][col] == player for row in range(BOARD_ROWS)):
                return True
        if all(board[i][i] == player for i in range(BOARD_ROWS)):
            return True
        if all(board[i][BOARD_COLS - 1 - i] == player for i in range(BOARD_ROWS)):
            return True
        return False

    def is_board_full():
        return all(board[r][c] != '' for r in range(BOARD_ROWS) for c in range(BOARD_COLS))

    def minimax(depth, is_maximizing):
        if check_win('O'):
            return 1
        if check_win('X'):
            return -1
        if is_board_full():
            return 0

        if is_maximizing:
            best = -math.inf
            for r in range(BOARD_ROWS):
                for c in range(BOARD_COLS):
                    if board[r][c] == '':
                        board[r][c] = 'O'
                        score = minimax(depth + 1, False)
                        board[r][c] = ''
                        best = max(best, score)
            return best
        else:
            best = math.inf
            for r in range(BOARD_ROWS):
                for c in range(BOARD_COLS):
                    if board[r][c] == '':
                        board[r][c] = 'X'
                        score = minimax(depth + 1, True)
                        board[r][c] = ''
                        best = min(best, score)
            return best

    def ai_move():
        if random.random() < 0.3:  # 30% шанс сделать случайный ход
            empty = [(r, c) for r in range(BOARD_ROWS) for c in range(BOARD_COLS) if board[r][c] == '']
            if empty:
                r, c = random.choice(empty)
                board[r][c] = 'O'
        else:
            best_score = -math.inf
            move = None
            for r in range(BOARD_ROWS):
                for c in range(BOARD_COLS):
                    if board[r][c] == '':
                        board[r][c] = 'O'
                        score = minimax(0, False)
                        board[r][c] = ''
                        if score > best_score:
                            best_score = score
                            move = (r, c)
            if move:
                board[move[0]][move[1]] = 'O'


    draw_board()
    pygame.display.update()

    clock = pygame.time.Clock()

    while True:
            draw_board()
            draw_figures()
            pygame.display.update()

            if game_over:
                pygame.time.delay(1500)
                return True  # Возврат в main.py

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False

                if event.type == pygame.KEYDOWN:
                    # Управление полноэкранным режимом с пересчётом размеров и смещений
                    if event.key == pygame.K_F11:
                        screen = screen_manager.toggle_fullscreen()
                        update_sizes()
                        

                    elif event.key == pygame.K_ESCAPE:
                        if screen_manager.is_fullscreen:
                            screen = screen_manager.toggle_fullscreen()
                            update_sizes()
                            
                        else:
                            return False

                if player_turn and event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    # Корректируем координаты с учетом смещения
                    x_rel = x - offset_x
                    y_rel = y - offset_y
                    if 0 <= x_rel < SQUARE_SIZE * BOARD_COLS and 0 <= y_rel < SQUARE_SIZE * BOARD_ROWS:
                        row = y_rel // SQUARE_SIZE
                        col = x_rel // SQUARE_SIZE

                        if board[row][col] == '':
                            board[row][col] = 'X'
                            if check_win('X'):
                                game_over = True
                            else:
                                player_turn = False

            if not player_turn and not game_over:
                pygame.time.delay(300)
                ai_move()
                if check_win('O'):
                    game_over = True
                player_turn = True

            if is_board_full() and not game_over:
                game_over = True
'''
'''import pygame
import sys
import random
import math

BOARD_ROWS = 3
BOARD_COLS = 3
LINE_WIDTH = 4
CIRCLE_WIDTH = 10
CROSS_WIDTH = 15
SPACE = 20

BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (84, 84, 84)


def tictactoe_game(screen, inventory, screen_manager):
    WIDTH, HEIGHT = screen.get_size()
    SQUARE_SIZE = WIDTH // BOARD_COLS
    board = [['' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    game_over = False
    player_turn = True

    def draw_board():
        screen.fill(BG_COLOR)
        for i in range(1, BOARD_ROWS):
            pygame.draw.line(screen, LINE_COLOR, (0, i * SQUARE_SIZE), (WIDTH, i * SQUARE_SIZE), LINE_WIDTH)
            pygame.draw.line(screen, LINE_COLOR, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

    def draw_figures():
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                center = (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2)
                if board[row][col] == 'O':
                    pygame.draw.circle(screen, CIRCLE_COLOR, center, SQUARE_SIZE // 3, CIRCLE_WIDTH)
                elif board[row][col] == 'X':
                    start1 = (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE)
                    end1 = (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE)
                    start2 = (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE)
                    end2 = (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE)
                    pygame.draw.line(screen, CROSS_COLOR, start1, end1, CROSS_WIDTH)
                    pygame.draw.line(screen, CROSS_COLOR, start2, end2, CROSS_WIDTH)

    def check_win(player):
        for row in board:
            if all(cell == player for cell in row):
                return True
        for col in range(BOARD_COLS):
            if all(board[row][col] == player for row in range(BOARD_ROWS)):
                return True
        if all(board[i][i] == player for i in range(BOARD_ROWS)):
            return True
        if all(board[i][BOARD_COLS - 1 - i] == player for i in range(BOARD_ROWS)):
            return True
        return False

    def is_board_full():
        return all(board[r][c] != '' for r in range(BOARD_ROWS) for c in range(BOARD_COLS))

    def minimax(depth, is_maximizing):
        if check_win('O'):
            return 1
        if check_win('X'):
            return -1
        if is_board_full():
            return 0

        if is_maximizing:
            best = -math.inf
            for r in range(BOARD_ROWS):
                for c in range(BOARD_COLS):
                    if board[r][c] == '':
                        board[r][c] = 'O'
                        score = minimax(depth + 1, False)
                        board[r][c] = ''
                        best = max(best, score)
            return best
        else:
            best = math.inf
            for r in range(BOARD_ROWS):
                for c in range(BOARD_COLS):
                    if board[r][c] == '':
                        board[r][c] = 'X'
                        score = minimax(depth + 1, True)
                        board[r][c] = ''
                        best = min(best, score)
            return best

    def ai_move():
        if random.random() < 0.3:  # 30% шанс сделать случайный ход
            empty = [(r, c) for r in range(BOARD_ROWS) for c in range(BOARD_COLS) if board[r][c] == '']
            if empty:
                r, c = random.choice(empty)
                board[r][c] = 'O'
        else:
            best_score = -math.inf
            move = None
            for r in range(BOARD_ROWS):
                for c in range(BOARD_COLS):
                    if board[r][c] == '':
                        board[r][c] = 'O'
                        score = minimax(0, False)
                        board[r][c] = ''
                        if score > best_score:
                            best_score = score
                            move = (r, c)
            if move:
                board[move[0]][move[1]] = 'O'

    draw_board()
    pygame.display.update()

    clock = pygame.time.Clock()

    while True:
        draw_board()
        draw_figures()
        pygame.display.update()

        if game_over:
            pygame.time.delay(1500)
            return True  # Возврат в main.py

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                # Управление полноэкранным режимом
                if event.key == pygame.K_F11:
                    screen = screen_manager.toggle_fullscreen()
                elif event.key == pygame.K_ESCAPE:
                    if screen_manager.is_fullscreen:
                        screen = screen_manager.toggle_fullscreen()
                    else:
                        return False

            if player_turn and event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                row = y // SQUARE_SIZE
                col = x // SQUARE_SIZE

                if board[row][col] == '':
                    board[row][col] = 'X'
                    if check_win('X'):
                        game_over = True
                    else:
                        player_turn = False

        if not player_turn and not game_over:
            pygame.time.delay(300)
            ai_move()
            if check_win('O'):
                game_over = True
            player_turn = True
        if is_board_full() and not game_over:
            game_over = True
'''
'''
глупые крустики нолики
import pygame, random
from game1.mini_games.common.ui import show_message

def check_winner(board, player):
    wins = [(0,1,2),(3,4,5),(6,7,8), (0,3,6),(1,4,7),(2,5,8), (0,4,8),(2,4,6)]
    for a,b,c in wins:
        if board[a] == board[b] == board[c] == player:
            return True
    return False

def tictactoe_game(screen, inventory):
    wins = 0
    attempts = 3
    font = pygame.font.SysFont("arial", 60)

    for attempt in range(attempts):
        board = [""] * 9
        current = "X"
        game_over = False

        while not game_over:
            screen.fill((255, 255, 255))
            for i in range(9):
                x, y = (i % 3) * 100 + 250, (i // 3) * 100 + 150
                pygame.draw.rect(screen, (200, 200, 200), (x, y, 90, 90), 2)
                if board[i] != "":
                    txt = font.render(board[i], True, (0, 0, 0))
                    screen.blit(txt, (x + 25, y + 10))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); exit()
                if event.type == pygame.MOUSEBUTTONDOWN and current == "X":
                    mx, my = pygame.mouse.get_pos()
                    col, row = (mx - 250) // 100, (my - 150) // 100
                    if 0 <= col < 3 and 0 <= row < 3:
                        idx = row * 3 + col
                        if board[idx] == "":
                            board[idx] = "X"
                            if check_winner(board, "X"):
                                wins += 1
                                game_over = True
                            elif "" not in board:
                                game_over = True
                            else:
                                current = "O"

            if current == "O" and not game_over:
                empty = [i for i, val in enumerate(board) if val == ""]
                if empty:
                    board[random.choice(empty)] = "O"
                    if check_winner(board, "O"):
                        game_over = True
                    elif "" not in board:
                        game_over = True
                    else:
                        current = "X"

    if wins == 0:
        return False
    elif wins == 1:
        inventory.add("ветки")
        show_message(screen, "Вы победили 1 раз", "Получены ветки")
        return True
    elif wins == 2:
        inventory.add("ветки для жилья")
        show_message(screen, "Вы победили 2 раза", "Получены ветки для жилья")
        return True
    else:
        inventory.add("фрукты")
        show_message(screen, "Все победы!", "Получены фрукты")
        return True'''
'''
import pygame
import random

WIDTH, HEIGHT = 800, 600
#FONT = pygame.font.SysFont("arial", 48)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LINE_COLOR = (28, 170, 156)

# Размеры клеток и линии
CELL_SIZE = 150
LINE_WIDTH = 10

# Шаблон для победных комбинаций
WINNING_COMBINATIONS = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]

# Функция для отрисовки игрового поля
def draw_grid(screen):
    for x in range(1, 3):
        pygame.draw.line(screen, LINE_COLOR, (x * CELL_SIZE, 0), (x * CELL_SIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, x * CELL_SIZE), (WIDTH, x * CELL_SIZE), LINE_WIDTH)

# Функция для отрисовки фишек
def draw_marks(screen, board):
    for i in range(9):
        row = i // 3
        col = i % 3
        if board[i] == 'X':
            pygame.draw.line(screen, WHITE, (col * CELL_SIZE + 50, row * CELL_SIZE + 50),
                             (col * CELL_SIZE + 100, row * CELL_SIZE + 100), 5)
            pygame.draw.line(screen, WHITE, (col * CELL_SIZE + 50, row * CELL_SIZE + 100),
                             (col * CELL_SIZE + 100, row * CELL_SIZE + 50), 5)
        elif board[i] == 'O':
            pygame.draw.circle(screen, WHITE, (col * CELL_SIZE + 75, row * CELL_SIZE + 75), 50, 5)

# Функция для проверки победы
def check_win(board):
    for combo in WINNING_COMBINATIONS:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] != '':
            return True
    return False

# Главная логика игры
def tictactoe_game(screen, inventory):
    board = [''] * 9
    current_player = 'X'
    game_over = False
    winner = None

    while not game_over:
        screen.fill(BLACK)
        draw_grid(screen)
        draw_marks(screen, board)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                row = y // CELL_SIZE
                col = x // CELL_SIZE
                index = row * 3 + col

                if board[index] == '':
                    board[index] = current_player
                    if check_win(board):
                        winner = current_player
                        game_over = True
                    current_player = 'O' if current_player == 'X' else 'X'

        pygame.time.delay(100)

    if winner == 'X':
        inventory.add_item('Ветки для костра!')
    elif winner == 'O':
        inventory.add_item('Ветки и жильё!')
    else:
        inventory.add_item('Фрукты!')

    return True'''