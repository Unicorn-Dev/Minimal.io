from pygame.sprite import Sprite


class Powerball(Sprite):
    """A class to manage powerballs fired from the unicorn"""

    def __init__(self, settings, screen, unicorn):
        """Create a powerball object at the unicorn's current position."""
        super().__init__()
        self.screen = screen

        # Create a powerball rect at (0, 0) and then set correct position.
        self.image = settings.powerball_image
        self.rect = settings.powerball_rect

        # Store the powerball's position as a decimal value.
        self.x = float(unicorn.rect.right)
        self.rect.right = self.x
        self.rect.top = unicorn.rect.top

        self.speed = settings.powerball_speed_factor

    def update(self):
        """Move the powerball up the screen."""
        # Update the decimal position of the powerball.
        self.x += self.speed
        # Update the rect position.
        self.rect.x = self.x

    def draw(self):
        """Draw the powerball to the screen."""
        self.screen.blit(self.image, self.rect)
