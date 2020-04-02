from pygame.sprite import Sprite
import pygame.draw as draw


class Enemy(Sprite):
    """Класс, представляющий одного пришельца."""
    def __init__(self, settings, screen):
        """Инициализирует пришельца и задает его начальную позицию."""
        super().__init__()
        self.screen = screen
        self.settings = settings

        # Загрузка изображения пришельца и назначение атрибута rect.
        self.radius = settings.enemy_radius
        self.color = settings.enemy_color
        self.speed_x = settings.enemy_horizontal_speed
        self.speed_y = settings.enemy_vertical_speed

        # Сохранение точной позиции пришельца.
        self.cx = settings.screen_width - self.radius * 2
        self.cy = float(self.radius)

    def check_edges(self):
        """Возвращает True, если пришелец находится у края экрана."""
        height = self.settings.screen_height
        return height - self.radius <= self.cy or self.cy <= self.radius

    def update(self):
        self.cx -= self.speed_x
        self.cy -= self.speed_y * self.settings.fleet_up

    def draw(self):
        """Выводит пришельца в текущем положении."""
        coordinates = (int(self.cx), int(self.cy))
        draw.circle(self.screen, self.color, coordinates, self.radius)
