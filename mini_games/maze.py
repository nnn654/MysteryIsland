# game/mini_games/maze.py
# maze.py
import pygame
import time

TILE_SIZE = 30
MAZE_WIDTH = 19
MAZE_HEIGHT = 15
FIELD_WIDTH = MAZE_WIDTH * TILE_SIZE
FIELD_HEIGHT = MAZE_HEIGHT * TILE_SIZE
FPS = 60

background_img = pygame.image.load("C:/Users/bel31/PycharmProjects/pythonProject/game/icons/screen_maze.png")
player_img = pygame.image.load("C:/Users/bel31/PycharmProjects/pythonProject/game/icons/man_maze.png")
player_img = pygame.transform.scale(player_img, (TILE_SIZE, TILE_SIZE))
goal_img = pygame.image.load("C:/Users/bel31/PycharmProjects/pythonProject/game/icons/goal.png")
defeat_img = pygame.image.load("C:/Users/bel31/PycharmProjects/pythonProject/game/icons/defeatmaze.png")  # Новый экран поражения

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 51, 0)
BLACK = (0, 0, 0)

MAZE = [
    "1111111111111111111",
    "1000000000000000001",
    "1011011110111111101",
    "1010000000010000101",
    "1010101111010110111",
    "1010100010000100001",
    "1010111011111110101",
    "1010001000100000101",
    "1011101011111110101",
    "1000101010000010101",
    "1111100010111010101",
    "1000011110101110001",
    "1011001010100011011",
    "1000000000001000001",
    "1111111111111111111"
]

player_pos = [1, 1]
goal_pos = [13, 10]

def draw_maze(screen, maze, player_pos, offset_x, offset_y, tile_size, player_img, goal_img):
    for y, row in enumerate(maze):
        for x, col in enumerate(row):
            if col == "1":
                pygame.draw.rect(screen, GREEN, pygame.Rect(
                    offset_x + x * tile_size,
                    offset_y + y * tile_size,
                    tile_size,
                    tile_size
                ), width=2)

    gx, gy = goal_pos
    screen.blit(goal_img, (offset_x + gx * tile_size, offset_y + gy * tile_size))
    px, py = player_pos
    screen.blit(player_img, (offset_x + px * tile_size, offset_y + py * tile_size))


def maze_game(screen, inventory, screen_manager, victory_imgs):
    global player_pos
    player_pos = [1, 1]
    time_limit = 30
    start_time = time.time()
    clock = pygame.time.Clock()

    running = True
    while running:
        screen.blit(pygame.transform.scale(background_img, screen.get_size()), (0, 0))
        screen_width, screen_height = screen.get_size()
        usable_width = int(screen_width * 0.8)
        usable_height = int(screen_height * 0.8)
        max_tile_x = usable_width // MAZE_WIDTH
        max_tile_y = usable_height // MAZE_HEIGHT
        TILE_SIZE = min(max_tile_x, max_tile_y)
        FIELD_WIDTH = MAZE_WIDTH * TILE_SIZE
        FIELD_HEIGHT = MAZE_HEIGHT * TILE_SIZE

        scaled_player_img = pygame.transform.scale(player_img, (TILE_SIZE, TILE_SIZE))
        scaled_goal_img = pygame.transform.scale(goal_img, (TILE_SIZE, TILE_SIZE))
        offset_x = (screen_width - FIELD_WIDTH) // 2
        offset_y = (screen_height - FIELD_HEIGHT) // 2
        draw_maze(screen, MAZE, player_pos, offset_x, offset_y, TILE_SIZE, scaled_player_img, scaled_goal_img)

        elapsed_time = int(time.time() - start_time)
        remaining_time = max(0, time_limit - elapsed_time)

        font = pygame.font.SysFont("arial", 28)
        time_text = font.render(f"Осталось времени: {remaining_time}s", True, WHITE)
        screen.blit(time_text, (20, 20))

        pygame.display.flip()

        if remaining_time <= 0:
            show_defeat_screen(screen, screen_manager)
            return False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    screen = screen_manager.toggle_fullscreen()
                elif event.key == pygame.K_ESCAPE:
                    if screen_manager.is_fullscreen:
                        screen = screen_manager.toggle_fullscreen()
                    else:
                        pygame.quit()
                        return False

                x, y = player_pos
                if event.key == pygame.K_LEFT and MAZE[y][x - 1] == "0":
                    player_pos[0] -= 1
                elif event.key == pygame.K_RIGHT and MAZE[y][x + 1] == "0":
                    player_pos[0] += 1
                elif event.key == pygame.K_UP and MAZE[y - 1][x] == "0":
                    player_pos[1] -= 1
                elif event.key == pygame.K_DOWN and MAZE[y + 1][x] == "0":
                    player_pos[1] += 1

        if player_pos == goal_pos:
            #show_victory_sequence(screen, victory_imgs)
            return True

        clock.tick(FPS)
    return False


