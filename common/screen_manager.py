# MysteryIsland/common/screen_manager.py
import pygame


class ScreenManager:
    def __init__(self):
        self.is_fullscreen = False
        self.screen = pygame.display.set_mode((800, 600))  # начальный оконный режим

    def toggle_fullscreen(self):
        self.is_fullscreen = not self.is_fullscreen
        if self.is_fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((800, 600))
        return self.screen

    def get_screen(self):
        return self.screen