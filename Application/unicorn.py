import pygame


class Unicorn:
    def __init__(self, settings, screen):
        """Initialize the ship and set its starting position."""
        self.screen = screen
        self.settings = settings

        # Load the ship image and get its rect.
        self.run_images = get_run_images(self)
        self.image = self.run_images[0]
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Store a decimal value for the ship's center.
        self.centery = float(self.rect.centery)
        self.centerx = float(self.rect.centerx)

        # Start each new ship at the bottom center of the screen.
        self.rect.centery = self.centery
        self.rect.left = self.screen_rect.left

        # Movement flag
        self.moving_up = False
        self.moving_down = False
        self.moving_left = False
        self.moving_right = False

        # Fire flag
        self.fire = False

    def update(self):
        """Update the ship's position based on the movement flags."""
        # Update the ship's center value, not the rect.
        if self.moving_up and self.rect.top > 0:
            self.centery -= self.settings.ship_speed_factor
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.centery += self.settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.centerx -= self.settings.ship_speed_factor
        if self.moving_right and self.rect.right < (self.settings.screen_width * 0.2):
            self.centerx += self.settings.ship_speed_factor

        # Update rect object from self.center.
        self.rect.centery = self.centery
        self.rect.centerx = self.centerx

    def draw(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)


def scale_size(self, image):
    """Масштабирование картинки ракеты в зависимости от размера окна."""
    rect = image.get_rect()
    scale = rect[3] / rect[2]
    width = self.settings.screen_width // 15
    height = int(width * scale)
    return width, height


def get_run_images(self):
    tmp = [pygame.image.load(f'images/run/{i + 1}.png') for i in range(5)]
    return [pygame.transform.scale(im, scale_size(self, im)) for im in tmp]
