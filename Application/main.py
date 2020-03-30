import pygame
from pygame.sprite import Group
from Application.game_settings import Settings
from Application.unicorn import Unicorn
import Application.game_functions as gf


def run_game():
    # Initialize game, settings, and create a screen object.
    pygame.init()
    settings = Settings()
    screen = pygame.display.set_mode(settings.screen_dimensions)
    pygame.display.set_caption(settings.name)
    pygame.display.set_icon(settings.favicon)
    clock = pygame.time.Clock()

    # Make a unicorn and a group to store powerballs in.
    unicorn = Unicorn(settings, screen)
    powerballs = Group()

    # Start the main loop for the game.
    while True:
        gf.check_events(settings, screen, unicorn, powerballs)
        unicorn.update()
        gf.update_powerballs(powerballs, settings)
        gf.update_screen(settings, screen, unicorn, powerballs)
        clock.tick(settings.FPS)


run_game()
