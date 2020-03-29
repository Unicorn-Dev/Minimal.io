import pygame


class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 700
        self.screen_height = 500
        self.screen_dimensions = (self.screen_width, self.screen_height)
        self.bg_color = (6, 0, 46)
        self.name = "Unicorn VS Planes"
        self.favicon = pygame.image.load("images/favicon.png")

        # Ship settings
        self.ship_speed_factor = 1

        # Bullet settings
        self.bullet_speed_factor = 2
        self.bullet_width = 15
        self.bullet_height = 3
        self.bullet_color = (255, 255, 33)
        self.bullets_limit = 3
