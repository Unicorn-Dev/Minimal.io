import random
import pygame.draw as draw
import math
from pygame.sprite import Sprite

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
    Ball.settings = setts
    Ball.screen = scr
    Ball.stats = statistics


class Ball(Sprite):
    screen = screen
    settings = settings
    stats = stats
    bullets = None

    def __init__(self):
        """
        Initialize the ball and set its starting position.
        """
        super().__init__()
        self.screen_rect = screen.get_rect()
        # set ball moving parameters
        self.radius = settings.hero_radius
        self.color = None

        # Place each new ball at the left center of the screen.
        self.cx = 0
        self.cy = 0
        self.speed_x = 0
        self.speed_y = 0
        self.direction = -1
        self.move_to_default_position()

        # live settings
        self.life = self.radius * self.radius * 3.14

        # battle atributes
        self.shield_thickness = 0
        self.shield_life = 0
        self.bullet_type = None
        self.shoot_freq = None
        self.shoot_frame_cnt = None

        # istance identy, Enemy -- for enemy, Hero -- for hero
        self.instance = 'Ball'
 
    def update(self):
        self.check_edges()
        self.update_coords()
        self.fire_bullet(self.bullets)

    def move_to_default_position(self):
        self.cx = float(self.radius)  # x coordinate of center
        self.cy = float(self.screen_rect.centery)  # y coordinate of center
    
    def check_edges(self):
        raise Exception

    def update_coords(self):
        """
        Funny thing:
            speed_x is speed on x coord (can be negative)
            speed_y is abs (can't be negative)
        """
        self.cx += self.speed_x
        self.cy += self.speed_y * self.direction

    def draw(self):
        """Draw ball on field."""
        coordinates = (int(self.cx), int(self.cy))
        draw.circle(screen, settings.enemy_shield_color, coordinates,
                                        self.radius + self.shield_thickness)
        draw.circle(screen, self.color, coordinates, self.radius)

    def receive_damage(self, bullets, bullet):
        """Control how balls receive damage from bullets"""
        if bullet.father != self.instance:
            damage = bullet.damage / ((not stats.single_player) + 1)
            if self.shield_life > 0:
                self.shield_life -= damage
                if self.shield_life <= 0:
                    self.life += self.shield_life
                    self.shield_life = 0
            else:
                self.life -= damage
            self.set_radiuses()
            bullet.kill()

    def set_radiuses(self):
        """
        Set ball shield and body radiuses (uses after bullet smashed enemy)
        """
        if self.life > 0:
            self.radius = int(math.sqrt(self.life / 3.14))
            if self.shield_life > 0:
                self.shield_thickness = int(math.sqrt(self.shield_life / 20))
            else:
                self.shield_thickness = 0
        else:
            self.radius = 0
            self.shield_life = 0
            self.shield_thickness = 0

    def set_lifes(self):
        """
        Set ball shield and body radiuses 
        (depends on radius and shield thickness)
        """
        if self.radius > 0:
            self.life = self.radius ** 2 * 3.14
            if self.shield_thickness > 0:
                self.shield_life = self.shield_thickness * \
                                        self.shield_thickness * 20
                assert self.shield_life >= 0
        else:
            self.life = 0
            self.shield_life = 0
            self.shield_thickness = 0

    def fire_bullet(self, bullets):
        """"
        Create an bullet if frame number is big enough.
        """
        if self.bullet_type is not None and self.alive:
            assert self.shoot_freq >= 1
            if self.shoot_frame_cnt >= self.shoot_freq:
                self.shoot_frame_cnt -= self.shoot_freq
                bullets.add(
                    settings.bullet_constructors[self.bullet_type](self)
                    )
            self.shoot_frame_cnt += 1

    def change_bullets(self, bullet_type: str) -> None:
        self.bullet_type = bullet_type
        self.shoot_freq = settings.innerFPS / \
                            settings.BulletPerSecond[self.bullet_type]
        self.shoot_frame_cnt = random.randint(0, 100) % self.shoot_freq
