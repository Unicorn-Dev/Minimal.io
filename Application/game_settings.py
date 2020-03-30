import pygame


class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 800
        self.screen_height = 480
        self.screen_dimensions = (self.screen_width, self.screen_height)
        self.bg_color = (6, 0, 46)
        self.name = "Unicorn VS Planes"
        self.favicon = pygame.image.load("images/favicon.png")
        self.FPS = 60

        # Unicorn settings
        self.lifes_limit = 3
        self.unicorn_speed = self.FPS // 8
        self.unicorn_run_refresh = 0.3  # Should be <= 1.
        self.unicorn_border = self.screen_width * 0.2

        # Powerball settings
        self.powerball_speed_factor = self.FPS // 4
        self.powerballs_limit = 3
        self.powerball_image = pygame.image.load('images/powerball.png')
        self.powerball_image = pb_scale(self.screen_width, self.powerball_image)
        self.powerball_rect = self.powerball_image.get_rect()

        # Plane settings
        self.plane_horizontal_speed = self.FPS // 60
        self.plane_vertical_speed = self.FPS // 30
        self.fleet_up = -1


def pb_scale(width, image):
    """Масштабирование картинки ракеты в зависимости от размера окна."""
    rect = image.get_rect()
    scale = rect[3] / rect[2]
    width = width // 50
    height = int(width * scale)
    return pygame.transform.scale(image, (width, height))
