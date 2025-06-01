# MysteryIsland/mini_games/match3_game.py
# match3.py
import pygame
import random
import pygame.transform
import time

TILE_SIZE = 64
WIDTH, HEIGHT = 8, 8
MAX_MOVES = 15
TARGET_BLUE = 18
FPS = 60

COLORS = [
    (51, 0, 102),
    (0, 102, 51),
    (0, 0, 255),
    (0, 102, 102),
    (0, 51, 102)
]
BLUE_INDEX = 2

BACKGROUND_IMAGE = pygame.image.load("../MysteryIsland/icons/screen_match3.PNG")
WATER_IMAGE = pygame.image.load("../MysteryIsland/icons/water_drop.png")
DEFEAT_IMAGE = pygame.image.load("../MysteryIsland/icons/defeatmatch3.png")

def match3_game(screen, inventory, screen_manager, victory_imgs):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)

    screen_width, screen_height = screen.get_size()
    bg_scaled = pygame.transform.scale(BACKGROUND_IMAGE, (screen_width, screen_height))

    board = [[random.randint(0, len(COLORS) - 1) for _ in range(WIDTH)] for _ in range(HEIGHT)]
    selected = None
    moves_left = MAX_MOVES
    blue_collected = 0
    game_over = False
    level_won = False
    defeat_screen_shown = False

    def draw_board(offset_x, offset_y):
        overlay = pygame.Surface((WIDTH * TILE_SIZE, HEIGHT * TILE_SIZE), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 0))
        screen.blit(overlay, (offset_x, offset_y))

        for y in range(HEIGHT):
            for x in range(WIDTH):
                cx = offset_x + x * TILE_SIZE + TILE_SIZE // 2
                cy = offset_y + y * TILE_SIZE + TILE_SIZE // 2

                if board[y][x] != -1:
                    if board[y][x] == BLUE_INDEX:
                        water_scaled = pygame.transform.scale(WATER_IMAGE, (TILE_SIZE - 8, TILE_SIZE - 8))
                        screen.blit(water_scaled, (cx - water_scaled.get_width() // 2, cy - water_scaled.get_height() // 2))
                    else:
                        size = TILE_SIZE - 20
                        rect_surface = pygame.Surface((size, size), pygame.SRCALPHA)
                        pygame.draw.rect(
                            rect_surface,
                            COLORS[board[y][x]],
                            (0, 0, size, size),
                            border_radius=12
                        )
                        rotated = pygame.transform.rotate(rect_surface, 45)
                        rect = rotated.get_rect(center=(cx, cy))
                        screen.blit(rotated, rect.topleft)

                if selected == (x, y):
                    pygame.draw.rect(screen, (255, 255, 255),
                                     pygame.Rect(offset_x + x * TILE_SIZE, offset_y + y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 3)

    def draw_ui(offset_x, offset_y):
        info_text = f"Капли: {blue_collected}/{TARGET_BLUE} | Ходы: {moves_left}"
        text = font.render(info_text, True, (255, 255, 255))
        screen.blit(text, (offset_x, offset_y - 40))

    def swap(x1, y1, x2, y2):
        board[y1][x1], board[y2][x2] = board[y2][x2], board[y1][x1]

    def find_matches():
        matched = [[False] * WIDTH for _ in range(HEIGHT)]
        for y in range(HEIGHT):
            for x in range(WIDTH - 2):
                if board[y][x] == board[y][x+1] == board[y][x+2] != -1:
                    matched[y][x] = matched[y][x+1] = matched[y][x+2] = True
        for x in range(WIDTH):
            for y in range(HEIGHT - 2):
                if board[y][x] == board[y+1][x] == board[y+2][x] != -1:
                    matched[y][x] = matched[y+1][x] = matched[y+2][x] = True
        return matched

    def remove_matches(matched):
        nonlocal blue_collected
        removed = False
        for y in range(HEIGHT):
            for x in range(WIDTH):
                if matched[y][x]:
                    if board[y][x] == BLUE_INDEX:
                        blue_collected += 1
                    board[y][x] = -1
                    removed = True
        return removed

    def drop_tiles():
        for x in range(WIDTH):
            for y in range(HEIGHT - 1, -1, -1):
                if board[y][x] == -1:
                    for k in range(y - 1, -1, -1):
                        if board[k][x] != -1:
                            board[y][x], board[k][x] = board[k][x], -1
                            break
                    else:
                        board[y][x] = random.randint(0, len(COLORS) - 1)

    running = True
    while running:
        clock.tick(FPS)
        screen_width, screen_height = screen.get_size()
        screen.blit(bg_scaled, (0, 0))

        offset_x = (screen_width - WIDTH * TILE_SIZE) // 2
        offset_y = (screen_height - HEIGHT * TILE_SIZE) // 2

        if not game_over:
            draw_board(offset_x, offset_y)
            draw_ui(offset_x, offset_y)
            pygame.display.flip()

            matched = find_matches()
            if any(any(row) for row in matched):
                pygame.time.delay(200)
                remove_matches(matched)
                drop_tiles()
                if blue_collected >= TARGET_BLUE:
                    level_won = True
                    game_over = True
                elif moves_left <= 0:
                    game_over = True
            elif moves_left <= 0:
                game_over = True

        else:
            if level_won:
                #show_victory_sequence(screen, victory_imgs)
                return True
            elif not defeat_screen_shown:
                defeat_scaled = pygame.transform.scale(DEFEAT_IMAGE, (screen_width, screen_height))
                screen.blit(defeat_scaled, (0, 0))
                pygame.display.flip()
                pygame.time.delay(10000)  # Показываем экран поражения 10 секунды
                return False
                defeat_screen_shown = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    screen = screen_manager.toggle_fullscreen()
                    screen_width, screen_height = screen.get_size()
                    bg_scaled = pygame.transform.scale(BACKGROUND_IMAGE, (screen_width, screen_height))
                elif event.key == pygame.K_ESCAPE:
                    if screen_manager.is_fullscreen:
                        screen = screen_manager.toggle_fullscreen()
                        screen_width, screen_height = screen.get_size()
                        bg_scaled = pygame.transform.scale(BACKGROUND_IMAGE, (screen_width, screen_height))
                    else:
                        pygame.quit()
                        return False

            elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mx, my = pygame.mouse.get_pos()
                if not (offset_x <= mx < offset_x + TILE_SIZE * WIDTH and offset_y <= my < offset_y + TILE_SIZE * HEIGHT):
                    continue
                x, y = (mx - offset_x) // TILE_SIZE, (my - offset_y) // TILE_SIZE
                if selected:
                    x0, y0 = selected
                    if abs(x - x0) + abs(y - y0) == 1:
                        swap(x0, y0, x, y)
                        matched = find_matches()
                        if any(any(row) for row in matched):
                            moves_left -= 1
                        else:
                            swap(x0, y0, x, y)
                        selected = None
                    else:
                        selected = (x, y)
                else:
                    selected = (x, y)
    return level_won

'''def show_victory_sequence(screen, imgs):
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

        # ждём нажатия клавиши или мыши
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
import pygame.transform
import time

TILE_SIZE = 64
WIDTH, HEIGHT = 8, 8
MAX_MOVES = 10
TARGET_BLUE = 18
FPS = 60

COLORS = [
    (51, 0, 102),  # Красный
    (0, 102, 51),  # Зелёный
    (0, 0, 255),  # Синий (цель)
    (0, 102, 102),  # Жёлтый
    (0, 51, 102)  # Розовый
]
BLUE_INDEX = 2

BACKGROUND_IMAGE = pygame.image.load("C:/Users/bel31/PycharmProjects/pythonProject/MysteryIsland/icons/screen_match3.PNG")
WATER_IMAGE = pygame.image.load("C:/Users/bel31/PycharmProjects/pythonProject/MysteryIsland/icons/water_drop.png")

def match3_game(screen, inventory, screen_manager, victory_imgs):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)

    # Подготовка фонового изображения под текущий размер экрана
    screen_width, screen_height = screen.get_size()
    bg_scaled = pygame.transform.scale(BACKGROUND_IMAGE, (screen_width, screen_height))

    board = [[random.randint(0, len(COLORS) - 1) for _ in range(WIDTH)] for _ in range(HEIGHT)]
    selected = None
    moves_left = MAX_MOVES
    blue_collected = 0
    game_over = False
    level_won = False

    def draw_board(offset_x, offset_y):
        overlay = pygame.Surface((WIDTH * TILE_SIZE, HEIGHT * TILE_SIZE), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 0))  # Полупрозрачный белый
        screen.blit(overlay, (offset_x, offset_y))

        for y in range(HEIGHT):
            for x in range(WIDTH):
                cx = offset_x + x * TILE_SIZE + TILE_SIZE // 2
                cy = offset_y + y * TILE_SIZE + TILE_SIZE // 2

                if board[y][x] != -1:
                    if board[y][x] == BLUE_INDEX:
                        water_scaled = pygame.transform.scale(WATER_IMAGE, (TILE_SIZE - 8, TILE_SIZE - 8))
                        screen.blit(water_scaled,
                                    (cx - water_scaled.get_width() // 2, cy - water_scaled.get_height() // 2))
                    else:
                        size = TILE_SIZE - 20
                        rect_surface = pygame.Surface((size, size), pygame.SRCALPHA)
                        pygame.draw.rect(
                            rect_surface,
                            COLORS[board[y][x]],
                            (0, 0, size, size),
                            border_radius=12
                        )
                        rotated = pygame.transform.rotate(rect_surface, 45)
                        rect = rotated.get_rect(center=(cx, cy))
                        screen.blit(rotated, rect.topleft)

                # Обводка для выделенной клетки
                if selected == (x, y):
                    pygame.draw.rect(screen, (255, 255, 255),
                                     pygame.Rect(offset_x + x * TILE_SIZE, offset_y + y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 3)

    def draw_ui(offset_x, offset_y):
        info_text = f"Капли: {blue_collected}/{TARGET_BLUE} | Ходы: {moves_left}"
        text = font.render(info_text, True, (255, 255, 255))
        screen.blit(text, (offset_x, offset_y - 40))

        if level_won:
            win_text = font.render("Уровень пройден!", True, (0, 255, 0))
            screen.blit(win_text, (offset_x + 200, offset_y + HEIGHT * TILE_SIZE + 10))
        elif game_over:
            lose_text = font.render("Ходы закончились!", True, (255, 100, 100))
            screen.blit(lose_text, (offset_x + 180, offset_y + HEIGHT * TILE_SIZE + 10))

    def swap(x1, y1, x2, y2):
        board[y1][x1], board[y2][x2] = board[y2][x2], board[y1][x1]

    def find_matches():
        matched = [[False]*WIDTH for _ in range(HEIGHT)]
        for y in range(HEIGHT):
            for x in range(WIDTH - 2):
                if board[y][x] == board[y][x+1] == board[y][x+2] != -1:
                    matched[y][x] = matched[y][x+1] = matched[y][x+2] = True
        for x in range(WIDTH):
            for y in range(HEIGHT - 2):
                if board[y][x] == board[y+1][x] == board[y+2][x] != -1:
                    matched[y][x] = matched[y+1][x] = matched[y+2][x] = True
        return matched

    def remove_matches(matched):
        nonlocal blue_collected
        removed = False
        for y in range(HEIGHT):
            for x in range(WIDTH):
                if matched[y][x]:
                    if board[y][x] == BLUE_INDEX:
                        blue_collected += 1
                    board[y][x] = -1
                    removed = True
        return removed

    def drop_tiles():
        for x in range(WIDTH):
            for y in range(HEIGHT - 1, -1, -1):
                if board[y][x] == -1:
                    for k in range(y - 1, -1, -1):
                        if board[k][x] != -1:
                            board[y][x], board[k][x] = board[k][x], -1
                            break
                    else:
                        board[y][x] = random.randint(0, len(COLORS) - 1)

    running = True
    while running:
        clock.tick(FPS)
        screen_width, screen_height = screen.get_size()
        screen.blit(bg_scaled, (0, 0))

        # Центрируем игровое поле
        offset_x = (screen_width - WIDTH * TILE_SIZE) // 2
        offset_y = (screen_height - HEIGHT * TILE_SIZE) // 2

        draw_board(offset_x, offset_y)
        draw_ui(offset_x, offset_y)

        pygame.display.flip()

        if not game_over and not level_won:
            matched = find_matches()
            if any(any(row) for row in matched):
                pygame.time.delay(200)
                remove_matches(matched)
                drop_tiles()
                if blue_collected >= TARGET_BLUE:
                    level_won = True
                    game_over = True
                elif moves_left <= 0:
                    game_over = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    screen = screen_manager.toggle_fullscreen()
                    screen_width, screen_height = screen.get_size()
                    bg_scaled = pygame.transform.scale(BACKGROUND_IMAGE, (screen_width, screen_height))
                elif event.key == pygame.K_ESCAPE:
                    if screen_manager.is_fullscreen:
                        screen = screen_manager.toggle_fullscreen()
                        screen_width, screen_height = screen.get_size()
                        bg_scaled = pygame.transform.scale(BACKGROUND_IMAGE, (screen_width, screen_height))
                    else:
                        pygame.quit()
                        return False
                elif game_over:
                    show_victory_sequence(screen, victory_imgs)
                    return level_won

            elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mx, my = pygame.mouse.get_pos()
                if not (
                        offset_x <= mx < offset_x + TILE_SIZE * WIDTH and offset_y <= my < offset_y + TILE_SIZE * HEIGHT):
                    continue
                x, y = (mx - offset_x) // TILE_SIZE, (my - offset_y) // TILE_SIZE
                if selected:
                    x0, y0 = selected
                    if abs(x - x0) + abs(y - y0) == 1:
                        swap(x0, y0, x, y)
                        matched = find_matches()
                        if any(any(row) for row in matched):
                            moves_left -= 1
                        else:
                            swap(x0, y0, x, y)
                        selected = None
                    else:
                        selected = (x, y)
                else:
                    selected = (x, y)
    return level_won

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
import pygame.transform


TILE_SIZE = 64
WIDTH, HEIGHT = 8, 8
SCREEN_WIDTH = TILE_SIZE * WIDTH
SCREEN_HEIGHT = TILE_SIZE * HEIGHT
MAX_MOVES = 20
TARGET_BLUE = 18
FPS = 60

COLORS = [
    (255, 0, 255),    # Красный
    (0, 0, 255),    # Зелёный
    (0, 0, 255),    # Синий (цель)
    (0, 255, 255),  # Жёлтый
    (127, 0, 255)   # Розовый
]
BLUE_INDEX = 2

BACKGROUND_IMAGE = pygame.image.load("C:/Users/bel31/PycharmProjects/pythonProject/MysteryIsland/icons/screen_match3.jpg")
BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (800, 600))

WATER_IMAGE = pygame.image.load("C:/Users/bel31/PycharmProjects/pythonProject/MysteryIsland/icons/water_drop.png")
WATER_IMAGE = pygame.transform.scale(WATER_IMAGE, (TILE_SIZE - 8, TILE_SIZE - 8))

def match3_game(screen, inventory):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)

    board = [[random.randint(0, len(COLORS) - 1) for _ in range(WIDTH)] for _ in range(HEIGHT)]
    selected = None
    moves_left = MAX_MOVES
    blue_collected = 0
    game_over = False
    level_won = False



    def draw_board():
        overlay = pygame.Surface((WIDTH * TILE_SIZE + 100, HEIGHT * TILE_SIZE + 30), pygame.SRCALPHA)
        overlay.fill((255, 255, 255, 55))  # Белый с альфа-каналом (180 из 255 — полупрозрачный)
        screen.blit(overlay, (100, 50))  # Те же координаты, что у поля
        for y in range(HEIGHT):
            for x in range(WIDTH):
                cx = x * TILE_SIZE + 100 + TILE_SIZE // 2
                cy = y * TILE_SIZE + 50 + TILE_SIZE // 2

                if board[y][x] != -1:
                    if board[y][x] == BLUE_INDEX:
                        screen.blit(WATER_IMAGE,
                                    (cx - WATER_IMAGE.get_width() // 2, cy - WATER_IMAGE.get_height() // 2))
                    else:
                        # Создаем поверхность для ромба
                        size = TILE_SIZE - 20
                        rect_surface = pygame.Surface((size, size), pygame.SRCALPHA)
                        pygame.draw.rect(
                            rect_surface,
                            COLORS[board[y][x]],
                            (0, 0, size, size),
                            border_radius=12
                        )

                        # Поворачиваем поверхность на 45 градусов
                        rotated = pygame.transform.rotate(rect_surface, 45)
                        rect = rotated.get_rect(center=(cx, cy))
                        screen.blit(rotated, rect.topleft)

    def draw_ui():
        info_text = f"Синих: {blue_collected}/{TARGET_BLUE} | Ходы: {moves_left}"
        text = font.render(info_text, True, (255, 255, 255))
        screen.blit(text, (100, 10))
        if level_won:
            win_text = font.render("Уровень пройден!", True, (0, 255, 0))
            screen.blit(win_text, (300, SCREEN_HEIGHT + 60))
        elif game_over:
            lose_text = font.render("Ходы закончились!", True, (255, 100, 100))
            screen.blit(lose_text, (280, SCREEN_HEIGHT + 60))

    def swap(x1, y1, x2, y2):
        board[y1][x1], board[y2][x2] = board[y2][x2], board[y1][x1]

    def find_matches():
        matched = [[False]*WIDTH for _ in range(HEIGHT)]
        for y in range(HEIGHT):
            for x in range(WIDTH - 2):
                if board[y][x] == board[y][x+1] == board[y][x+2] != -1:
                    matched[y][x] = matched[y][x+1] = matched[y][x+2] = True
        for x in range(WIDTH):
            for y in range(HEIGHT - 2):
                if board[y][x] == board[y+1][x] == board[y+2][x] != -1:
                    matched[y][x] = matched[y+1][x] = matched[y+2][x] = True
        return matched

    def remove_matches(matched):
        nonlocal blue_collected
        removed = False
        for y in range(HEIGHT):
            for x in range(WIDTH):
                if matched[y][x]:
                    if board[y][x] == BLUE_INDEX:
                        blue_collected += 1
                    board[y][x] = -1
                    removed = True
        return removed

    def drop_tiles():
        for x in range(WIDTH):
            for y in range(HEIGHT - 1, -1, -1):
                if board[y][x] == -1:
                    for k in range(y - 1, -1, -1):
                        if board[k][x] != -1:
                            board[y][x], board[k][x] = board[k][x], -1
                            break
                    else:
                        board[y][x] = random.randint(0, len(COLORS) - 1)

    running = True
    while running:
        clock.tick(FPS)
        screen.blit(BACKGROUND_IMAGE, (0, 0))
        draw_board()
        draw_ui()
        pygame.display.flip()

        if not game_over and not level_won:
            matched = find_matches()
            if any(any(row) for row in matched):
                pygame.time.delay(200)
                remove_matches(matched)
                drop_tiles()
                if blue_collected >= TARGET_BLUE:
                    level_won = True
                    game_over = True
                elif moves_left <= 0:
                    game_over = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            elif event.type == pygame.KEYDOWN:
                if game_over:
                    return level_won
            elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mx, my = pygame.mouse.get_pos()
                if not (100 <= mx < 100 + TILE_SIZE * WIDTH and 50 <= my < 50 + TILE_SIZE * HEIGHT):
                    continue
                x, y = (mx - 100) // TILE_SIZE, (my - 50) // TILE_SIZE
                if selected:
                    x0, y0 = selected
                    if abs(x - x0) + abs(y - y0) == 1:
                        swap(x0, y0, x, y)
                        matched = find_matches()
                        if any(any(row) for row in matched):
                            moves_left -= 1
                        else:
                            swap(x0, y0, x, y)
                        selected = None
                    else:
                        selected = (x, y)
                else:
                    selected = (x, y)

    return level_won'''

'''
import pygame
import random
import time

WIDTH, HEIGHT = 800, 600
TILE_SIZE = 64
GRID_SIZE = 8
MAX_MOVES = 20
TARGET_DROPS = 1
FPS = 60
WHITE = (255, 255, 255)
BLUE = (50, 150, 255)
WATER_COLOR = (0, 180, 255)

TILES = ['D', 'A', 'L', 'C', 'G']  # Доступные фишки

# Функция для отрисовки сетки
def draw_grid(screen, grid, font):
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, WHITE, rect, 1)
            tile = grid[y][x]
            color = WATER_COLOR if tile == 'D' else WHITE
            text = font.render(tile, True, color)
            screen.blit(text, (x * TILE_SIZE + 20, y * TILE_SIZE + 10))

# Функция для обмена фишками
def swap(grid, pos1, pos2):
    y1, x1 = pos1
    y2, x2 = pos2
    grid[y1][x1], grid[y2][x2] = grid[y2][x2], grid[y1][x1]

# Функция для поиска совпадений
def find_matches(grid):
    matches = set()
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE - 2):
            if grid[y][x] == grid[y][x + 1] == grid[y][x + 2]:
                matches.update({(y, x), (y, x + 1), (y, x + 2)})
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE - 2):
            if grid[y][x] == grid[y + 1][x] == grid[y + 2][x]:
                matches.update({(y, x), (y + 1, x), (y + 2, x)})
    return matches

# Функция для удаления совпадений и замены фишек
def remove_matches(grid, matches):
    for y, x in matches:
        grid[y][x] = random.choice(TILES)

# Основная логика игры
def match3_game(screen, inventory):
    font = pygame.font.SysFont(None, 48)
    grid = [[random.choice(TILES) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    selected = None
    collected_drops = 0
    moves_left = MAX_MOVES
    game_over = False
    win = False

    clock = pygame.time.Clock()

    while not game_over:
        screen.fill((0, 0, 0))
        draw_grid(screen, grid, font)
        info = f"Капли: {collected_drops}/{TARGET_DROPS}  Ходы: {moves_left}"
        text = font.render(info, True, WHITE)
        screen.blit(text, (10, HEIGHT - 40))

        if moves_left <= 0 or collected_drops >= TARGET_DROPS:
            game_over = True
            win = collected_drops >= TARGET_DROPS
            message = "Победа! Доступ к воде!" if win else "Вы умерли от жажды..."
            end_text = font.render(message, True, BLUE if win else (255, 0, 0))
            screen.blit(end_text, (WIDTH // 2 - end_text.get_width() // 2, HEIGHT // 2))
            pygame.display.flip()
            pygame.time.wait(2000)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

            if not game_over and event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if y < HEIGHT - 40:
                    grid_x, grid_y = x // TILE_SIZE, y // TILE_SIZE
                    if selected:
                        sy, sx = selected
                        if abs(sy - grid_y) + abs(sx - grid_x) == 1:
                            swap(grid, (sy, sx), (grid_y, grid_x))
                            matches = find_matches(grid)
                            if matches:
                                remove_matches(grid, matches)
                                collected_drops += len([1 for (y, x) in matches if grid[y][x] == 'D'])
                                moves_left -= 1
                            else:
                                swap(grid, (sy, sx), (grid_y, grid_x))
                            selected = None
                        else:
                            selected = (grid_y, grid_x)
                    else:
                        selected = (grid_y, grid_x)

        clock.tick(FPS)

    return win
'''