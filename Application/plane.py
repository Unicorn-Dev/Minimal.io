import pygame
from pygame.sprite import Sprite


class Plane(Sprite):
    """Класс, представляющий одного пришельца."""
    def __init__(self, settings, screen):
        """Инициализирует пришельца и задает его начальную позицию."""
        super().__init__()
        self.screen = screen
        self.settings = settings
        # Загрузка изображения пришельца и назначение атрибута rect.
        self.image = pygame.image.load('images/plane.png')
        self.image = plane_scale(settings.screen_width, self.image)
        self.rect = self.image.get_rect()
        # Сохранение точной позиции пришельца.
        self.x = settings.screen_width - self.rect.width * 1.2
        self.y = float(self.rect.height)
        # Каждый новый пришелец появляется в левом верхнем углу экрана.
        self.rect.x = self.x
        self.rect.y = self.y

    def check_edges(self):
        """Возвращает True, если пришелец находится у края экрана."""
        screen_rect = self.screen.get_rect()
        return self.rect.top <= 0 or self.rect.bottom >= screen_rect.bottom

    def update(self):
        self.x -= self.settings.plane_horizontal_speed
        self.y -= self.settings.plane_vertical_speed * self.settings.fleet_up
        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self):
        """Выводит пришельца в текущем положении."""
        self.screen.blit(self.image, self.rect)


def plane_scale(width, image):
    """Масштабирование картинки ракеты в зависимости от размера окна."""
    rect = image.get_rect()
    scale = rect[3] / rect[2]
    width = width // 13
    height = int(width * scale)
    return pygame.transform.scale(image, (width, height))