def show_defeat_screen(screen, screen_manager):
    screen_width, screen_height = screen.get_size()
    scaled_defeat = pygame.transform.scale(defeat_img, (screen_width, screen_height))
    screen.blit(scaled_defeat, (0, 0))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False


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
import time

TILE_SIZE = 30
MAZE_WIDTH = 19
MAZE_HEIGHT = 15
FIELD_WIDTH = MAZE_WIDTH * TILE_SIZE
FIELD_HEIGHT = MAZE_HEIGHT * TILE_SIZE
FPS = 60

background_img = pygame.image.load("C:/Users/bel31/PycharmProjects/pythonProject/game/icons/screen_maze.PNG")
player_img = pygame.image.load("C:/Users/bel31/PycharmProjects/pythonProject/game/icons/man_maze.png")
player_img = pygame.transform.scale(player_img, (TILE_SIZE, TILE_SIZE))
goal_img = pygame.image.load("C:/Users/bel31/PycharmProjects/pythonProject/game/icons/goal.png")

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 51, 0)
BLACK = (0, 0, 0)

MAZE = [
    "1111111111111111111",
    "1000000000000000001",
    "1011011110111111101",
    "1010000000010000101",
    "1010101111010110111",
    "1010100010000100001",
    "1010111011111110101",
    "1010001000100000101",
    "1011101011111110101",
    "1000101010000010101",
    "1111100010111010101",
    "1000011110101110001",
    "1011001010100011011",
    "1000000000001000001",
    "1111111111111111111"
]

player_pos = [1, 1]
goal_pos = [13, 10]

def draw_maze(screen, maze, player_pos, offset_x, offset_y, tile_size, player_img, goal_img):
    for y, row in enumerate(maze):
        for x, col in enumerate(row):
            if col == "1":
                pygame.draw.rect(screen, GREEN, pygame.Rect(
                    offset_x + x * tile_size,
                    offset_y + y * tile_size,
                    tile_size,
                    tile_size
                ), width=2)

    gx, gy = goal_pos
    screen.blit(goal_img, (offset_x + gx * tile_size, offset_y + gy * tile_size))
    px, py = player_pos
    screen.blit(player_img, (offset_x + px * tile_size, offset_y + py * tile_size))

def maze_game(screen, inventory, screen_manager, victory_imgs):
    global player_pos
    player_pos = [1, 1]
    time_limit = 40
    start_time = time.time()
    clock = pygame.time.Clock()

    running = True
    while running:
        screen.blit(pygame.transform.scale(background_img, screen.get_size()), (0, 0))
        screen_width, screen_height = screen.get_size()
        usable_width = int(screen_width * 0.8)
        usable_height = int(screen_height * 0.8)
        max_tile_x = usable_width // MAZE_WIDTH
        max_tile_y = usable_height // MAZE_HEIGHT
        TILE_SIZE = min(max_tile_x, max_tile_y)
        FIELD_WIDTH = MAZE_WIDTH * TILE_SIZE
        FIELD_HEIGHT = MAZE_HEIGHT * TILE_SIZE

        scaled_player_img = pygame.transform.scale(player_img, (TILE_SIZE, TILE_SIZE))
        scaled_goal_img = pygame.transform.scale(goal_img, (TILE_SIZE, TILE_SIZE))
        offset_x = (screen_width - FIELD_WIDTH) // 2
        offset_y = (screen_height - FIELD_HEIGHT) // 2
        draw_maze(screen, MAZE, player_pos, offset_x, offset_y, TILE_SIZE, scaled_player_img, scaled_goal_img)

        elapsed_time = int(time.time() - start_time)
        remaining_time = max(0, time_limit - elapsed_time)

        font = pygame.font.SysFont("arial", 28)
        time_text = font.render(f"Осталось времени: {remaining_time}s", True, WHITE)
        screen.blit(time_text, (20, 20))

        pygame.display.flip()

        if remaining_time <= 0:
            show_message(screen, "Время вышло!", "Вы проиграли...", color=RED)
            return False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    screen = screen_manager.toggle_fullscreen()
                elif event.key == pygame.K_ESCAPE:
                    if screen_manager.is_fullscreen:
                        screen = screen_manager.toggle_fullscreen()
                    else:
                        pygame.quit()
                        return False

                x, y = player_pos
                if event.key == pygame.K_LEFT and MAZE[y][x - 1] == "0":
                    player_pos[0] -= 1
                elif event.key == pygame.K_RIGHT and MAZE[y][x + 1] == "0":
                    player_pos[0] += 1
                elif event.key == pygame.K_UP and MAZE[y - 1][x] == "0":
                    player_pos[1] -= 1
                elif event.key == pygame.K_DOWN and MAZE[y + 1][x] == "0":
                    player_pos[1] += 1

        if player_pos == goal_pos:
            show_victory_sequence(screen, victory_imgs)
            return True

        clock.tick(FPS)
    return False

