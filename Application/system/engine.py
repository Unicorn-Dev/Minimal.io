from Application.system.stats import Statistics
from Application.system.menu import Menu
from Application.system.settings import Settings
import Application.system.game_functions as gf
import pygame


class Engine:
    __instance = None

    def __init__(self):
        if not Engine.__instance:
            pygame.init()
            self.settings = Settings()
            self.stats = Statistics()
            self.screen = pygame.display.set_mode(self.settings.screen_dimensions)
            pygame.display.set_caption(self.settings.name)
            pygame.display.set_icon(pygame.image.load(self.settings.favicon))
            self.clock = pygame.time.Clock()

            gf.set_global_var(self.settings, self.screen, self.stats)

            self.menu = Menu()
            self.buttons = list()

            # Create a list of heroes (there can be 1 or 2).
            self.heroes = list()

            # Create a fleet of enemy balls.
            self.enemies = pygame.sprite.Group()
            gf.create_fleet(self.enemies)

            # Make a hero and a group to store bullets in.
            self.bullets = pygame.sprite.Group()
            __instance = self
        else:
            raise Exception("Engine is a singleton!")

    def run(self) -> None:
        gf.check_events(self.buttons, self.heroes, self.enemies, self.bullets)
        if self.stats.game_active:
            gf.update_heroes(self.heroes)
            gf.fire_bullets(self.heroes, self.bullets, self.enemies)
            gf.update_bullets(self.heroes, self.enemies, self.bullets)
            gf.update_enemies(self.heroes, self.enemies, self.bullets)
            gf.update_screen(self.heroes, self.enemies, self.bullets)
        else:
            self.buttons = self.menu.show()
        self.clock.tick(self.settings.innerFPS)
