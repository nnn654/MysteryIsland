# MysteryIsland

## Описание проекта

Mystery Island - это квест-игра, разработанная в рамках учебной практики по дисциплине "Основы программирования". Цель проекта - создать игру, включающую элементы квеста, головоломок и аркадных мини-игр, каждая из которых реализована как самостоятельный модуль.

## Механика игры

Ссылка на видео с демонстрацией механики игры - https://disk.yandex.ru/i/WiEsXafC0tk-Mw. 

## Технологии

Проект разработан с использованием следующих технологий:
<ul>
  <li> Язык программирования: Python</li>
  <li> Библиотека: Pygame</li>
  <li> Среда разработки: PyCharm</li>
</ul>  

## Техническое описание проекта

### Установка
1. Клонируйте репозиторий:
```bash
git clone https://github.com/nnn654/MysteryIsland.git
```
2. Откройте проект в PyCharm.
3. Соберите и запустите проект.

## Описание файла main.py

Это основной модуль, который запускает все мини-игры и экраны между ними.
### Функции:
<ul>
  <li> play_music(path, fadeout_ms=2000, fadein_ms=2000)</li>
    <ul>
    <li>Воспроизводит музыкальный файл с fade in/fade out.</li>
    </ul>
  <li> stop_music(fadeout_ms=2000)</li>
    <ul>
    <li>Останавливает текущую музыку с fade out.</li>
    </ul>
  <li> fade_in(screen, image)</li>
    <ul>
    <li>Плавное появление изображения с наложением затемнения.</li>
    </ul>
  <li> fade_out(screen, image)</li>
    <ul>
    <li>Плавное исчезновение изображения с наложением затемнения.</li>
    </ul>
  <li> show_intro_sequence(screen_manager)</li>
    <ul>
    <li>Показывает вступительные сцены в начале игры.</li>
    </ul>
  <li> show_victory_sequence(screen, images, final_music=False)</li>
    <ul>
    <li>Анимация победы после прохождения мини-игры.</li>
    </ul>
  <li> main()</li>
    <ul>
    <li>Главная логика запуска и переходов между мини-играми.</li>
    </ul>
  <li> game_loop()</li>
    <ul>
    Главный цикл, обрабатывающий события и запускающий main().
    </ul>
</ul>

## Описание файла maze.py

Это модуль игры "Лабиринт". Он полностью отвечает за ее реализацию.
### Функции:
<ul>
  <li> maze_game(screen, inventory, screen_manager, victory_images)</li>
    <ul>
    <li>Игровой цикл лабиринта, отслеживает время и победу.</li>
    </ul>
  <li> draw_maze(screen, maze, player_pos, goal_pos, tile_size)</li>
    <ul>
    <li>Отрисовка карты лабиринта, игрока и цели.</li>
    </ul>
  <li> show_defeat_screen(screen, screen_manager)</li>
    <ul>
    <li>Показ экрана поражения, если игрок не прошёл лабиринт вовремя.</li>
    </ul>
</ul>

## Описание файла match3.py

Это модуль игры "Три в ряд". Он полностью отвечает за ее реализацию.
### Функции:
<ul>
  <li> match3_game(screen, inventory, screen_manager, victory_images)</li>
    <ul>
    <li>Главная логика игры Три в ряд.</li>
    </ul>
  <li> draw_board(screen, board, tile_size)</li>
    <ul>
    <li>Отрисовка плиток на поле.</li>
    </ul>
  <li> draw_ui(screen, font, water_count, moves_left)</li>
    <ul>
    <li>Показ интерфейса: очки и ходы.</li>
    </ul>
  <li> swap(board, x1, y1, x2, y2)</li>
    <ul>
    <li>Обмен местами двух плиток.</li>
    </ul>
  <li> find_matches(board)</li>
    <ul>
    <li>Поиск совпадений из 3+ одинаковых плиток.</li>
    </ul>
  <li> remove_matches(board, matches)</li>
    <ul>
    <li>Удаление совпадений с поля.</li>
    </ul>
  <li> drop_tiles(board)</li>
    <ul>
    <li>Падение плиток на свободные места.</li>
    </ul>
</ul>

## Описание файла hangman.py

