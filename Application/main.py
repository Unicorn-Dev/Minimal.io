import pygame
from pygame.sprite import Group
from Application.settings import Settings
from Application.unicorn import Unicorn
import Application.game_functions as gf


def run_game():
    # Initialize game, settings, and create a screen object.
    pygame.init()
    settings = Settings()
    screen = pygame.display.set_mode(settings.screen_dimensions)
    pygame.display.set_caption(settings.name)
    pygame.display.set_icon(settings.favicon)

    # Make a unicorn and a group to store bullets in.
    unicorn = Unicorn(settings, screen)
    bullets = Group()

    # Start the main loop for the game.
    while True:
        gf.check_events(settings, screen, unicorn, bullets)
        unicorn.update()
        gf.update_bullets(bullets, settings)
        gf.update_screen(settings, screen, unicorn, bullets)


run_game()