def show_message(screen, title, message, color=WHITE):
    font = pygame.font.SysFont("arial", 32)
    title_text = font.render(title, True, color)
    message_text = font.render(message, True, color)
    screen.fill(BLACK)
    screen_width, screen_height = screen.get_size()
    screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, screen_height // 3))
    screen.blit(message_text, (screen_width // 2 - message_text.get_width() // 2, screen_height // 2))
    pygame.display.flip()
    time.sleep(2)

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
import pygame
import time
#теперь тут в конце есть карта, но все остальное не работает :)

TILE_SIZE = 30
MAZE_WIDTH = 19
MAZE_HEIGHT = 15
FIELD_WIDTH = MAZE_WIDTH * TILE_SIZE
FIELD_HEIGHT = MAZE_HEIGHT * TILE_SIZE
FPS = 60

background_img = pygame.image.load("C:/Users/bel31/PycharmProjects/pythonProject/game/icons/screen_maze.PNG")  # фон
player_img = pygame.image.load("C:/Users/bel31/PycharmProjects/pythonProject/game/icons/man_maze.png")          # игрок
player_img = pygame.transform.scale(player_img, (TILE_SIZE, TILE_SIZE))
victory_img = pygame.image.load("C:/Users/bel31/PycharmProjects/pythonProject/game/icons/victory.PNG")  # путь к изображению победы
goal_img = pygame.image.load("C:/Users/bel31/PycharmProjects/pythonProject/game/icons/goal.png")


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 51, 0)
BLUE = (0, 0, 255)

MAZE = [
    "1111111111111111111",
    "1000000000000000001",
    "1011011110111111101",
    "1010000000010000101",
    "1010101111010110111",
    "1010100010000100001",
    "1010111011111110101",
    "1010001000100000101",
    "1011101011111110101",
    "1000101010000010101",
    "1111100010111010101",
    "1000011110101110001",
    "1011001010100011011",
    "1000000000001000001",
    "1111111111111111111"
]

player_pos = [1, 1]
goal_pos = [13, 10]

def draw_maze(screen, maze, player_pos, offset_x, offset_y, tile_size, player_img, goal_img):
    # Сначала рисуем стены и фон
    for y, row in enumerate(maze):
        for x, col in enumerate(row):
            if col == "1":
                # Тонкая обводка стены
                pygame.draw.rect(
                    screen,
                    GREEN,
                    pygame.Rect(
                        offset_x + x * tile_size,
                        offset_y + y * tile_size,
                        tile_size,
                        tile_size
                    ),
                    width=2
                )

    # Затем рисуем выход, чтобы он оказался сверху
    gx, gy = goal_pos
    screen.blit(goal_img, (offset_x + gx * tile_size, offset_y + gy * tile_size))
   

    # И наконец игрока
    px, py = player_pos
    screen.blit(player_img, (offset_x + px * tile_size, offset_y + py * tile_size))


def maze_game(screen, inventory, screen_manager, victory_img):
    global player_pos
    player_pos = [1, 1]
    time_limit = 40
    start_time = time.time()
    clock = pygame.time.Clock()

    running = True
    while running:
        screen.blit(pygame.transform.scale(background_img, screen.get_size()), (0, 0))


        # Получаем актуальный размер экрана (в случае переключения полноэкранного режима)
        screen_width, screen_height = screen.get_size()

        # Ограничиваем лабиринт до 70% ширины и высоты окна
        usable_width = int(screen_width * 0.8)
        usable_height = int(screen_height * 0.8)

        max_tile_x = usable_width // MAZE_WIDTH
        max_tile_y = usable_height // MAZE_HEIGHT
        TILE_SIZE = min(max_tile_x, max_tile_y)

        FIELD_WIDTH = MAZE_WIDTH * TILE_SIZE
        FIELD_HEIGHT = MAZE_HEIGHT * TILE_SIZE

        # Обновляем спрайт игрока
        scaled_player_img = pygame.transform.scale(player_img, (TILE_SIZE, TILE_SIZE))
        scaled_goal_img = pygame.transform.scale(goal_img, (TILE_SIZE, TILE_SIZE))

        offset_x = (screen_width - FIELD_WIDTH) // 2
        offset_y = (screen_height - FIELD_HEIGHT) // 2

        draw_maze(screen, MAZE, player_pos, offset_x, offset_y, TILE_SIZE, scaled_player_img, scaled_goal_img)

        # Рассчитываем максимально возможный TILE_SIZE, чтобы всё влезло

        elapsed_time = int(time.time() - start_time)
        remaining_time = max(0, time_limit - elapsed_time)

        font = pygame.font.SysFont("arial", 28)
        time_text = font.render(f"Осталось времени: {remaining_time}s", True, WHITE)
        screen.blit(time_text, (20, 20))

        pygame.display.flip()

        if remaining_time <= 0:
            show_message(screen, "Время вышло!", "Вы проиграли...", color=RED)
            return False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

            if event.type == pygame.KEYDOWN:
                # Переключение полноэкранного режима по F11 и ESC
                if event.key == pygame.K_F11:
                    screen = screen_manager.toggle_fullscreen()
                elif event.key == pygame.K_ESCAPE:
                    if screen_manager.is_fullscreen:
                        screen = screen_manager.toggle_fullscreen()
                    else:
                        pygame.quit()
                        return False

                x, y = player_pos
                if event.key == pygame.K_LEFT and MAZE[y][x - 1] == "0":
                    player_pos[0] -= 1
                elif event.key == pygame.K_RIGHT and MAZE[y][x + 1] == "0":
                    player_pos[0] += 1
                elif event.key == pygame.K_UP and MAZE[y - 1][x] == "0":
                    player_pos[1] -= 1
                elif event.key == pygame.K_DOWN and MAZE[y + 1][x] == "0":
                    player_pos[1] += 1

        if player_pos == goal_pos:
            show_victory_screen(screen, victory_img)
            return True

        clock.tick(FPS)
    return False

def show_message(screen, title, message, color=WHITE):
    font = pygame.font.SysFont("arial", 32)
    title_text = font.render(title, True, color)
    message_text = font.render(message, True, color)
    screen.fill(BLACK)
    screen_width, screen_height = screen.get_size()
    screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, screen_height // 3))
    screen.blit(message_text, (screen_width // 2 - message_text.get_width() // 2, screen_height // 2))
    pygame.display.flip()
    time.sleep(2)
    
def show_victory_screen(screen, victory_img):
    screen_width, screen_height = screen.get_size()
    scaled_img = pygame.transform.scale(victory_img, (screen_width, screen_height))
    screen.blit(scaled_img, (0, 0))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False'''

'''
import pygame
import time
import sys

# Параметры игры
TILE_SIZE = 30
MAZE_WIDTH = 19
MAZE_HEIGHT = 15
FIELD_WIDTH = MAZE_WIDTH * TILE_SIZE
FIELD_HEIGHT = MAZE_HEIGHT * TILE_SIZE
FPS = 60

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Карта лабиринта (как на изображении)
MAZE = [
    "1111111111111111111",
    "1000011110000000001",
    "1011011110111111101",
    "1010000000010000101",
    "1010101111010110111",
    "1010100010000100001",
    "1010111011111111101",
    "1010001000100000101",
    "1011111111101110101",
    "1000101010000010101",
    "1111100010111010101",
    "1000001000101110001",
    "1011111111100011111",
    "1000000000001000001",
    "1111111111111111111"
]

# Старт и финиш
player_pos = [1, 1]
goal_pos = [17, 13]


def draw_maze(screen, maze, player_pos, offset_x, offset_y):
    for y, row in enumerate(maze):
        for x, col in enumerate(row):
            color = WHITE
            if col == "1":
                color = BLACK
            elif [x, y] == player_pos:
                color = BLUE
            elif [x, y] == goal_pos:
                color = GREEN
            pygame.draw.rect(
                screen,
                color,
                pygame.Rect(offset_x + x * TILE_SIZE, offset_y + y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            )


def maze_game(screen, inventory):
    global player_pos
    player_pos = [1, 1]
    time_limit = 40
    start_time = time.time()
    clock = pygame.time.Clock()

    screen_width, screen_height = screen.get_size()
    offset_x = (screen_width - FIELD_WIDTH) // 2
    offset_y = (screen_height - FIELD_HEIGHT) // 2

    running = True
    while running:
        screen.fill(BLACK)
        draw_maze(screen, MAZE, player_pos, offset_x, offset_y)

        elapsed_time = int(time.time() - start_time)
        remaining_time = max(0, time_limit - elapsed_time)

        font = pygame.font.SysFont("arial", 24)
        time_text = font.render(f"Осталось времени: {remaining_time}s", True, WHITE)
        screen.blit(time_text, (20, 20))

        pygame.display.flip()

        if remaining_time <= 0:
            show_message(screen, "Время вышло!", "Вы проиграли...", RED)
            return False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                x, y = player_pos
                if event.key == pygame.K_LEFT and MAZE[y][x - 1] == "0":
                    player_pos[0] -= 1
                elif event.key == pygame.K_RIGHT and MAZE[y][x + 1] == "0":
                    player_pos[0] += 1
                elif event.key == pygame.K_UP and MAZE[y - 1][x] == "0":
                    player_pos[1] -= 1
                elif event.key == pygame.K_DOWN and MAZE[y + 1][x] == "0":
                    player_pos[1] += 1

        if player_pos == goal_pos:
            show_message(screen, "Вы нашли выход!", "Ура, победа!", GREEN)
            return True

        clock.tick(FPS)
    return False


def show_message(screen, title, message, color=WHITE):
    font = pygame.font.SysFont("arial", 32)
    title_text = font.render(title, True, color)
    message_text = font.render(message, True, color)
    screen.fill(BLACK)
    screen.blit(title_text, (screen.get_width() // 2 - title_text.get_width() // 2, screen.get_height() // 3))
    screen.blit(message_text, (screen.get_width() // 2 - message_text.get_width() // 2, screen.get_height() // 2))
    pygame.display.flip()
    time.sleep(2)
'''

'''
import pygame
import time

# Параметры игры
TILE_SIZE = 30
MAZE_WIDTH = 19
MAZE_HEIGHT = 15
FIELD_WIDTH = MAZE_WIDTH * TILE_SIZE
FIELD_HEIGHT = MAZE_HEIGHT * TILE_SIZE
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Смещение для центрирования
OFFSET_X = (SCREEN_WIDTH - FIELD_WIDTH) // 2
OFFSET_Y = (SCREEN_HEIGHT - FIELD_HEIGHT) // 2

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Карта лабиринта
MAZE = [
    "1111111111111111111",
    "1000011110000000001",
    "1011011110111111101",
    "1010000000010000101",
    "1010101111010110111",
    "1010100010000100001",
    "1010111011111111101",
    "1010001000100000101",
    "1011111111101110101",
    "1000101010000010101",
    "1111100010111010101",
    "1000001000101110001",
    "1011111111100011111",
    "1000000000001000001",
    "1111111111111111111"
]

# Старт и финиш
player_pos = [1, 1]
goal_pos = [17, 13]

def draw_maze(screen, maze, player_pos):
    for y, row in enumerate(maze):
        for x, col in enumerate(row):
            color = WHITE
            if col == "1":
                color = BLACK
            elif [x, y] == player_pos:
                color = BLUE
            elif [x, y] == goal_pos:
                color = GREEN
            pygame.draw.rect(
                screen,
                color,
                pygame.Rect(OFFSET_X + x * TILE_SIZE, OFFSET_Y + y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            )


def maze_game(screen, inventory):
    global player_pos
    player_pos = [1, 1]
    time_limit = 40
    start_time = time.time()
    clock = pygame.time.Clock()

    running = True
    while running:
        screen.fill(BLACK)
        draw_maze(screen, MAZE, player_pos)

        elapsed_time = int(time.time() - start_time)
        remaining_time = max(0, time_limit - elapsed_time)

        font = pygame.font.SysFont("arial", 24)
        time_text = font.render(f"Осталось времени: {remaining_time}s", True, WHITE)
        screen.blit(time_text, (20, 20))

        pygame.display.flip()

        if remaining_time <= 0:
            show_message(screen, "Время вышло!", "Вы проиграли...", color=RED)
            return False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                x, y = player_pos
                if event.key == pygame.K_LEFT and MAZE[y][x - 1] == "0":
                    player_pos[0] -= 1
                elif event.key == pygame.K_RIGHT and MAZE[y][x + 1] == "0":
                    player_pos[0] += 1
                elif event.key == pygame.K_UP and MAZE[y - 1][x] == "0":
                    player_pos[1] -= 1
                elif event.key == pygame.K_DOWN and MAZE[y + 1][x] == "0":
                    player_pos[1] += 1

        if player_pos == goal_pos:
            show_message(screen, "Вы нашли выход!", "Ура, победа!", color=GREEN)
            return True

        clock.tick(FPS)
    return False


def show_message(screen, title, message, color=WHITE):
    font = pygame.font.SysFont("arial", 32)
    title_text = font.render(title, True, color)
    message_text = font.render(message, True, color)
    screen.fill(BLACK)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 3))
    screen.blit(message_text, (SCREEN_WIDTH // 2 - message_text.get_width() // 2, SCREEN_HEIGHT // 2))
    pygame.display.flip()
    time.sleep(2)
'''



'''
import pygame
import random
import time
from game.common.ui import show_message, show_end_screen, draw_map

WIDTH, HEIGHT = 800, 600
TILE_SIZE = 40
MAZE_WIDTH = 15
MAZE_HEIGHT = 12
FPS = 60

WHITE = (255, 255, 255)
RED = (200, 0, 0)
GREEN = (0, 180, 0)

# Функция для генерации лабиринта
def generate_maze():
    maze = [['#' for _ in range(MAZE_WIDTH)] for _ in range(MAZE_HEIGHT)]
    start, end = (1, 1), (MAZE_HEIGHT - 2, MAZE_WIDTH - 2)
    maze[start[0]][start[1]] = 'S'
    maze[end[0]][end[1]] = 'E'
    return maze, start, end

# Функция для отрисовки лабиринта
def draw_maze(screen, maze, player_pos):
    screen.fill(WHITE)
    for y in range(MAZE_HEIGHT):
        for x in range(MAZE_WIDTH):
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if maze[y][x] == '#':
                pygame.draw.rect(screen, (0, 0, 0), rect)
            elif maze[y][x] == 'S':
                pygame.draw.rect(screen, GREEN, rect)
            elif maze[y][x] == 'E':
                pygame.draw.rect(screen, RED, rect)
            pygame.draw.rect(screen, (255, 255, 255), rect, 1)

    player_rect = pygame.Rect(player_pos[1] * TILE_SIZE, player_pos[0] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
    pygame.draw.rect(screen, (0, 0, 255), player_rect)

    pygame.display.flip()

# Основная логика игры
def maze_game(screen, inventory):
    maze, start, end = generate_maze()
    player_pos = list(start)
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('arial', 24)
    game_over = False
    time_limit = 30
    start_time = time.time()

    while not game_over:
        elapsed_time = time.time() - start_time
        if elapsed_time > time_limit:
            game_over = True
            show_message(screen, "Время истекло!", "Вы не успели пройти лабиринт.", color=RED)
            return False

        draw_maze(screen, maze, player_pos)
        remaining_time = max(0, time_limit - int(elapsed_time))
        time_text = font.render(f"Оставшееся время: {remaining_time}s", True, (255, 255, 255))
        screen.blit(time_text, (10, 10))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and maze[player_pos[0] - 1][player_pos[1]] != '#':
                    player_pos[0] -= 1
                elif event.key == pygame.K_DOWN and maze[player_pos[0] + 1][player_pos[1]] != '#':
                    player_pos[0] += 1
                elif event.key == pygame.K_LEFT and maze[player_pos[0]][player_pos[1] - 1] != '#':
                    player_pos[1] -= 1
                elif event.key == pygame.K_RIGHT and maze[player_pos[0]][player_pos[1] + 1] != '#':
                    player_pos[1] += 1

        if player_pos == end:
            game_over = True
            show_message(screen, "Поздравляем!", "Вы нашли выход!", color=GREEN)
            inventory.add_item("Карта острова")
            return True

        clock.tick(FPS)

    return False
'''