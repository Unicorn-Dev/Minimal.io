import pygame


class Menu:
    __instance = None

    def __init__(self, settings, screen, stats):
        if not Menu.__instance:
            self.screen = screen
            self.screen_rect = screen.get_rect()
            self.stats = stats

            self.height = settings.screen_height
            self.menu_color = settings.bg_color
            self.text_color = (94, 82, 86)
            self.font = pygame.font.SysFont(None, 64)

            Menu.__instance = self
        else:
            raise Exception("Menu is a singleton!")

    def show(self):
        self.screen.fill(self.menu_color)
        director = Director(MenuBuilder())
        menu = director.get_menu_contains(self.screen, self.stats)
        y = self.get_first_y(menu)

        self.text_image = self.font.render(menu.text, True, self.text_color)
        self.text_image_rect = self.text_image.get_rect()
        self.text_image_rect.centerx = self.screen_rect.centerx
        self.text_image_rect.y = y
        self.screen.blit(self.text_image, self.text_image_rect)

        for button in menu.buttons:
            y += 3 * button.height // 2
            button.set_y(y)
            button.prep_msg(button.text)
            button.draw()
        pygame.display.flip()

        return menu.buttons

    def get_first_y(self, menu):
        return (self.height - 2 * menu.buttons[0].height) // (len(menu.buttons) + 1)


class MenuContains:
    def __init__(self):
        self.text = None
        self.buttons = list()

    def set_text(self, text):
        self.text = text

    def set_buttons(self, buttons):
        self.buttons = buttons


class Director:
    def __init__(self, builder):
        self.__builder = builder

    def get_menu_contains(self, screen, stats):
        menu = MenuContains()
        menu.set_text(self.__builder.get_text(stats))
        menu.set_buttons(self.__builder.get_buttons(screen, stats))
        return menu


class MenuBuilder:
    def get_text(self, stats):
        if stats.pause:
            return """Game paused."""
        elif stats.first_game:
            return """Get ready, Player One!"""
        else:
            return f"""Your score is {stats.last_score}!"""

    def get_buttons(self, screen, stats):
        buttons = list()
        if stats.pause:
            buttons.append(Button(screen, "Continue"))
            buttons.append(Button(screen, "Restart"))
        else:
            buttons.append(Button(screen, "Play"))
        buttons.append(Button(screen, "Quit"))
        return buttons


class Button:
    def __init__(self, screen, msg):
        """Инициализирует атрибуты кнопки."""
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Назначение размеров и свойств кнопок.
        self.width, self.height = 200, 50
        self.button_color = (214, 168, 142)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Построение объекта rect кнопки и выравнивание по центру экрана.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # Сообщение кнопки создается только один раз.
        self.text = msg

    def prep_msg(self, msg):
        """Преобразует msg в прямоугольник и выравнивает текст по центру."""
        self.msg_image = self.font.render(msg, True, self.text_color,
                                            self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def set_y(self, y):
        self.rect.y = y

    def draw(self):
        # Отображение пустой кнопки и вывод сообщения.
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
