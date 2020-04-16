import sys
from time import sleep
from math import sqrt
from functools import lru_cache
import pygame
from Application.objects.enemy import Enemy
import Application.objects.bullet as bullet_module
import Application.objects.enemy as enemy_module
import Application.objects.hero as hero_module
import Application.system.menu as menu_module


settings = None
screen = None
stats = None


def set_global_var(setts, scr, statistics):
    global settings
    global screen
    global stats
    settings = setts
    screen = scr
    stats = statistics
    bullet_module.set_global_var(setts, scr, statistics)
    enemy_module.set_global_var(setts, scr, statistics)
    hero_module.set_global_var(setts, scr, statistics)
    menu_module.set_global_var(setts, scr, statistics)


def check_events(buttons, hero, enemies, bullets):
    """Respond to key presses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_key_down_events(event, hero, enemies, bullets)
        elif event.type == pygame.KEYUP:
            check_key_up_events(event, hero)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            check_menu_buttons(buttons, hero, enemies, bullets)


def check_key_down_events(event, hero, enemies, bullets):
    """Respond to key presses."""
    if event.key == pygame.K_q:
        sys.exit()
    elif event.key == pygame.K_p and not stats.game_active:
        start_game(hero, enemies, bullets)
    elif event.key == pygame.K_ESCAPE and stats.game_active != stats.pause:
        set_pause(stats, not stats.pause)
    elif stats.game_active:
        # for test, remove in future
        # you can change bullets type if press f (for fast), b (for big) or n (for normal)
        if event.key == pygame.K_n:
            hero.bullet_type = "Bullet"
        if event.key == pygame.K_f:
            hero.bullet_type = "FastBullet"
        if event.key == pygame.K_b:
            hero.bullet_type = "BigBullet"
        #
        if event.key == pygame.K_EQUALS:
            hero.not_fire = not hero.not_fire
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


def check_menu_buttons(buttons, hero, enemies, bullets):
    """Запускает новую игру при нажатии кнопки Play."""
    if not stats.game_active:
        for button in buttons:
            button_clicked = button.rect.collidepoint(pygame.mouse.get_pos())
            if button_clicked:
                if button.text == 'Continue':
                    set_pause(stats, False)
                elif button.text == 'Play' or button.text == 'Restart':
                    start_game(hero, enemies, bullets)
                elif button.text == 'Quit':
                    sys.exit()
                break


def start_game(hero, enemies, bullets):
    prepare_field(hero, enemies, bullets)
    stats.reset_stats()
    pygame.mouse.set_visible(False)
    stats.game_active = True
    stats.pause = False


def set_pause(pause):
    stats.pause = pause
    stats.game_active = not pause
    pygame.mouse.set_visible(pause)


def fire_bullet(hero, bullets, enemies, frame=[0]):
    """"Create an bullet if frame number is big enough."""
    k = settings.innerFPS / settings.BulletPerSecond[hero.bullet_type]
    assert k >= 1
    if not hero.not_fire:
        if frame[0] >= k:
            frame[0] -= k
            bullets.add(settings.bullet_constructors[hero.bullet_type](hero))
        frame[0] += 1
    for enemy in enemies:
        enemy.fire_bullet(bullets)


def create_fleet(enemies):
    """Создает флот пришельцев."""
    # Создание пришельца и вычисление количества пришельцев в ряду.
    # Интервал между соседними пришельцами равен одной ширине пришельца.
    number_enemies_row = get_number_enemies_in_row()
    number_rows = get_number_rows()
    # Создание первого ряда пришельцев.
    for row in range(number_rows):
        for enemy_number in range(number_enemies_row):
            create_enemy(enemies, (enemy_number, number_enemies_row), row)


@lru_cache(maxsize=1)
def get_number_enemies_in_row():
    """Вычисляет количество пришельцев в ряду."""
    return 2


@lru_cache(maxsize=1)
def get_number_rows():
    """Определяет количество рядов, помещающихся на экране."""
    available_space_x = (settings.battle_screen_width -
                         6 * settings.enemy_radius - settings.hero_border)
    return available_space_x // (3 * settings.enemy_radius)


def create_enemy(enemies, enemy_numbers, row):
    """Создает пришельца и размещает его в ряду."""
    EnemyBuilder = enemy_module.EnemyBuilder()
    enemy =  enemy_module.EnemyDirector.RandomEnemy(EnemyBuilder, row)
    # enemy = Enemy(row)
    enemy.cx = settings.battle_screen_width - settings.enemy_radius * (1 + 3 * row)
    enemy.cy = settings.battle_screen_height / enemy_numbers[1] * enemy_numbers[0]
    enemies.add(enemy)


def update_bullets(hero, enemies, bullets):
    """Обновляет позиции пуль и уничтожает старые пули."""
    bullets.update()
    # Удаление пуль, вышедших за край экрана.
    for bullet in bullets.copy():
        if bullet.cx < 0 or bullet.cx > settings.battle_screen_width:
            bullets.remove(bullet)
    check_fire_collisions(hero, enemies, bullets)


