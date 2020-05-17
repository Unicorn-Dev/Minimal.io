import random
import pygame.draw as draw
import math

from Application.objects.ball import Ball


class Hero(Ball):
    def __init__(self):
        """Initialize the hero and set its starting position."""
        super().__init__()
        self.color = self.settings.hero_color
        
        # live settings
        self.remaining_lives = self.settings.lives_limit
        self.alive = True

        # Movement flags
        self.direction = 1
        self.speed = self.settings.hero_speed
        self.border = self.settings.hero_border

        # type of his bullets, name the same ass bullet class name
        self.bullet_type = "Bullet"
        self.shoot_freq = self.settings.innerFPS / \
                          self.settings.BulletPerSecond[self.bullet_type]
        self.shoot_frame_cnt = random.randint(0, 100) % self.shoot_freq

        self.instance = 'Hero'
    
    def check_edges(self):
        height = self.settings.battle_screen_height
        if (height - self.radius <= self.cy and self.speed_y > 0) or\
                            (self.cy <= self.radius and self.speed_y < 0):
            self.speed_y = 0
        if (self.cx <= self.radius and self.speed_x < 0) or\
            (self.cx + self.radius >= self.border and self.speed_x > 0):
            self.speed_x = 0
