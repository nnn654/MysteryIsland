# MysteryIsland/mini_games/maze.py
# maze.py
import pygame
import time

TILE_SIZE = 30
MAZE_WIDTH = 19
MAZE_HEIGHT = 15
FIELD_WIDTH = MAZE_WIDTH * TILE_SIZE
FIELD_HEIGHT = MAZE_HEIGHT * TILE_SIZE
FPS = 60

background_img = pygame.image.load("../MysteryIsland/icons/screen_maze.png")
player_img = pygame.image.load("../MysteryIsland/icons/man_maze.png")
player_img = pygame.transform.scale(player_img, (TILE_SIZE, TILE_SIZE))
goal_img = pygame.image.load("../MysteryIsland/icons/goal.png")
defeat_img = pygame.image.load("../MysteryIsland/icons/defeatmaze.png")

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


def maze_game(screen, inventory, screen_manager):
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
            show_defeat_screen(screen)
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
            return True

        clock.tick(FPS)
    return False


def show_defeat_screen(screen):
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
