import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """A class to manage bullets fired from the ship"""

    def __init__(self, settings, screen, ship):
        """Create a bullet object at the ship's current position."""
        super().__init__()
        self.screen = screen

        # Create a bullet rect at (0, 0) and then set correct position.
        self.rect = pygame.Rect(0, 0, settings.bullet_width,
                                settings.bullet_height)

        # Store the bullet's position as a decimal value.
        self.x = float(ship.rect.right)
        self.rect.right = self.x
        self.rect.top = ship.rect.top

        self.color = settings.bullet_color
        self.speed = settings.bullet_speed_factor

    def update(self):
        """Move the bullet up the screen."""
        # Update the decimal position of the bullet.
        self.x += self.speed
        # Update the rect position.
        self.rect.x = self.x

    def draw(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)
