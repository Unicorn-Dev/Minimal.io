import random
import pygame.draw as draw
import math

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


class Hero:
    __instance = None

    def __init__(self):
        """Initialize the unicorn and set its starting position."""

        self.screen_rect = screen.get_rect()

        # Load the unicorn's running and flying images and get its' rect.
        self.radius = settings.hero_radius
        self.life = self.radius * self.radius * 3.14
        self.color = settings.hero_color
        self.speed = settings.hero_speed
        self.border = settings.hero_border

        # Start each new unicorn at the left center of the screen.
        self.cx = 0
        self.cy = 0
        self.move_to_default_position()

        self.remaining_lives = settings.lives_limit
        self.alive = True

        # Movement flags
        self.moving_up = False
        self.moving_down = False
        self.moving_left = False
        self.moving_right = False
        # type of his bullets, name the same ass bullet class name
        self.bullet_type = "Bullet"
        self.shoot_freq = settings.innerFPS / settings.BulletPerSecond[self.bullet_type]
        self.shoot_frame_cnt = random.randint(0, 100) % self.shoot_freq
        # to make app check easier and for hard players)

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
        """Draw hero on field."""
        coordinates = (int(self.cx), int(self.cy))
        draw.circle(screen, self.color, coordinates, self.radius)

    def receive_damage(self, bullets, bullet):
        """Control how enemies receive damage from bullets"""
        if bullet.father == 'Enemy':
            self.life -= bullet.damage
            self.set_radiuses()
            bullets.remove(bullet)

    def set_radiuses(self):
        """Set enemy shield and body radiuses (uses after bullet smashed enemy)"""
        if self.life > 0:
            self.radius = int(math.sqrt(self.life / 3.14))
        else:
            self.radius = 0

    def fire_bullet(self, bullets):
        """"Create an bullet if frame number is big enough."""
        if self.bullet_type is not None and self.alive:
            assert self.shoot_freq >= 1
            if self.shoot_frame_cnt >= self.shoot_freq:
                self.shoot_frame_cnt -= self.shoot_freq
                bullets.add(settings.bullet_constructors[self.bullet_type](self))
            self.shoot_frame_cnt += 1

    def change_bullets(self, bullet_type: str) -> None:
        self.bullet_type = bullet_type
        self.shoot_freq = settings.innerFPS / settings.BulletPerSecond[self.bullet_type]
        self.shoot_frame_cnt = random.randint(0, 100) % self.shoot_freq
