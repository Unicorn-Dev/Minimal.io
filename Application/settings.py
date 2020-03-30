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
        self.unicorn_speed = 0.5

        # powerball settings
        self.powerball_speed_factor = 0.8
        self.powerball_width = 15
        self.powerball_height = 3
        self.powerballs_limit = 5
        self.powerball_image = pygame.image.load('images/powerball.png')
        self.powerball_image = pb_scale(self.screen_width, self.powerball_image)
        self.powerball_rect = self.powerball_image.get_rect()


def pb_scale(width, image):
    """Масштабирование картинки ракеты в зависимости от размера окна."""
    rect = image.get_rect()
    scale = rect[3] / rect[2]
    width = width // 50
    height = int(width * scale)
    return pygame.transform.scale(image, (width, height))