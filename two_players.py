import pygame
import sys

# Инициализация Pygame
pygame.init()
pygame.mixer.init()



# Установка размеров окна
WIDTH, HEIGHT = 1000, 600  # Увеличиваем ширину окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Морской бой для двух игроков")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
SHIP_COLOR = (100, 100, 100, 100)  # Устанавливаем прозрачность кораблей
MESSAGE_POSITION = (WIDTH // 2 - 100, HEIGHT - 105)  # Новые координаты для вывода сообщений

# Размеры и расположение игрового поля
BOARD_SIZE = 300
BOARD_MARGIN = 50
CELL_SIZE = 30
BOARD_OFFSET = 420  # Увеличиваем смещение, чтобы второе поле было правее

# Глобальные переменные для хранения текущего направления корабля (0 - горизонтально, 1 - вертикально) и текущего игрока
ship_direction = 0
current_player = 1
message_timer = 0
message_duration = 1500  # Продолжительность отображения сообщений в миллисекундах

# Флаг, определяющий, на каком экране находится игрок (True - игровой экран, False - главный экран)
game_screen = False
show_ships = True

# Функция для отображения сообщения "Ранил" или "Мимо"
def display_hit_or_miss_message(screen, hit):
    font = pygame.font.Font(None, 36)
    if hit:
        text = font.render("Ранил(а)!", True, GREEN)
    else:
        text = font.render("Мимо!", True, RED)
    text_rect = text.get_rect(center=MESSAGE_POSITION)  # Располагаем сообщение в новых координатах
    screen.blit(text, text_rect)
    pygame.display.update()  # Обновляем экран после отображения надписи
    pygame.time.delay(185)

# Функция для отображения сообщения "Корабль сломан"
def display_ship_destroyed_message(screen):
    font = pygame.font.Font(None, 36)
    text = font.render("Корабль сломан!", True, BLUE)
    text_rect = text.get_rect(center=MESSAGE_POSITION)  # Располагаем сообщение в новых координатах
    screen.blit(text, text_rect)

# Функция для отображения сообщения "Игра окончена! Победил игрок №х"
def display_game_over_message(screen, winner):
    font = pygame.font.Font(None, 36)
    text = font.render(f"Игра окончена! Победил игрок №{winner}", True, BLACK)
    text_rect = text.get_rect(center=(WIDTH // 2 - 75, HEIGHT - 75))  # Изменяем координаты для отображения текста чуть ниже
    screen.blit(text, text_rect)


# Функция для отображения игрового поля
def draw_board(surface, board, player):
    # Рисуем игровое поле
    for x in range(10):
        for y in range(10):
            rect = pygame.Rect(BOARD_MARGIN + x * CELL_SIZE + BOARD_OFFSET * player,
                               BOARD_MARGIN + y * CELL_SIZE,
                               CELL_SIZE,
                               CELL_SIZE)
            pygame.draw.rect(surface, WHITE, rect, 1)

    # Рисуем сетку на игровом поле
    for i in range(11):
        pygame.draw.line(surface, BLACK, (BOARD_MARGIN + BOARD_OFFSET * player, BOARD_MARGIN + i * CELL_SIZE),
                         (BOARD_MARGIN + BOARD_OFFSET * player + 10 * CELL_SIZE, BOARD_MARGIN + i * CELL_SIZE), 1)
        pygame.draw.line(surface, BLACK, (BOARD_MARGIN + BOARD_OFFSET * player + i * CELL_SIZE, BOARD_MARGIN),
                         (BOARD_MARGIN + BOARD_OFFSET * player + i * CELL_SIZE, BOARD_MARGIN + 10 * CELL_SIZE), 1)

    # Рисуем координаты
    for i in range(10):
        font = pygame.font.Font(None, 20)
        text = font.render(str(i+1), True, BLACK)
        surface.blit(text, (BOARD_MARGIN - 30 + BOARD_OFFSET * player, BOARD_MARGIN + i * CELL_SIZE + 10))
        text = font.render(chr(65+i), True, BLACK)
        surface.blit(text, (BOARD_MARGIN + i * CELL_SIZE + 10 + BOARD_OFFSET * player, BOARD_MARGIN - 30))

    # Рисуем корабли и попадания на игровом поле
    for x in range(10):
        for y in range(10):
            rect = pygame.Rect(BOARD_MARGIN + x * CELL_SIZE + BOARD_OFFSET * player + 1,
                               BOARD_MARGIN + y * CELL_SIZE + 1,
                               CELL_SIZE - 1,
                               CELL_SIZE - 1)
            if board[x][y] == 1 and show_ships:  # Рисуем корабли, если флаг показа кораблей установлен в True
                pygame.draw.rect(surface, SHIP_COLOR, rect)
            elif board[x][y] == 2:  # Рисуем "Х" в случае попадания
                font = pygame.font.Font(None, 24)
                text = font.render("X", True, RED)
                text_rect = text.get_rect(center=rect.center)
                surface.blit(text, text_rect)

# Функция для вертикальной установки кораблей
def check_ship_placement(board, x, y, size, direction):
    # Проверяем, можно ли поместить корабль на данную позицию
    if direction == 0:  # Горизонтальное направление
        for i in range(size):
            if x + i >= 10 or board[x + i][y] != 0:
                return False
    else:  # Вертикальное направление
        for i in range(size):
            if y + i >= 10 or board[x][y + i] != 0:
                return False
    return True

# Функция для размещения кораблей на поле
def place_ship(board, x, y, size, direction):
    # Размещаем корабль на поле
    if direction == 0:  # Горизонтальное направление
        for i in range(size):
            board[x + i][y] = 1
    else:  # Вертикальное направление
        for i in range(size):
            board[x][y + i] = 1

# Функция для проверки попадания по кораблю
def check_hit(board, x, y):
    if board[x][y] == 1:
        return True
    return False

# Функция для проверки завершения игры
def check_game_over(board):
    for row in board:
        for cell in row:
            if cell == 1:
                return False
    return True

# Функция для размещения кораблей игроками
def place_ships(player_board, screen, player):
    global ship_direction  # Добавляем обращение к глобальной переменной ship_direction
    global show_ships

    ships = {1: 4, 2: 3, 3: 2, 4: 1}  # Количество кораблей каждого размера
    ship_size = 4  # Начинаем с самого большого корабля

    while ship_size > 0:
        screen.fill(WHITE)
        draw_board(screen, player_board, player)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = pygame.mouse.get_pos()
                if BOARD_MARGIN + BOARD_OFFSET * player <= mouseX <= BOARD_MARGIN + BOARD_OFFSET * player + BOARD_SIZE and BOARD_MARGIN <= mouseY <= BOARD_MARGIN + BOARD_SIZE:
                    cell_x = (mouseX - BOARD_MARGIN - BOARD_OFFSET * player) // CELL_SIZE
                    cell_y = (mouseY - BOARD_MARGIN) // CELL_SIZE
                    if player_board[cell_x][cell_y] == 0:
                        if check_ship_placement(player_board, cell_x, cell_y, ship_size, ship_direction):
                            place_ship(player_board, cell_x, cell_y, ship_size, ship_direction)
                            ships[ship_size] -= 1
                            if ships[ship_size] == 0:
                                ship_size -= 1
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # При нажатии на пробел меняем направление корабля
                    ship_direction = (ship_direction + 1) % 2

# Функция для двух игроков
def two_players_game():
    global message_timer, current_player, game_screen, show_ships

    player_1_board = [[0] * 10 for _ in range(10)]
    player_2_board = [[0] * 10 for _ in range(10)]

    player = 1

    place_ships(player_1_board, screen, 0)
    show_ships = True  # Показываем корабли на первой доске
    place_ships(player_2_board, screen, 1)
    show_ships = False  # Скрываем корабли на второй доске

    while True:
        screen.fill(WHITE)
        draw_board(screen, player_1_board, 0)
        draw_board(screen, player_2_board, 1)

        font = pygame.font.Font(None, 24)
        text = font.render(f"Сейчас ходит: Игрок {current_player}", True, BLACK)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2 - 90, HEIGHT - 50))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = pygame.mouse.get_pos()
                if current_player == 1 and BOARD_MARGIN + BOARD_OFFSET <= mouseX <= BOARD_MARGIN + BOARD_OFFSET + BOARD_SIZE and BOARD_MARGIN <= mouseY <= BOARD_MARGIN + BOARD_SIZE:
                    cell_x = (mouseX - BOARD_MARGIN - BOARD_OFFSET) // CELL_SIZE
                    cell_y = (mouseY - BOARD_MARGIN) // CELL_SIZE
                    if check_hit(player_2_board, cell_x, cell_y):
                        print("Player 1: Ранил(а)!")
                        player_2_board[cell_x][cell_y] = 2
                        display_hit_or_miss_message(screen, True)
                        message_timer = message_duration
                    else:
                        print("Player 1: Мимо!")
                        display_hit_or_miss_message(screen, False)
                        current_player = 2
                        message_timer = message_duration

                elif current_player == 2 and BOARD_MARGIN <= mouseX <= BOARD_MARGIN + BOARD_SIZE and BOARD_MARGIN <= mouseY <= BOARD_MARGIN + BOARD_SIZE:
                    cell_x = (mouseX - BOARD_MARGIN) // CELL_SIZE
                    cell_y = (mouseY - BOARD_MARGIN) // CELL_SIZE
                    if check_hit(player_1_board, cell_x, cell_y):
                        print("Player 2: Ранил(а)!")
                        player_1_board[cell_x][cell_y] = 2
                        display_hit_or_miss_message(screen, True)
                        message_timer = message_duration
                    else:
                        print("Player 2: Мимо!")
                        display_hit_or_miss_message(screen, False)
                        current_player = 1
                        message_timer = message_duration


        # Проверяем завершение игры
        if check_game_over(player_1_board):
            display_game_over_message(screen, 2)
            pygame.display.update()
            end_time = pygame.time.get_ticks() + 7000  # Устанавливаем время окончания
            while pygame.time.get_ticks() < end_time:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                pygame.display.update()
            # Переключаемся на главный экран
            game_screen = False
            main_screen()
            break
        elif check_game_over(player_2_board):
            display_game_over_message(screen, 1)
            pygame.display.update()
            end_time = pygame.time.get_ticks() + 7000  # Устанавливаем время окончания
            while pygame.time.get_ticks() < end_time:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                pygame.display.update()
            # Переключаемся на главный экран
            game_screen = False
            main_screen()
            break

        pygame.time.delay(50)

# Функция для отображения главного экрана
def main_screen():
    global game_screen

    font = pygame.font.Font(None, 36)
    text = font.render("На главную", True, BLACK)
    text_rect = text.get_rect(center=(WIDTH // 2 - 100, HEIGHT - 140))
    screen.blit(text, text_rect)
    pygame.display.update()

    while not game_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = pygame.mouse.get_pos()
                if text_rect.collidepoint((mouseX, mouseY)):
                    game_screen = True

# Основная функция
def main():
    main_screen()

# Запуск игры
if __name__ == "__main__":
    main()

