import pygame.font


class Menu:
    def __init__(self, settings, screen, stats):
        self.settings = settings
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.stats = stats

        self.width = settings.screen_width // 2
        self.height = settings.screen_height // 2
        self.menu_window_color = (255, 255, 255)
        self.buttons_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        self.menu_rect = pygame.Rect(0, 0, self.width, self.height)
        self.menu_rect.center = self.screen_rect.center

        self.message = '''Get ready, Player One!'''
        self.show()

    def show(self):
        pass


class Button:
    def __init__(self, screen, msg):
        """Инициализирует атрибуты кнопки."""
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Назначение размеров и свойств кнопок.
        self.width, self.height = 200, 50
        self.button_color = (255, 0, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Построение объекта rect кнопки и выравнивание по центру экрана.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # Сообщение кнопки создается только один раз.
        self.prep_msg(msg)

    def prep_msg(self, msg):
        """Преобразует msg в прямоугольник и выравнивает текст по центру."""
        self.msg_image = self.font.render(msg, True, self.text_color,
                                            self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw(self):
        # Отображение пустой кнопки и вывод сообщения.
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
