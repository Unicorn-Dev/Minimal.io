from Application.system.stats import Statistics
from Application.system.menu import Menu
from Application.system.settings import Settings
import Application.system.game_functions as gf
from pygame.sprite import Group
import pygame


def run_game():
    # Initialize game, settings, and create a screen object.
    pygame.init()
    settings = Settings()
    stats = Statistics()
    screen = pygame.display.set_mode(settings.app_screen_dimensions)
    pygame.display.set_caption(settings.name)
    pygame.display.set_icon(pygame.image.load(settings.favicon))
    clock = pygame.time.Clock()

    gf.set_global_var(settings, screen, stats)

    menu = Menu()
    buttons = list()

    # Make a hero and a group to store bullets in.
    bullets = Group()

    # Создание флота enemy balls.
    heroes = list()
    enemies = Group()
    gf.create_fleet(enemies)

    # Start the main loop for the game.
    while True:
        gf.check_events(buttons, heroes, enemies, bullets)
        if stats.game_active:
            gf.update_heroes(heroes)
            gf.fire_bullets(heroes, bullets, enemies)
            gf.update_bullets(heroes, enemies, bullets)
            gf.update_enemies(heroes, enemies, bullets)
            gf.update_screen(heroes, enemies, bullets)
        else:
            buttons = menu.show()
        clock.tick(settings.innerFPS)


run_game()
