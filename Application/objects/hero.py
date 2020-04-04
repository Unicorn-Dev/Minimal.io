import pygame.draw as draw


class Hero:
    __instance = None

    def __init__(self, settings, screen):
        if not Hero.__instance:
            """Initialize the unicorn and set its starting position."""
            self.screen = screen
            self.screen_rect = screen.get_rect()

            # Load the unicorn's running and flying images and get its' rect.
            self.radius = settings.hero_radius
            self.color = settings.hero_color
            self.speed = settings.hero_speed
            self.border = settings.hero_border

            # Start each new unicorn at the left center of the screen.
            self.move_to_default_position()

            # Movement flags
            self.moving_up = False
            self.moving_down = False
            self.moving_left = False
            self.moving_right = False
            # type of his bullets, name the same ass bullet class name
            self.bullet_type = "Bullet"
            # to make app check easier and for hard players)
            self.not_fire = False
            Hero.__instance = self
        else:
            raise Exception("Hero is a singleton!")

    def move_to_default_position(self):
        self.cx = float(self.radius)  # x coordinate of center
        self.cy = float(self.screen_rect.centery)  # y coordinate of center

    def update(self):
        if self.moving_up and self.cy > self.radius:
            self.cy -= self.speed
        if self.moving_down and self.cy + self.radius < self.screen_rect.bottom:
            self.cy += self.speed
        if self.moving_left and self.cx > self.radius:
            self.cx -= self.speed
        if self.moving_right and self.cx + self.radius < self.border:
            self.cx += self.speed

    def draw(self):
        """Draw the unicorn at its current location."""
        coordinates = (int(self.cx), int(self.cy))
        draw.circle(self.screen, self.color, coordinates, self.radius)