def check_fire_collisions(hero, enemies, bullets):
    """Check for every bullet and enemy in sprites if they collision.
    If they collision enemy receive damage"""
    for collision in collisions_of(bullets.sprites(), enemies.sprites()):
        collision[1].receive_damage(bullets, collision[0])
        if collision[1].radius < settings.battle_screen_width / 50:
            stats.last_score += collision[1].reward / settings.battle_screen_width
            enemies.remove(collision[1])
    for collision in collisions_of(bullets.sprites(), [hero]):
        hero.receive_damage(bullets, collision[0])
        if hero.radius < settings.battle_screen_width / 50:
            hero_die(hero, enemies, bullets)
    if len(enemies) == 0:
        bullets.empty()
        create_fleet(enemies)


def check_enemy_collisions(enemies) -> None:
    """Check for every pair of enemies in sprites if they collision.
       If they collision and the hit will happen funk make hit
       according to law of conservation of momentum, m = r ^ 2"""
    for collision in collisions_of_enemies(enemies):
        if will_be_collision(collision[0], collision[1]):
            m0 = collision[0].radius ** 2
            m1 = collision[1].radius ** 2
            # speed before collision
            V0y = collision[0].speed_y * collision[0].direction
            V1y = collision[1].speed_y * collision[1].direction
            # speed after collision
            U0y = (2 * m1 * V1y + m0 * V0y - m1 * V0y) / (m0 + m1)
            U1y = (2 * m0 * V0y + m1 * V1y - m0 * V1y) / (m0 + m1)
            if U0y * V0y < 0:
                collision[0].direction *= -1
            if U1y * V1y < 0:
                collision[1].direction *= -1
            collision[0].speed_y = abs(U0y)
            collision[1].speed_y = abs(U1y)


def will_be_collision(enemy1: Enemy, enemy2: Enemy) -> bool:
    """Check if there will be a collision
    (speed V1y and V2y meet the requirements of the collision)"""
    assert isinstance(enemy1, Enemy) and isinstance(enemy2, Enemy), 'Arguments of wrong type!'
    if enemy1.direction * enemy2.direction < 0:
        if (enemy1.direction > 0 and enemy1.cy < enemy2.cy)\
                or (enemy1.direction < 0 and enemy1.cy > enemy2.cy):
            return True
    elif enemy1.cy > enemy2.cy:
        if (enemy1.direction > 0 and enemy1.speed_y < enemy2.speed_y)\
                or (enemy1.direction < 0 and enemy1.speed_y > enemy2.speed_y):
            return True
    elif (enemy1.direction > 0 and enemy1.speed_y > enemy2.speed_y)\
            or (enemy1.direction < 0 and enemy1.speed_y < enemy2.speed_y):
        return True
    return False


def collisions_of(bullets, enemies):
    for bullet in bullets:
        for enemy in enemies:
            if is_collision(bullet, enemy):
                yield bullet, enemy


def collisions_of_enemies(enemies: pygame.sprite.Group):
    for i in range(len(enemies.sprites())):
        for j in range(i + 1, len(enemies.sprites())):
            if is_collision(enemies.sprites()[i], enemies.sprites()[j]):
                yield enemies.sprites()[i], enemies.sprites()[j]


def update_enemies(hero, enemies, bullets):
    enemies.update()
    for enemy in enemies:
        enemy.check_edges()
    check_enemy_collisions(enemies)
    if enemy_took_hero(hero, enemies) or enemies_flied(enemies):
        hero_die(hero, enemies, bullets)


def is_collision(object1, object2):
    distance = sqrt((object1.cx - object2.cx)**2 + (object1.cy - object2.cy)**2)
    return distance <= object1.radius + object2.radius


def enemy_took_hero(hero, enemies):
    """Сhecks whether one of the enemies was able to touch the hero."""
    for enemy in enemies:
        if is_collision(hero, enemy):
            return True
    return False


def enemies_flied(enemies):
    """Проверяет, добрались ли enemy balls до нижнего края экрана."""
    for enemy in enemies.sprites():
        if enemy.cx <= enemy.radius:
            return True
    return False


def hero_die(hero, enemies, bullets):
    """Handle cases when hero collision with enough enemies or hero receive to many damage from enemy bullets."""
    # reset radius
    hero.radius = settings.hero_radius
    hero.life = hero.radius * hero.radius * 3.14
    if stats.lifes_left > 1:
        # Уменьшение ships_left.
        stats.lifes_left -= 1
        prepare_field(hero, enemies, bullets)
        # Пауза.
        sleep(1)
    else:
        stats.game_active = False
        stats.first_game = False
        pygame.mouse.set_visible(True)


def prepare_field(hero, enemies, bullets):
    # Очистка списков пришельцев и пуль.
    enemies.empty()
    bullets.empty()
    # Создание нового флота и размещение корабля в центре.
    create_fleet(enemies)
    hero.move_to_default_position()


def update_screen(hero, enemies, bullets, frame_numb=[0]):
    """Update images on the screen and flip to the new screen."""
    k = settings.innerFPS / settings.userFPS
    assert k >= 1
    if frame_numb[0] >= k:
        frame_numb[0] -= k - 1
        screen.fill(settings.bg_color)
        hero.draw()  # Redraw hero.
        for bullet in bullets:
            bullet.draw()
        for enemy in enemies:
            enemy.draw()
        pygame.display.flip()
    frame_numb[0] += 1
