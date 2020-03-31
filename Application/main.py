import pygame
from pygame.sprite import Group
from Application.system.menu import Button
from Application.system.settings import Settings
from Application.system.stats import Statistics
from Application.objects.unicorn import Unicorn
import Application.system.game_functions as gf


def run_game():
    # Initialize game, settings, and create a screen object.
    pygame.init()
    settings = Settings()
    stats = Statistics(settings)
    screen = pygame.display.set_mode(settings.screen_dimensions)
    pygame.display.set_caption(settings.name)
    pygame.display.set_icon(settings.favicon)
    clock = pygame.time.Clock()

    button = Button(screen, "Play")

    # Make a unicorn and a group to store powerballs in.
    unicorn = Unicorn(settings, screen)
    powerballs = Group()

    # Создание флота пришельцев.
    planes = Group()
    gf.create_fleet(settings, screen, unicorn, planes)

    # Start the main loop for the game.
    while True:
        gf.check_events(settings, screen, stats, button, unicorn, planes, powerballs)
        if stats.game_active:
            unicorn.update()
            gf.update_powerballs(powerballs, planes, unicorn, screen, settings)
            gf.update_planes(settings, stats, screen, unicorn, planes, powerballs)
        gf.update_screen(settings, screen, stats, button, unicorn, planes, powerballs)
        clock.tick(settings.FPS)


run_game()
