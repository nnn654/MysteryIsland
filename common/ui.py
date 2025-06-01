# game/common/ui.py

import pygame
import sys

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
OVERLAY_COLOR = (0, 0, 0, 180)
GREEN = (0, 180, 0)
RED = (200, 0, 0)

def show_message(screen, title, subtitle="", color=WHITE, wait_for_key=True):
    font_title = pygame.font.SysFont("arial", 40)
    font_sub = pygame.font.SysFont("arial", 28)

    screen.fill(BLACK)
    title_surf = font_title.render(title, True, color)
    title_rect = title_surf.get_rect(center=(400, 250))
    screen.blit(title_surf, title_rect)

    if subtitle:
        sub_surf = font_sub.render(subtitle, True, WHITE)
        sub_rect = sub_surf.get_rect(center=(400, 320))
        screen.blit(sub_surf, sub_rect)

    pygame.display.flip()

    if wait_for_key:
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    waiting = False

def show_end_screen(screen, victory=True):
    font = pygame.font.SysFont("arial", 48)
    screen.fill((0, 0, 0))
    text = "Победа! Вы спаслись!" if victory else "Вы умерли... Игра окончена"
    color = GREEN if victory else RED
    txt_surface = font.render(text, True, color)
    rect = txt_surface.get_rect(center=(400, 250))
    screen.blit(txt_surface, rect)

    sub_font = pygame.font.SysFont("arial", 28)
    restart_surface = sub_font.render("Нажмите любую клавишу для перезапуска", True, WHITE)
    restart_rect = restart_surface.get_rect(center=(400, 350))
    screen.blit(restart_surface, restart_rect)

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False

def draw_map(screen, inventory):
    map_img = pygame.Surface((400, 400))
    map_img.fill((50, 100, 50))
    pygame.draw.rect(map_img, (255, 255, 255), map_img.get_rect(), 3)

    font = pygame.font.SysFont("arial", 24)
    locations = [
        ("Лабиринт", (20, 20)),
        ("Озеро", (250, 20)),
        ("Виселица", (20, 150)),
        ("Обезьяны", (250, 150)),
        ("Пальмы", (130, 300)),
        ("Корабль", (150, 360))
    ]
    for name, pos in locations:
        text = font.render(name, True, WHITE)
        map_img.blit(text, pos)

    screen.blit(map_img, (200, 100))
    pygame.display.flip()
    pygame.time.wait(3000)