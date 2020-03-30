import pygame
from pygame.sprite import Group
from Application.game_settings import Settings
from Application.game_stats import GameStats
from Application.unicorn import Unicorn
import Application.game_functions as gf


def run_game():
    # Initialize game, settings, and create a screen object.
    pygame.init()
    settings = Settings()
    stats = GameStats(settings)
    screen = pygame.display.set_mode(settings.screen_dimensions)
    pygame.display.set_caption(settings.name)
    pygame.display.set_icon(settings.favicon)
    clock = pygame.time.Clock()

    # Make a unicorn and a group to store powerballs in.
    unicorn = Unicorn(settings, screen)
    powerballs = Group()
    planes = Group()

    # Создание флота пришельцев.
    gf.create_fleet(settings, screen, unicorn, planes)

    # Start the main loop for the game.
    while True:
        gf.check_events(settings, screen, unicorn, powerballs)
        if not stats.game_over:
            unicorn.update()
            gf.update_powerballs(powerballs, planes, unicorn, screen, settings)
            gf.update_planes(settings, stats, screen,
                             unicorn, planes, powerballs)
            gf.update_screen(settings, screen, unicorn, planes, powerballs)
        clock.tick(settings.FPS)


run_game()
