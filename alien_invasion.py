import sys
import pygame
from settings import Settings


def run_game() -> object:
    """Инициализирует pygame, settings и объект экрана."""
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width,
         ai_settings.screen_height)
    )
    pygame.display.set_caption("Alien Invasion")

    # Запуск основного цикла.
    while True:
        # Отслеживание действий клавиатуры и мыши.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        # При каждом прохождении цикла перерисовывать фон.
        screen.fill(ai_settings.bg_color)
        # Отображение последнего присвоенного экрана.
        pygame.display.flip()


run_game()
