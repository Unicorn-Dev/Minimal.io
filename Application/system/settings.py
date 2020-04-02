import pygame.image as image


class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 800
        self.screen_height = 480
        self.screen_dimensions = (self.screen_width, self.screen_height)
        self.bg_color = (242, 235, 227)
        self.name = "Minimal.io"
        self.favicon = image.load("images/favicon.png")
        self.FPS = 80

        # hero settings
        self.lifes_limit = 3
        self.hero_radius = self.screen_height // 10
        self.hero_color = (127, 118, 121)
        self.hero_speed = self.FPS // 16
        self.hero_border = self.screen_width // 5

        # bullet settings
        self.bullet_radius = self.hero_radius // 8
        self.bullet_speed = self.FPS // 8
        self.bullets_limit = 5

        # enemy settings
        self.enemy_radius = self.screen_height // 15
        self.enemy_color = (76, 76, 76)
        self.enemy_horizontal_speed = self.FPS // 80
        self.enemy_vertical_speed = self.FPS // 40
        self.fleet_up = -1
