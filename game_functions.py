import sys
import pygame
from bullet import Bullet
from alien import Alien


def update_screen(ai_settings, screen, ship, aliens, bullets):
    """При каждом прохождении цикла перерисовывать фон."""
    screen.blit(ai_settings.background, (0, 0))
    ship.blitme()
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    aliens.draw(screen)
    # Отображение последнего присвоенного экрана.
    pygame.display.flip()


def update_bullets(bullets):
    """Обновляет позиции пуль и уничтожает старые пули."""
    # Обновление позиции пуль.
    bullets.update()
    # Удаление пуль, вышедших за край экрана.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)


def fire_bullet(ai_settings, screen, ship, bullets):
    """Выпускает пулю, если максимум ещё не достигнут"""
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def check_fleet_edges(ai_settings, aliens):
    """Реагирует на достижение пришельцем края экрана."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """Опускает весь флот и меняет направление флота."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def update_aliens(ai_settings, aliens):
    """Обновляет позиции всех пришельцев во флоте."""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()


def create_fleet(ai_settings, screen, ship, aliens):
    """Создаёт флот пришельцев."""
    # Интервал между соседними пришельцами равен одной ширине пришельца.

    alien = Alien(ai_settings, screen)

    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
                                  alien.rect.height)

    # Создание флота пришельцев.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Создает пришельца и размещает его в ряду."""
    # Создание пришельца и размещение его в ряду.
    alien = Alien(ai_settings, screen)
    alien.x = alien.rect.width + 2 * alien.rect.width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def get_number_aliens_x(ai_settings, alien_width):
    """Вычисляет количество пришельцев в ряду."""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """Вычисляет количество рядов пришельцев."""
    available_space_y = (ai_settings.screen_height -
                         (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def check_events(ai_settings, screen, ship, bullets):
    """"Обрабатывает нажатия клавиш и события мыши."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


def check_keyup_events(event, ship):
    """Реагирует на отпускание клавиш"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """Реагирует на нажатие клавиш"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()