Это модуль игры "Виселица". Он полностью отвечает за ее реализацию.
### Функции:
<ul>
  <li> hangman_game(screen, inventory, screen_manager, victory_images)</li>
    <ul>
    <li>Игровой цикл по угадыванию 3 слов.</li>
    </ul>
  <li> hangman_round(screen, word, screen_manager)</li>
    <ul>
    <li>Процесс угадывания одного слова.</li>
    </ul>
  <li> show_final_rewards_screen(screen, inventory, screen_manager)</li>
    <ul>
    <li>Отображение наград после угадывания.</li>
    </ul>
  <li> show_failure_screen(screen, screen_manager)</li>
    <ul>
    <li>Экран поражения при неудаче.</li>
    </ul>
</ul>

## Описание файла tictactoe.py

Это модуль игры "Крестики-нолики". Он полностью отвечает за ее реализацию.
### Функции:
<ul>
  <li> tictactoe_game(screen, inventory, screen_manager, victory_images)</li>
    <ul>
    <li>Игра в крестики-нолики: 3 раунда.</li>
    </ul>
  <li> play_one_round(screen, board, screen_manager)</li>
    <ul>
    <li>Один игровой раунд.</li>
    </ul>
  <li> draw_board()</li>
    <ul>
    <li>Отрисовка поля 3x3.</li>
    </ul>
  <li> draw_figures(board)</li>
    <ul>
    <li>Отображение X и O.</li>
    </ul>
  <li> check_win(board, player)</li>
    <ul>
    <li>Проверка выигрыша игрока.</li>
    </ul>
  <li> is_board_full(board)</li>
    <ul>
    <li>Проверка на ничью.</li>
    </ul>
  <li> ai_move(board)</li>
    <ul>
    <li>Ход ИИ.</li>
    </ul>
  <li> draw_background()</li>
    <ul>
    <li>Отрисовка заднего фона игры.</li>
    </ul>
  <li> minimax(board, depth, is_maximizing)</li>
    <ul>
    <li>Рекурсивный алгоритм выбора лучшего хода ИИ.</li>
    </ul>
  <li> update_sizes()</li>
    <ul>
    <li>Изменение размеров поля.</li>
    </ul>
</ul>

## Описание файла memo.py

Это модуль игры "Memo". Он полностью отвечает за ее реализацию.
### Функции:
<ul>
  <li> memo_game(screen, inventory, screen_manager, victory_images)</li>
    <ul>
    <li>Цикл игры на запоминание карточек.</li>
    </ul>
  <li> get_screen_size()</li>
    <ul>
    <li>Текущий размер экрана.</li>
    </ul>
  <li> scale_assets(card_size)</li>
    <ul>
    <li>Масштабирование карточек.</li>
    </ul>
  <li> draw_text(text, pos, color=(0, 0, 0))</li>
    <ul>
    <li>Отрисовка текста.</li>
    </ul>
  <li> draw(self, surface)</li>
    <ul>
    <li>Отрисовка карточки, в зависимости от ее состояния.</li>
    </ul>
  <li> create_cards()</li>
    <ul>
    <li>Создание карточек.</li>
    </ul>
  <li> update_layout()</li>
    <ul>
    <li>Пересоздает части игры под размер окна.</li>
    </ul>
  <li> show_victory_sequence(screen, imgs)</li>
    <ul>
    <li>Используется для показа экрана при поражении.</li>
    </ul>
</ul>

## Описание файла screen_manager.py

Это менеджер экрана, он отвечает за состояние режима экрана.
### Функции:
<ul>
  <li>get_screen()</li>
    <ul>
    <li>Возвращает текущий экран в нужном режиме.</li>
    </ul>
  <li> toggle_fullscreen()</li>
    <ul>
    <li>Переключает между полноэкранным и оконным режимом.</li>
    </ul>
</ul>

## Описание файла inventory.py

Этот модуль добавляет и хранит в списке предметы.
### Функции:
<ul>
  <li>add(self, item)</li>
    <ul>
    <li>Добавляет предмет в инвентарь.</li>
    </ul>
  <li> has(self, item)</li>
    <ul>
    <li>Проверяет наличие предмета в инвентаре.</li>
    </ul>
</ul>

## Описание файла ui.py

Этот модуль отвечает за сообщения, появляющиеся на экране.
### Функции:
<ul>
  <li>show_message(screen, title, subtitle="", color=WHITE, wait_for_key=True)</li>
    <ul>
    <li>Показывает сообщение по центру экрана.</li>
    </ul>
</ul>

