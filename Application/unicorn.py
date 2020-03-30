import pygame


class Unicorn:
    def __init__(self, settings, screen):
        """Initialize the unicorn and set its starting position."""
        self.screen = screen
        self.settings = settings

        # Load the unicorn's running and flying images and get its' rect.
        self.run_images = get_run_images(settings.screen_width)
        self.fly_images = get_fly_images(settings.screen_width)
        self.run_iteration = 0
        self.image = self.run_images[self.run_iteration]
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Store a decimal value for the unicorn's center.
        self.centery = float(self.rect.centery)
        self.centerx = float(self.rect.centerx)

        # Start each new unicorn at the left center of the screen.
        self.rect.centery = self.centery
        self.rect.centerx = self.centerx
        self.rect.left = self.screen_rect.left

        # Movement flags
        self.moving_up = False
        self.moving_down = False
        self.moving_left = False
        self.moving_right = False

    def update(self):
        """Update the unicorn's image and position
         based on the movement flags."""
        if self.moving_up == self.moving_down:
            self.run_iteration += 0.013
            if self.run_iteration >= len(self.run_images):
                self.run_iteration = 0
            self.image = self.run_images[int(self.run_iteration)]
        else:
            if self.moving_up and self.rect.top > 0:
                self.centery -= self.settings.unicorn_speed
                self.run_iteration = 0
                self.image = self.fly_images[0]
            if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
                self.centery += self.settings.unicorn_speed
                self.run_iteration = 0
                self.image = self.fly_images[1]
        if self.moving_left and self.rect.left > 0:
            self.centerx -= self.settings.unicorn_speed
        if self.moving_right and self.rect.right < (self.settings.screen_width * 0.2):
            self.centerx += self.settings.unicorn_speed

        # Update rect object from self.center.
        self.rect = self.image.get_rect()
        self.rect.centery = self.centery
        self.rect.centerx = self.centerx

    def draw(self):
        """Draw the unicorn at its current location."""
        self.screen.blit(self.image, self.rect)


def scale_size(width, image):
    """Масштабирование картинки ракеты в зависимости от размера окна."""
    rect = image.get_rect()
    scale = rect[3] / rect[2]
    width = width // 15
    height = int(width * scale)
    return width, height


def get_run_images(width):
    tmp = [pygame.image.load(f'images/run/{i + 1}.png') for i in range(6)]
    return [pygame.transform.scale(im, scale_size(width, im)) for im in tmp]


def get_fly_images(width):
    up = pygame.image.load('images/run/up.png')
    down = pygame.image.load('images/run/down.png')
    tmp = (up, down)
    return [pygame.transform.scale(im, scale_size(width, im)) for im in tmp]
