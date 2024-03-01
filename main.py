import pygame
import sys
from two_players import two_players_game

# Инициализация Pygame
pygame.init()
pygame.mixer.init()  # Инициализация модуля звука

# Установка размеров окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Выбор режима игры")

background_image = pygame.image.load("photo.jpg").convert()

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


# Шрифты
font = pygame.font.Font(None, 36)

# Загрузка звукового файла MP3
pygame.mixer.music.load("boi.mp3")  # Путь к вашему файлу MP3

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

def main_menu():
    while True:
        screen.blit(background_image, (0, 0))

        draw_text('МОРСКОЙ БОЙ', font, BLACK, screen, WIDTH // 2, 50)

        # Рисуем кнопки
        button_width, button_height = 350, 50
        button_x = WIDTH // 2 - button_width // 2
        button_spacing = 20
        button_y = 150

        pygame.draw.rect(screen, GRAY, (button_x, button_y, button_width, button_height))
        draw_text('Два игрока', font, BLACK, screen, WIDTH // 2, button_y + button_height // 2)


        pygame.draw.rect(screen, BLUE, (button_x, button_y + 1 * (button_height + button_spacing), button_width, button_height))
        draw_text('Включить звук', font, BLACK, screen, WIDTH // 2, button_y + 1 * (button_height + button_spacing) + button_height // 2)

        pygame.draw.rect(screen, RED, (button_x, button_y + 2 * (button_height + button_spacing), button_width, button_height))
        draw_text('Выключить звук', font, BLACK, screen, WIDTH // 2, button_y + 2 * (button_height + button_spacing) + button_height // 2)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if button_x <= mouse_pos[0] <= button_x + button_width:
                    if button_y <= mouse_pos[1] <= button_y + button_height:
                        # Запускаем режим для двух игроков
                        two_players_game()
                    elif button_y + 1 * (button_height + button_spacing) <= mouse_pos[1] <= button_y + 2 * (button_height + button_spacing):
                        # Включаем звук
                        pygame.mixer.music.play(-1)  # Воспроизводим музыку (циклически)
                        print("Включаем звук")
                    elif button_y + 2 * (button_height + button_spacing) <= mouse_pos[1] <= button_y + 3 * (button_height + button_spacing):
                        # Выключаем звук
                        pygame.mixer.music.stop()  # Останавливаем музыку
                        print("Выключаем звук")

if __name__ == "__main__":
    main_menu()

