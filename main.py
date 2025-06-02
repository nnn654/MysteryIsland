### main.py
import pygame
import sys
from MysteryIsland.mini_games.maze import maze_game
from MysteryIsland.mini_games.match3 import match3_game
from MysteryIsland.mini_games.hangman import hangman_game
from MysteryIsland.mini_games.tictactoe import tictactoe_game
from MysteryIsland.mini_games.memo import memo_game
from MysteryIsland.common.inventory import Inventory
from MysteryIsland.common.screen_manager import ScreenManager


pygame.init()
pygame.font.init()
pygame.mixer.init()
pygame.display.set_caption("MysteryIsland")
icon = pygame.image.load("../MysteryIsland/icons/icon.png")
pygame.display.set_icon(icon)

screen_manager = ScreenManager()
screen_manager.toggle_fullscreen()
FONT = pygame.font.SysFont("arial", 28)


def play_music(music_path, fadeout_ms=1000, fadein_ms=1000):
    pygame.mixer.music.fadeout(fadeout_ms)
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.play(-1, fade_ms=fadein_ms)


def stop_music(fadeout_ms=1000):
    pygame.mixer.music.fadeout(fadeout_ms)


def fade_in(screen, image):
    clock = pygame.time.Clock()
    overlay = pygame.Surface(screen.get_size()).convert_alpha()
    for alpha in range(0, 256, 5):
        screen.blit(image, (0, 0))
        overlay.fill((0, 0, 0, 255 - alpha))
        screen.blit(overlay, (0, 0))
        pygame.display.flip()
        clock.tick(60)


def fade_out(screen, image):
    clock = pygame.time.Clock()
    overlay = pygame.Surface(screen.get_size()).convert_alpha()
    for alpha in range(0, 256, 5):
        screen.blit(image, (0, 0))
        overlay.fill((0, 0, 0, alpha))
        screen.blit(overlay, (0, 0))
        pygame.display.flip()
        clock.tick(60)


def show_intro_sequence(screen_manager):
    SCREEN = screen_manager.get_screen()
    intro_images = [
        pygame.image.load("../MysteryIsland/icons/intro1.png"),
        pygame.image.load("../MysteryIsland/icons/intro2.png"),
        pygame.image.load("../MysteryIsland/icons/intro3.png"),
        pygame.image.load("../MysteryIsland/icons/intro4.png"),
        pygame.image.load("../MysteryIsland/icons/intro5.png"),
    ]

    play_music("../MysteryIsland/sounds/intro_theme.ogg")

    for i, img in enumerate(intro_images):
        img = pygame.transform.scale(img, SCREEN.get_size())

        if i == 2:
            stop_music()
            play_music("../MysteryIsland/sounds/intro3_theme.ogg")

        fade_in(SCREEN, img)
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    waiting = False

        if i == 2:
            stop_music()
            play_music("../MysteryIsland/sounds/main_theme.ogg")

        if i < len(intro_images) - 1:
            fade_out(SCREEN, img)
        else:
            SCREEN.blit(img, (0, 0))
            pygame.display.flip()


def show_victory_sequence(screen, images, final_music=False):
    if final_music:
        play_music("../MysteryIsland/sounds/final_theme.ogg")
    else:
        play_music("../MysteryIsland/sounds/main_theme.ogg")

    for img in images:
        img = pygame.transform.scale(img, screen.get_size())
        fade_in(screen, img)
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    waiting = False
        fade_out(screen, img)


def main():
    inventory = Inventory()

    maze_victory_imgs = [
        pygame.image.load("../MysteryIsland/icons/victorymaze.png"),
        pygame.image.load("../MysteryIsland/icons/map1.png"),
        pygame.image.load("../MysteryIsland/icons/aboutsheep.png"),
        pygame.image.load("../MysteryIsland/icons/intro6.png")
    ]

    match3_victory_imgs = [
        pygame.image.load("../MysteryIsland/icons/victorymatch3.png"),
        pygame.image.load("../MysteryIsland/icons/map2.png"),
        pygame.image.load("../MysteryIsland/icons/intro7.png")
    ]

    hangman_victory_imgs = [
        pygame.image.load("../MysteryIsland/icons/victoryhangman.png"),
        pygame.image.load("../MysteryIsland/icons/map3.png"),
        pygame.image.load("../MysteryIsland/icons/intro8.png")
    ]

    tictactoe_victory_imgs = [
        pygame.image.load("../MysteryIsland/icons/victorytictactoe.png"),
        pygame.image.load("../MysteryIsland/icons/map4.png"),
        pygame.image.load("../MysteryIsland/icons/intro9.png")
    ]

    memo_victory_imgs = [
        pygame.image.load("../MysteryIsland/icons/victorymemo.png"),
        pygame.image.load("../MysteryIsland/icons/map5.png"),
        pygame.image.load("../MysteryIsland/icons/victorygame.png"),
        pygame.image.load("../MysteryIsland/icons/the_end.png")
    ]

    stages = [
        (maze_game, maze_victory_imgs, "../MysteryIsland/sounds/maze_theme.ogg", False),
        (match3_game, match3_victory_imgs, "../MysteryIsland/sounds/match3_theme.ogg", False),
        (hangman_game, hangman_victory_imgs, "../MysteryIsland/sounds/hangman_theme.ogg", False),
        (tictactoe_game, tictactoe_victory_imgs, "../MysteryIsland/sounds/tictactoe_theme.ogg", False),
        (memo_game, memo_victory_imgs, "../MysteryIsland/sounds/memo_theme.ogg", True)
    ]

    for game_func, victory_imgs, music_path, is_final in stages:
        SCREEN = screen_manager.get_screen()
        play_music(music_path)
        result = game_func(SCREEN, inventory, screen_manager)
        if not result:
            pygame.quit()
            sys.exit()
        else:
            show_victory_sequence(SCREEN, victory_imgs, final_music=is_final)

    pygame.quit()
    sys.exit()


def game_loop():
    clock = pygame.time.Clock()

    show_intro_sequence(screen_manager)
    main()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    screen_manager.toggle_fullscreen()
                elif event.key == pygame.K_ESCAPE:
                    if screen_manager.is_fullscreen:
                        screen_manager.toggle_fullscreen()
                    else:
                        pygame.quit()
                        sys.exit()
        pygame.display.flip()
        clock.tick(60)


game_loop()
