# MysteryIsland/mini_games/tictactoe.py
# tictactoe.py

import pygame
import random
import math


BOARD_ROWS = 3
BOARD_COLS = 3
LINE_WIDTH = 4


def tictactoe_game(screen, inventory, screen_manager):
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

    # Основная логика
    wins = 0
    for _ in range(3):
        res = play_one_round()
        if res == "exit":
            return False
        if res:
            wins += 1

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

    return True