# MysteryIsland/mini_games/match3_game.py
# match3.py
import pygame
import random
import pygame.transform

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


def match3_game(screen, inventory, screen_manager):
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

    def swap(x1, y1, x2, y2): #Меняет местами две плитки.
        board[y1][x1], board[y2][x2] = board[y2][x2], board[y1][x1]

    def find_matches(): #Поиск совпадений.
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

    def drop_tiles(): #Заменяет удалённые плитки
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

        if not game_over: #Обработка логики матчей
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
                return True
            elif not defeat_screen_shown:
                defeat_scaled = pygame.transform.scale(DEFEAT_IMAGE, (screen_width, screen_height))
                screen.blit(defeat_scaled, (0, 0))
                pygame.display.flip()
                pygame.time.delay(10000)  # Показываем экран поражения 10 секунд
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

            elif event.type == pygame.MOUSEBUTTONDOWN and not game_over: #Если клик по полю, вычисляем координаты плитки.
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