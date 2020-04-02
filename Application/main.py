import pygame
from pygame.sprite import Group
from Application.system.menu import Button
from Application.system.settings import Settings
from Application.system.stats import Statistics
from Application.objects.hero import Hero
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

    # Make a hero and a group to store bullets in.
    hero = Hero(settings, screen)
    bullets = Group()

    # Создание флота пришельцев.
    enemies = Group()
    gf.create_fleet(settings, screen, enemies)

    # Start the main loop for the game.
    while True:
        gf.check_events(settings, screen, stats, button, hero, enemies, bullets)
        if stats.game_active:
            hero.update()
            gf.update_bullets(settings, screen, bullets, enemies)
            gf.update_enemies(settings, stats, screen, hero, enemies, bullets)
        gf.update_screen(settings, screen, stats, button, hero, enemies, bullets)
        clock.tick(settings.FPS)


run_game()
