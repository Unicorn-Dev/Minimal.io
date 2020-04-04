import math
from pygame.sprite import Sprite
import pygame.draw as draw
from random import uniform, randint


class Enemy(Sprite):
    """Класс, представляющий одного пришельца."""

    def __init__(self, settings, screen, row):
        """Инициализирует пришельца и задает его начальную позицию."""
        super().__init__()
        self.screen = screen
        self.settings = settings

        # enemy base parameters
        self.radius = randint(settings.enemy_radius // 2, settings.enemy_radius)
        # life is area of ball (in pixels^2 of course)
        self.life = self.radius * self.radius * 3.14
        # reward for killing this enemy. It is equal to self.life point in the begin
        self.reward = self.life
        self.color = settings.enemy_color
        self.speed_x = settings.enemy_horizontal_speed
        self.speed_y = uniform(0, settings.enemy_vertical_speed)
        self.direction = -1

        # Сохранение точной позиции of enemy ball.
        self.cx = settings.battle_screen_width - self.radius * 2
        self.cy = float(self.radius)

    def check_edges(self):
        """Возвращает True, если пришелец находится у края экрана."""
        height = self.settings.battle_screen_height
        if height - self.radius <= self.cy:
            self.direction *= -1
            self.cy = height - self.radius
        elif self.cy <= self.radius:
            self.direction *= -1
            self.cy = self.radius

    def update(self):
        self.cx -= self.speed_x
        self.cy -= self.speed_y * self.direction

    def draw(self):
        """Выводит пришельца в текущем положении."""
        coordinates = (int(self.cx), int(self.cy))
        draw.circle(self.screen, self.color, coordinates, self.radius)

    def set_radius(self):
        if self.life > 0:
            self.radius = int(math.sqrt(self.life / 3.14))
        else:
            self.radius = 0
