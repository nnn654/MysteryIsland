# game/mini_games/memo.py
# memo.py


import pygame
import random
import time
import os


def memo_game(screen, inventory, is_fullscreen, victory_imgs):
    ROWS, COLS = 3, 4
    FPS = 30
    TIME_LIMIT = 45  # секунд
    defeat_image = pygame.image.load("C:/Users/bel31/PycharmProjects/pythonProject/game/icons/defeatmemo.png")

    image_filenames = [
        "plita_1.PNG", "plita_2.PNG", "plita_3.PNG", "plita_4.PNG",
        "plita_5.PNG", "plita_6.PNG"
    ]

    base_path = "C:/Users/bel31/PycharmProjects/pythonProject/game/icons"

    font = pygame.font.SysFont(None, 36)
    clock = pygame.time.Clock()

    def get_screen_size():
        return screen.get_size()

    def scale_assets(card_size):
        card_back = pygame.image.load(os.path.join(base_path, "card_back.PNG")).convert()
        card_back = pygame.transform.scale(card_back, (card_size, card_size))
        faces = []
        for filename in image_filenames:
            img = pygame.image.load(os.path.join(base_path, filename)).convert_alpha()
            img = pygame.transform.scale(img, (card_size, card_size))
            faces.append(img)
        return card_back, faces

    def draw_text(text, pos, color=(0, 0, 0)):
        img = font.render(text, True, color)
        screen.blit(img, pos)

    class Card:
        def __init__(self, x, y, image):
            self.rect = pygame.Rect(x, y, card_size, card_size)
            self.image = image
            self.revealed = False
            self.matched = False

        def draw(self, surface):
            if self.revealed or self.matched:
                surface.blit(self.image, self.rect.topleft)
            else:
                surface.blit(card_back_image, self.rect.topleft)
            pygame.draw.rect(surface, (0, 0, 0), self.rect, 2)

    def create_cards():
        pairs = card_faces[: (ROWS * COLS) // 2] * 2
        random.shuffle(pairs)
        cards = []
        for row in range(ROWS):
            for col in range(COLS):
                x = offset_x + col * card_size
                y = offset_y + row * card_size
                image = pairs.pop()
                cards.append(Card(x, y, image))
        return cards

    def update_layout():
        nonlocal WIDTH, HEIGHT, card_size, offset_x, offset_y, card_back_image, card_faces
        WIDTH, HEIGHT = get_screen_size()
        card_size = min(WIDTH // COLS, HEIGHT // ROWS)
        offset_x = (WIDTH - card_size * COLS) // 2
        offset_y = (HEIGHT - card_size * ROWS) // 2
        card_back_image, card_faces = scale_assets(card_size)
        return create_cards()

    # Установка начального режима экрана
    if is_fullscreen:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((800, 600))

    WIDTH, HEIGHT = get_screen_size()
    card_size = min(WIDTH // COLS, HEIGHT // ROWS)
    offset_x = (WIDTH - card_size * COLS) // 2
    offset_y = (HEIGHT - card_size * ROWS) // 2
    card_back_image, card_faces = scale_assets(card_size)
    cards = create_cards()

    first_card = None
    second_card = None
    start_time = time.time()
    matched_pairs = 0
    wait_time_after_fail = 1000  # миллисекунд
    fail_time_start = None

    running = True
    while running:
        clock.tick(FPS)
        screen.fill((255, 255, 255))

        elapsed = time.time() - start_time
        time_left = max(0, int(TIME_LIMIT - elapsed))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False, screen, is_fullscreen

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if is_fullscreen:
                        is_fullscreen = False
                        screen = pygame.display.set_mode((800, 600))
                        cards = update_layout()
                    else:
                        return False, screen, is_fullscreen

                elif event.key == pygame.K_F11:
                    is_fullscreen = not is_fullscreen
                    if is_fullscreen:
                        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode((800, 600))
                    cards = update_layout()

            if event.type == pygame.MOUSEBUTTONDOWN and fail_time_start is None:
                pos = pygame.mouse.get_pos()
                for card in cards:
                    if card.rect.collidepoint(pos):
                        if not card.revealed and not card.matched:
                            card.revealed = True
                            if first_card is None:
                                first_card = card
                            elif second_card is None:
                                second_card = card
                                if first_card.image == second_card.image:
                                    first_card.matched = True
                                    second_card.matched = True
                                    matched_pairs += 1
                                    first_card = None
                                    second_card = None
                                else:
                                    fail_time_start = pygame.time.get_ticks()
                        break

        if fail_time_start:
            if pygame.time.get_ticks() - fail_time_start > wait_time_after_fail:
                first_card.revealed = False
                second_card.revealed = False
                first_card = None
                second_card = None
                fail_time_start = None

        for card in cards:
            card.draw(screen)

        draw_text(f"Время: {time_left}s", (10, HEIGHT - 40))

        if matched_pairs == (ROWS * COLS) // 2:
            #show_victory_sequence(screen, victory_imgs)
            return True, screen, is_fullscreen

        if time_left <= 0:
            show_victory_sequence(screen, [defeat_image])  # например, последнее изображение — экран поражения
            return False, screen, is_fullscreen

        pygame.display.flip()


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



'''import pygame
import random
import time
import os


def memo_game(screen, inventory):
    WIDTH, HEIGHT = 800, 600
    ROWS, COLS = 3, 4
    CARD_SIZE = WIDTH // COLS
    FPS = 30
    TIME_LIMIT = 60  # секунд

    COLORS = [
        (255, 0, 0),      # красный
        (0, 255, 0),      # зелёный
        (0, 0, 255),      # синий
        (255, 255, 0),    # жёлтый
        (255, 0, 255),    # пурпурный
        (0, 255, 255),    # бирюзовый
    ]

    font = pygame.font.SysFont(None, 36)
    clock = pygame.time.Clock()

    card_back_image = pygame.image.load("C:/Users/bel31/PycharmProjects/pythonProject/game/icons/card_back.PNG").convert()
    card_back_image = pygame.transform.scale(card_back_image, (CARD_SIZE, CARD_SIZE))

    image_filenames = [
        "plita_1.PNG", "plita_2.PNG", "plita_3.PNG", "plita_4.PNG",
        "plita_5.PNG", "plita_6.PNG"
    ]

    card_faces = []
    for filename in image_filenames:
        img = pygame.image.load(os.path.join("C:/Users/bel31/PycharmProjects/pythonProject/game/icons", filename)).convert_alpha()
        img = pygame.transform.scale(img, (CARD_SIZE, CARD_SIZE))
        card_faces.append(img)


    def draw_text(text, pos, color=(0,0,0)):
        img = font.render(text, True, color)
        screen.blit(img, pos)

    class Card:
        def __init__(self, x, y, image):
            self.rect = pygame.Rect(x, y, CARD_SIZE, CARD_SIZE)
            self.image = image
            self.revealed = False
            self.matched = False

        def draw(self, surface):
            if self.revealed or self.matched:
                surface.blit(self.image, self.rect.topleft)
            else:
                surface.blit(card_back_image, self.rect.topleft)
            pygame.draw.rect(surface, (0, 0, 0), self.rect, 2)

    def create_cards():
        pairs = card_faces[: (ROWS * COLS) // 2] * 2
        random.shuffle(pairs)
        cards = []
        for row in range(ROWS):
            for col in range(COLS):
                x = col * CARD_SIZE
                y = row * CARD_SIZE
                image = pairs.pop()
                cards.append(Card(x, y, image))
        return cards


    cards = create_cards()
    first_card = None
    second_card = None
    start_time = time.time()
    matched_pairs = 0
    wait_time_after_fail = 1000  # миллисекунд
    fail_time_start = None

    running = True
    while running:
        clock.tick(FPS)
        screen.fill((255, 255, 255))

        elapsed = time.time() - start_time
        time_left = max(0, int(TIME_LIMIT - elapsed))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Вернём False - игра прервана
                return False

            if event.type == pygame.KEYDOWN:
                # Можно добавить выход по ESC
                if event.key == pygame.K_ESCAPE:
                    return False

            if event.type == pygame.MOUSEBUTTONDOWN and fail_time_start is None:
                pos = pygame.mouse.get_pos()
                for card in cards:
                    if card.rect.collidepoint(pos):
                        if not card.revealed and not card.matched:
                            card.revealed = True
                            if first_card is None:
                                first_card = card
                            elif second_card is None:
                                second_card = card
                                if first_card.image == second_card.image:
                                    first_card.matched = True
                                    second_card.matched = True
                                    matched_pairs += 1
                                    first_card = None
                                    second_card = None
                                else:
                                    fail_time_start = pygame.time.get_ticks()
                        break

        if fail_time_start:
            if pygame.time.get_ticks() - fail_time_start > wait_time_after_fail:
                first_card.revealed = False
                second_card.revealed = False
                first_card = None
                second_card = None
                fail_time_start = None

        for card in cards:
            card.draw(screen)

        draw_text(f"Время: {time_left}s", (10, HEIGHT - 40))

        if matched_pairs == (ROWS * COLS) // 2:
            draw_text("Вы выиграли!", (WIDTH // 2 - 80, HEIGHT // 2 - 20), (0, 180, 0))
            pygame.display.flip()
            pygame.time.delay(2000)
            return True

        if time_left <= 0:
            draw_text("Время вышло!", (WIDTH // 2 - 90, HEIGHT // 2 - 20), (255, 0, 0))
            pygame.display.flip()
            pygame.time.delay(2000)
            return False

        pygame.display.flip()'''

'''
import pygame, random
from game1.mini_games.common.ui import show_message


def memo_game(screen, inventory):
    show_message(screen, "Глава 5: Мемо", "Найдите все пары за 30 секунд")

    items = ["банан", "рыба", "манго", "ананас", "клубника", "киви"]
    cards = items * 2
    random.shuffle(cards)

    revealed = [False] * 12
    matched = [False] * 12
    selected = []
    font = pygame.font.SysFont("arial", 60)
    clock = pygame.time.Clock()
    start_ticks = pygame.time.get_ticks()
    max_time = 45

    while True:
        screen.fill((255, 255, 255))
        for i, card in enumerate(cards):
            x, y = 100 + (i % 4) * 120, 100 + (i // 4) * 120
            rect = pygame.Rect(x, y, 100, 100)
            if matched[i] or revealed[i]:
                pygame.draw.rect(screen, (200, 255, 200), rect)
                screen.blit(font.render(card, True, (0, 0, 0)), (x + 20, y + 20))
            else:
                pygame.draw.rect(screen, (150, 150, 150), rect)

        seconds = (pygame.time.get_ticks() - start_ticks) / 1000
        remaining = max(0, max_time - int(seconds))
        time_txt = pygame.font.SysFont("arial", 30).render(f"Время: {remaining}", True, (200, 0, 0))
        screen.blit(time_txt, (10, 10))
        pygame.display.flip()

        if all(matched):
            show_message(screen, "Вы нашли всю еду!", "Получена еда")
            inventory.add("еда")
            return True

        if remaining <= 0:
            show_message(screen, "Вы не успели найти еду", "GAME OVER", color=(200, 0, 0))
            return False

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                for i in range(12):
                    x, y = 100 + (i % 4) * 120, 100 + (i // 4) * 120
                    rect = pygame.Rect(x, y, 100, 100)
                    if rect.collidepoint(mx, my) and not revealed[i] and not matched[i]:
                        revealed[i] = True
                        selected.append(i)
                        if len(selected) == 2:
                            pygame.time.delay(500)
                            if cards[selected[0]] == cards[selected[1]]:
                                matched[selected[0]] = matched[selected[1]] = True
                            revealed[selected[0]] = revealed[selected[1]] = False
                            selected.clear()
        clock.tick(30)
'''