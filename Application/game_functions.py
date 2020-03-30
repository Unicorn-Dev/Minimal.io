import sys
from time import sleep
import pygame
from Application.powerball import Powerball
from Application.plane import Plane


def check_events(settings, screen, unicorn, powerballs):
    """Respond to key presses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_key_down_events(event, settings, screen, unicorn, powerballs)
        elif event.type == pygame.KEYUP:
            check_key_up_events(event, unicorn)


def check_key_down_events(event, settings, screen, unicorn, powerballs):
    """Respond to key presses."""
    if event.key == pygame.K_q:
        sys.exit()
    if event.key == pygame.K_SPACE:
        fire_powerball(settings, screen, unicorn, powerballs)
    if event.key == pygame.K_UP:
        unicorn.moving_up = True
    elif event.key == pygame.K_DOWN:
        unicorn.moving_down = True
    elif event.key == pygame.K_LEFT:
        unicorn.moving_left = True
    elif event.key == pygame.K_RIGHT:
        unicorn.moving_right = True


def check_key_up_events(event, unicorn):
    """Respond to key unpresses."""
    if event.key == pygame.K_UP:
        unicorn.moving_up = False
    elif event.key == pygame.K_DOWN:
        unicorn.moving_down = False
    elif event.key == pygame.K_LEFT:
        unicorn.moving_left = False
    elif event.key == pygame.K_RIGHT:
        unicorn.moving_right = False


def fire_powerball(settings, screen, unicorn, powerballs):
    if len(powerballs) < settings.powerballs_limit:
        new_powerball = Powerball(settings, screen, unicorn)
        powerballs.add(new_powerball)


def create_fleet(settings, screen, unicorn, planes):
    """Создает флот пришельцев."""
    # Создание пришельца и вычисление количества пришельцев в ряду.
    # Интервал между соседними пришельцами равен одной ширине пришельца.
    plane = Plane(settings, screen)
    number_planes_row = get_number_planes_in_row(settings, plane.rect.height)
    number_rows = get_number_rows(settings, unicorn.rect.width,
                                  plane.rect.width)
    # Создание первого ряда пришельцев.
    for row_number in range(number_rows):
        for plane_number in range(number_planes_row):
            create_plane(settings, screen, planes, plane_number, row_number)


def get_number_planes_in_row(settings, plane_height):
    """Вычисляет количество пришельцев в ряду."""
    available_space_y = settings.screen_height - 2 * plane_height
    return available_space_y // (2 * plane_height)


def get_number_rows(settings, unicorn_width, plane_width):
    """Определяет количество рядов, помещающихся на экране."""
    available_space_x = (settings.screen_width -
                         (3 * plane_width) - unicorn_width)
    return available_space_x // (3 * plane_width)


def create_plane(settings, screen, planes, plane_number, row_number):
    """Создает пришельца и размещает его в ряду."""
    plane = Plane(settings, screen)
    plane.x = settings.screen_width - 2 * plane.rect.width * (1 + row_number)
    plane.y = plane.rect.height + 2 * plane.rect.height * plane_number
    plane.rect.x = plane.x
    plane.rect.y = plane.y
    planes.add(plane)


def update_powerballs(powerballs, planes, unicorn, screen, settings):
    """Обновляет позиции пуль и уничтожает старые пули."""
    powerballs.update()
    # Удаление пуль, вышедших за край экрана.
    for powerball in powerballs.copy():
        if powerball.x > settings.screen_width:
            powerballs.remove(powerball)
    check_fire_collisions(settings, screen, unicorn, planes, powerballs)


def check_fire_collisions(settings, screen, unicorn, planes, powerballs):
    collisions = pygame.sprite.groupcollide(powerballs, planes, True, True)
    if len(planes) == 0:
        powerballs.empty()
        create_fleet(settings, screen, unicorn, planes)


def check_fleet_edges(settings, planes):
    """Реагирует на достижение пришельцем края экрана."""
    for plane in planes.sprites():
        if plane.check_edges():
            settings.fleet_up *= -1
            break


def update_planes(settings, stats, screen, unicorn, planes, powerballs):
    if check_fleet_edges(settings, planes):
        settings.fleet_up *= -1
    planes.update()
    if pygame.sprite.spritecollideany(unicorn, planes) or planes_flied(planes):
        unicorn_hit(settings, stats, screen, unicorn, planes, powerballs)


def planes_flied(planes):
    """Проверяет, добрались ли пришельцы до нижнего края экрана."""
    for plane in planes.sprites():
        if plane.rect.left <= 0:
            return True


def unicorn_hit(settings, stats, screen, unicorn, planes, powerballs):
    """Обрабатывает столкновение корабля с пришельцем."""
    if stats.lifes_left > 0:
        # Уменьшение ships_left.
        stats.lifes_left -= 1
        # Очистка списков пришельцев и пуль.
        planes.empty()
        powerballs.empty()
        # Создание нового флота и размещение корабля в центре.
        create_fleet(settings, screen, unicorn, planes)
        unicorn.default_position()
        # Пауза.
        sleep(0.5)
    else:
        stats.game_over = True


def update_screen(settings, screen, unicorn, planes, powerballs):
    """Update images on the screen and flip to the new screen."""
    # Redraw the screen during each pass through the loop.
    screen.fill(settings.bg_color)
    unicorn.draw()  # Redraw unicorn.
    powerballs.draw(screen)
    planes.draw(screen)
    pygame.display.flip()
