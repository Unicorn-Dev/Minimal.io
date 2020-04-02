from pygame.sprite import Sprite
import pygame.draw as draw


class Bullet(Sprite):
    """A class to manage powerballs fired from the unicorn"""

    def __init__(self, settings, screen, hero):
        """Create a powerball object at the unicorn's current position."""
        super().__init__()
        self.screen = screen

        # Create a powerball rect at (0, 0) and then set correct position.
        self.radius = settings.bullet_radius
        self.color = settings.hero_color
        self.speed = settings.bullet_speed

        # Store the powerball's position as a decimal value.
        self.cx = float(hero.cx + hero.radius - self.radius)
        self.cy = hero.cy

    def update(self):
        """Move the powerball up the screen."""
        self.cx += self.speed

    def draw(self):
        """Draw the powerball to the screen."""
        coordinates = (int(self.cx), int(self.cy))
        draw.circle(self.screen, self.color, coordinates, self.radius)
