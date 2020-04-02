import sys
from time import sleep
from math import sqrt
from functools import lru_cache
import pygame
from Application.objects.bullet import Bullet
from Application.objects.enemy import Enemy


def check_events(settings, screen, stats, buttons, hero, enemies, bullets):
    """Respond to key presses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_key_down_events(event, settings, screen, stats, hero, enemies, bullets)
        elif event.type == pygame.KEYUP:
            check_key_up_events(event, hero)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            check_menu_buttons(settings, screen, stats, buttons, hero, enemies, bullets)


def check_key_down_events(event, settings, screen, stats, hero, enemies, bullets):
    """Respond to key presses."""
    if event.key == pygame.K_q:
        sys.exit()
    elif event.key == pygame.K_p and not stats.game_active:
        start_game(settings, screen, stats, hero, enemies, bullets)
    elif event.key == pygame.K_ESCAPE and stats.game_active != stats.pause:
        set_pause(stats, not stats.pause)
    elif stats.game_active:
        if event.key == pygame.K_SPACE:
            fire_bullet(settings, screen, hero, bullets)
        if event.key == pygame.K_UP:
            hero.moving_up = True
        elif event.key == pygame.K_DOWN:
            hero.moving_down = True
        elif event.key == pygame.K_LEFT:
            hero.moving_left = True
        elif event.key == pygame.K_RIGHT:
            hero.moving_right = True


def check_key_up_events(event, hero):
    """Respond to key unpresses."""
    if event.key == pygame.K_UP:
        hero.moving_up = False
    elif event.key == pygame.K_DOWN:
        hero.moving_down = False
    elif event.key == pygame.K_LEFT:
        hero.moving_left = False
    elif event.key == pygame.K_RIGHT:
        hero.moving_right = False


def check_menu_buttons(settings, screen, stats, buttons, hero, enemies, bullets):
    """Запускает новую игру при нажатии кнопки Play."""
    if not stats.game_active:
        for button in buttons:
            button_clicked = button.rect.collidepoint(pygame.mouse.get_pos())
            if button_clicked:
                if button.text == 'Continue':
                    set_pause(stats, False)
                elif button.text == 'Play' or button.text == 'Restart':
                    start_game(settings, screen, stats, hero, enemies, bullets)
                elif button.text == 'Quit':
                    sys.exit()
                break


def start_game(settings, screen, stats, hero, enemies, bullets):
    prepare_field(settings, screen, hero, enemies, bullets)
    stats.reset_stats()
    pygame.mouse.set_visible(False)
    stats.game_active = True
    stats.pause = False


def set_pause(stats, pause):
    stats.pause = pause
    stats.game_active = not pause
    pygame.mouse.set_visible(pause)


def fire_bullet(settings, screen, hero, bullets):
    if len(bullets) < settings.bullets_limit:
        bullet = Bullet(settings, screen, hero)
        bullets.add(bullet)


def create_fleet(settings, screen, enemies):
    """Создает флот пришельцев."""
    # Создание пришельца и вычисление количества пришельцев в ряду.
    # Интервал между соседними пришельцами равен одной ширине пришельца.
    number_enemies_row = get_number_enemies_in_row(settings)
    number_rows = get_number_rows(settings)
    # Создание первого ряда пришельцев.
    for row in range(number_rows):
        for enemy in range(number_enemies_row):
            create_enemy(settings, screen, enemies, enemy, row)


@lru_cache(maxsize=1)
def get_number_enemies_in_row(settings):
    """Вычисляет количество пришельцев в ряду."""
    available_space_y = settings.screen_height - 2 * settings.enemy_radius
    return available_space_y // (4 * settings.enemy_radius)


@lru_cache(maxsize=1)
def get_number_rows(settings):
    """Определяет количество рядов, помещающихся на экране."""
    available_space_x = (settings.screen_width -
                         6 * settings.enemy_radius - settings.hero_border)
    return available_space_x // (3 * settings.enemy_radius)


def create_enemy(settings, screen, enemies, enemy_number, row):
    """Создает пришельца и размещает его в ряду."""
    enemy = Enemy(settings, screen, row)
    enemy.cx = settings.screen_width - enemy.radius * (1 + 3 * row)
    enemy.cy = enemy.radius * (1 + 4 * enemy_number)
    enemies.add(enemy)


def update_bullets(settings, screen, stats, bullets, enemies):
    """Обновляет позиции пуль и уничтожает старые пули."""
    bullets.update()
    # Удаление пуль, вышедших за край экрана.
    for bullet in bullets.copy():
        if bullet.cx - bullet.radius > settings.screen_width:
            bullets.remove(bullet)
    check_fire_collisions(settings, screen, stats, enemies, bullets)


def check_fire_collisions(settings, screen, stats, enemies, bullets):
    for collision in collisions_of(bullets, enemies):
        bullets.remove(collision[0])
        enemies.remove(collision[1])
        stats.last_score += 1
    if len(enemies) == 0:
        bullets.empty()
        create_fleet(settings, screen, enemies)


def collisions_of(bullets, enemies):
    for bullet in bullets.sprites():
        for enemy in enemies.sprites():
            if is_collision(bullet, enemy):
                yield (bullet, enemy)


def update_enemies(settings, stats, screen, hero, enemies, bullets):
    enemies.update()
    for enemy in enemies:
        enemy.check_edges()
    if enemy_took_hero(hero, enemies) or enemies_flied(enemies):
        hero_die(settings, stats, screen, hero, enemies, bullets)


def is_collision(object1, object2):
    distance = sqrt((object1.cx - object2.cx)**2 + (object1.cy - object2.cy)**2)
    return distance <= object1.radius + object2.radius


def enemy_took_hero(hero, enemies):
    for enemy in enemies:
        if is_collision(hero, enemy):
            return True
    return False


def enemies_flied(enemies):
    """Проверяет, добрались ли пришельцы до нижнего края экрана."""
    for enemy in enemies.sprites():
        if enemy.cx <= enemy.radius:
            return True
    return False


def hero_die(settings, stats, screen, hero, enemies, bullets):
    """Обрабатывает столкновение корабля с пришельцем."""
    if stats.lifes_left > 1:
        # Уменьшение ships_left.
        stats.lifes_left -= 1
        prepare_field(settings, screen, hero, enemies, bullets)
        # Пауза.
        sleep(1)
    else:
        stats.game_active = False
        stats.first_game = False
        pygame.mouse.set_visible(True)


def prepare_field(settings, screen, hero, enemies, bullets):
    # Очистка списков пришельцев и пуль.
    enemies.empty()
    bullets.empty()
    # Создание нового флота и размещение корабля в центре.
    create_fleet(settings, screen, enemies)
    hero.move_to_default_position()


def update_screen(settings, screen, stats, hero, enemies, bullets):
    """Update images on the screen and flip to the new screen."""
    # Redraw the screen during each pass through the loop.
    screen.fill(settings.bg_color)
    hero.draw()  # Redraw hero.
    for bullet in bullets:
        bullet.draw()
    for enemy in enemies:
        enemy.draw()
    pygame.display.flip()
