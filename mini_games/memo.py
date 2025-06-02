# MysteryIsland/mini_games/memo.py
# memo.py
import pygame
import random
import time
import os


def memo_game(screen, inventory, is_fullscreen):
    ROWS, COLS = 3, 4
    FPS = 30
    TIME_LIMIT = 45
    defeat_image = pygame.image.load("../MysteryIsland/icons/defeatmemo.png")

    image_filenames = [
        "plita_1.PNG", "plita_2.PNG", "plita_3.PNG", "plita_4.PNG",
        "plita_5.PNG", "plita_6.PNG"
    ]

    base_path = "../MysteryIsland/icons"

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
            return True

        if time_left <= 0:
            show_victory_sequence(screen, [defeat_image])
            return False

        pygame.display.flip()


def show_victory_sequence(screen, imgs):
    screen_width, screen_height = screen.get_size()
    fade_surface = pygame.Surface((screen_width, screen_height))
    fade_surface.fill((0, 0, 0))

    for img in imgs:
        scaled_img = pygame.transform.scale(img, (screen_width, screen_height))
        for alpha in range(0, 256, 15):
            screen.blit(scaled_img, (0, 0))
            fade_surface.set_alpha(255 - alpha)
            screen.blit(fade_surface, (0, 0))
            pygame.display.flip()
            pygame.time.delay(30)

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