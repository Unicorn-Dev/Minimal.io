import pygame.image as image


class Settings:
    """A class to store all settings for Alien Invasion."""
    __instance = None

    def __init__(self):
        if not Settings.__instance:
            """Initialize the game's settings."""
            # Screen settings
            self.screen_width = 800
            self.screen_height = 480
            self.screen_dimensions = (self.screen_width, self.screen_height)
            self.bg_color = (242, 235, 227)
            self.name = "Minimal.io"
            self.favicon = image.load("images/favicon.png")
            self.FPS = 60

            # hero settings
            self.lifes_limit = 3
            self.hero_radius = self.screen_height // 12
            self.hero_color = (201, 160, 138)
            self.hero_speed = self.FPS // 8
            self.hero_border = self.screen_width // 5

            # bullet settings
            self.bullet_radius = self.hero_radius // 8
            self.bullet_speed = self.FPS // 4
            self.bullets_limit = 4

            # enemy settings
            self.enemy_radius = self.screen_height // 15
            self.enemy_color = (76, 76, 76)
            self.enemy_horizontal_speed = self.FPS // 60
            self.enemy_vertical_speed = self.FPS // 7

            Settings.__instance = self
        else:
            raise Exception("Settings is a singleton!")
