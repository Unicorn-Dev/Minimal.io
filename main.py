import copy
import pygame
from pygame.sprite import Group
from Application.system.menu import Menu
from Application.system.settings import Settings
from Application.system.stats import Statistics
from Application.objects.hero import Hero
import Application.system.game_functions as gf


def run_game():
    # Initialize game, settings, and create a screen object.
    pygame.init()
    settings = Settings()
    stats = Statistics(settings)
    screen = pygame.display.set_mode(settings.app_screen_dimensions)
    pygame.display.set_caption(settings.name)
    clock = pygame.time.Clock()

    gf.set_global_var(settings, screen, stats)

    menu = Menu()
    buttons = list()

    # Make a hero and a group to store bullets in.
    hero = Hero()
    bullets = Group()

    # Создание флота enemy balls.
    enemies = Group()
    gf.create_fleet(enemies)

    # Start the main loop for the game.
    while True:
        gf.check_events(buttons, hero, enemies, bullets)
        if stats.game_active:
            hero.update()
            gf.fire_bullet(hero, bullets, enemies)
            gf.update_bullets(hero, enemies, bullets)
            gf.update_enemies(hero, enemies, bullets)
            gf.update_screen(hero, enemies, bullets)
        else:
            buttons = menu.show()
        clock.tick(settings.innerFPS)


run_game()
