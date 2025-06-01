# MysteryIsland/mini_games/hangman.py
# hangman.py

import pygame
import random
#from game1.mini_games.common.ui import show_message  # Используется для экрана поражения

# Словарь категорий и слов
WORD_BANKS = {
    "компас": ["север", "восток", "запад", "стрелка", "путь"],
    "ведро": ["вода", "колодец", "ковш", "тара", "озеро"],
    "факел": ["огонь", "искра", "свет", "пламя", "свеча"]
}

REWARDS = {
    "компас": "Компас.",
    "ведро": "Ведро.",
    "факел": "Факел."
}

def hangman_round(screen, category, words, inventory, screen_manager):
    word = random.choice(words).upper()
    guessed = set()
    wrong = 0
    max_wrong = 6

    background = pygame.image.load("../MysteryIsland/icons/screen_hangman.PNG").convert()
    background = pygame.transform.scale(background, screen.get_size())

    while wrong < max_wrong and not all(c in guessed for c in word):
        # Отрисовка фона
        scaled_bg = pygame.transform.scale(background, screen.get_size())
        screen.blit(scaled_bg, (0, 0))

        # Шрифт, масштабируемый под размер экрана
        font_size = screen.get_height() // 15
        font = pygame.font.SysFont("arial", font_size)

        # Отображение слова с угаданными буквами
        display = " ".join([c if c in guessed else "_" for c in word])
        display_render = font.render(f"{category.upper()}: {display}", True, (65, 47, 47))
        msg_render = font.render(f"Ошибки: {wrong}/{max_wrong}", True, (152, 2, 2))

        screen_width, screen_height = screen.get_size()
        display_rect = display_render.get_rect(center=(screen_width // 2, screen_height // 2 - font_size))
        msg_rect = msg_render.get_rect(center=(screen_width // 2, screen_height // 2 + font_size))

        screen.blit(display_render, display_rect)
        screen.blit(msg_render, msg_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    screen = screen_manager.toggle_fullscreen()
                elif event.key == pygame.K_ESCAPE:
                    if screen_manager.is_fullscreen:
                        screen = screen_manager.toggle_fullscreen()
                    else:
                        pygame.quit()
                        return False

                ch = event.unicode.upper()
                if ch.isalpha() and len(ch) == 1:
                    if ch in word:
                        guessed.add(ch)
                    else:
                        wrong += 1

    if all(c in guessed for c in word):
        inventory.add(category)
        return True
    else:
        return False


def hangman_game(screen, inventory, screen_manager, victory_imgs):
    background_img = pygame.image.load("../MysteryIsland/icons/screen_reshang.png").convert()

    guessed_categories = []

    for category, words in WORD_BANKS.items():
        result = hangman_round(screen, category, words, inventory, screen_manager)
        if result:
            guessed_categories.append(category)

    if len(guessed_categories) == 0:
        show_failure_screen(screen, background_img)
        return False

    show_final_rewards_screen(screen, guessed_categories, background_img)
    #show_victory_sequence(screen, victory_imgs)
    return True



def show_final_rewards_screen(screen, guessed_categories, background_img=None):
    screen_width, screen_height = screen.get_size()

    # Рисуем фон, если он есть
    if background_img:
        bg_scaled = pygame.transform.scale(background_img, (screen_width, screen_height))
        screen.blit(bg_scaled, (0, 0))
    else:
        screen.fill((0, 0, 0))

    # Шрифт для заголовка — больше размера для текста "ВЫ ПОЛУЧИЛИ:"
    title_font_size = screen_height // 12  # например, побольше
    title_font = pygame.font.SysFont("arial", title_font_size, bold=True)

    # Шрифт для остальных строк (награды)
    reward_font_size = screen_height // 18
    reward_font = pygame.font.SysFont("arial", reward_font_size)

    # Рендерим заголовок
    title_text = "ВЫ ПОЛУЧИЛИ:"
    title_render = title_font.render(title_text, True, (65, 47, 47))
    # Позиционируем заголовок чуть выше — например, на 1/8 экрана по вертикали
    title_rect = title_render.get_rect(center=(screen_width // 2, screen_height // 3))
    screen.blit(title_render, title_rect)

    # Стартовая позиция для списка наград — ниже заголовка (с отступом)
    y_offset = title_rect.bottom + 30

    for category in guessed_categories:
        text = REWARDS.get(category, f"Получено: {category}")
        reward_render = reward_font.render(text, True, (65, 47, 47))
        reward_rect = reward_render.get_rect(center=(screen_width // 2, y_offset))
        screen.blit(reward_render, reward_rect)
        y_offset += reward_font.get_height() + 10

    pygame.display.flip()

    # Ждем нажатия клавиши или клика для продолжения
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False


def show_failure_screen(screen, background_img):
    screen_width, screen_height = screen.get_size()
    screen.blit(pygame.transform.scale(background_img, (screen_width, screen_height)), (0, 0))

    font = pygame.font.SysFont("arial", screen_height // 14)

    lines = [
        "Вы проиграли",
        "и становитесь частью острова..."
    ]

    # Рассчитаем высоту блока текста
    line_height = font.get_height()
    total_height = len(lines) * (line_height + 5) - 5  # 5 — отступ между строками
    start_y = (screen_height - total_height) // 2

    for i, line in enumerate(lines):
        text_surf = font.render(line, True, (152, 2, 2))
        text_rect = text_surf.get_rect(center=(screen_width // 2, start_y + i * (line_height + 5) + line_height // 2))
        screen.blit(text_surf, text_rect)

    pygame.display.flip()

    # Ждём, пока пользователь нажмёт клавишу или кнопку мыши
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


'''import pygame, random
from game1.mini_games.common.ui import show_message

WORD_BANKS = {
    "компас": ["север", "восток", "запад", "стрелка", "путь"],
    "ведро": ["вода", "колодец", "ковш", "тара", "озеро"],
    "факел": ["огонь", "искра", "свет", "пламя", "свеча"]
}


def hangman_round(screen, category, words, inventory):
    word = random.choice(words).upper()
    guessed = set()
    wrong = 0
    max_wrong = 6
    font = pygame.font.SysFont("arial", 36)

    while wrong < max_wrong and not all(c in guessed for c in word):
        screen.fill((255, 255, 255))
        display = " ".join([c if c in guessed else "_" for c in word])
        render = font.render(f"{category.upper()}: {display}", True, (0, 0, 0))
        screen.blit(render, (100, 200))
        msg = font.render(f"Ошибки: {wrong}/{max_wrong}", True, (200, 0, 0))
        screen.blit(msg, (100, 260))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()
            if event.type == pygame.KEYDOWN:
                ch = event.unicode.upper()
                if ch.isalpha() and len(ch) == 1:
                    if ch in word:
                        guessed.add(ch)
                    else:
                        wrong += 1

    if all(c in guessed for c in word):
        inventory.add(category)
        show_message(screen, f"Угадано слово: {word}", f"Получен предмет: {category}")
        return True
    else:
        show_message(screen, f"Не угадано слово: {word}", "Раунд проигран")
        return False


def hangman_game(screen, inventory):
    wins = 0
    for category, words in WORD_BANKS.items():
        result = hangman_round(screen, category, words, inventory)
        if result:
            wins += 1

    if wins == 0:
        show_message(screen, "Вы не прошли ни одного раунда", "GAME OVER", color=(200, 0, 0))
        return False
    return True'''
