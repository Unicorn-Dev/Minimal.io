from pygame.sprite import Sprite
import pygame.draw as draw


class Bullet(Sprite):
    """A class to manage powerballs fired from the unicorn"""

    def __init__(self, settings, screen, father):
        """Create a powerball object at the unicorn's current position."""
        super().__init__()
        self.screen = screen

        # Create a powerball rect at (0, 0) and then set correct position.
        self.radius = settings.bullet_radius
        self.color = father.color
        self.speed = settings.bullet_speed
        self.direction = 1
        self.type = 0

        # Store the powerball's position as a decimal value.
        self.cx = float(father.cx + father.radius - self.radius * self.direction)
        self.cy = father.cy

    def update(self):
        """Move the powerball up the screen."""
        self.cx += self.speed * self.direction

    def draw(self):
        """Draw the powerball to the screen."""
        coordinates = (int(self.cx), int(self.cy))
        draw.circle(self.screen, self.color, coordinates, self.radius)
