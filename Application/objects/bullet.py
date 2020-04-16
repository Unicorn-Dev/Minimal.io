import pygame.draw as draw
from pygame.sprite import Sprite

from Application.objects.hero import Hero

settings = None
screen = None
stats = None


def set_global_var(setts, scr, statistics):
    global settings
    global screen
    global stats
    settings = setts
    screen = scr
    stats = statistics


class Bullet(Sprite):
    """A class to manage powerballs fired from the unicorn"""

    def __init__(self, father, radius=None):
        """Create a powerball object at the unicorn's current position."""
        super().__init__()
        self.screen = screen
        self.father = 'Hero'
        # Create a powerball rect at (0, 0) and then set correct position.
        if radius is None:
            self.radius = settings.bullet_radius
        else:
            self.radius = radius
        self.color = father.color
        self.speed = settings.bullet_speed
        self.direction = 1
        self.type = 0

        # Store the powerball's position as a decimal value.
        self.cx = float(father.cx + father.radius - self.radius * self.direction)
        self.cy = father.cy

        # bullet damage parametrs
        self.damage = self.radius * self.radius * 30

    def update(self):
        """Move the powerball up the screen."""
        self.cx += self.speed * self.direction

    def draw(self):
        """Draw the powerball to the screen."""
        coordinates = (int(self.cx), int(self.cy))
        draw.circle(self.screen, self.color, coordinates, self.radius)


class FastBullet(Bullet):
    def __init__(self, father, speed_multiplier=2):
        Bullet.__init__(self, father)
        self.speed = self.speed * speed_multiplier


class BigBullet(Bullet):
    def __init__(self, father, radius_multiplier=3):
        Bullet.__init__(self, father, settings.bullet_radius * radius_multiplier)


class EnemyBullet(Bullet):
    def __init__(self, father):
        Bullet.__init__(self, father)
        self.father = 'Enemy'
        self.cx = float(father.cx - father.radius)
        self.direction = -1
