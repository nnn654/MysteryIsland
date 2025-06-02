# MysteryIsland/common/ui.py

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