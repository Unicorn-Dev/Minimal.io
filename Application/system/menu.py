import pygame


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


class Menu:
    __instance = None

    def __init__(self):
        if not Menu.__instance:
            self.height = settings.battle_screen_height
            self.menu_color = settings.bg_color
            self.text_color = (94, 82, 86)
            self.font = pygame.font.SysFont(None, 64)

            Menu.__instance = self
        else:
            raise Exception("Menu is a singleton!")

    def draw_text(self, screen_rect, y, text):
        text_image = self.font.render(text, True, self.text_color)
        text_image_rect = text_image.get_rect()
        text_image_rect.centerx = screen_rect.centerx
        text_image_rect.y = y
        screen.blit(text_image, text_image_rect)

    def draw_button(self, button, y):
        button.set_y(y)
        button.set_msg(button.text)
        button.draw()

    def show(self):
        director = MenuDirector()
        if stats.choosing_game_type:
            director.set_builder(ChoosingGameTypeMenuBuilder())
        elif stats.pause:
            director.set_builder(PauseMenuBuilder())
        elif stats.first_game:
            director.set_builder(StartMenuBuilder())
        else:
            director.set_builder(NewGameMenuBuilder())
        return director.manage(self)


class MenuDirector:
    def set_builder(self, builder):
        self.__builder = builder

    def manage(self, menu):
        screen.fill(menu.menu_color)
        buttons = self.__builder.get_buttons()

        y = self.get_first_y(menu, buttons)
        screen_rect = screen.get_rect()

        menu.draw_text(screen_rect, y, self.__builder.get_text())

        for button in buttons:
            y += 3 * button.height // 2
            menu.draw_button(button, y)

        pygame.display.flip()

        return buttons

    def get_first_y(self, menu, buttons):
        return (menu.height - 2 * buttons[0].height) // (len(buttons) + 1)


class MenuBuilder:
    def get_text(self):
        pass

    def get_buttons(self):
        pass


class StartMenuBuilder(MenuBuilder):
    def get_text(self):
        return """Get ready, Player One!"""

    def get_buttons(self):
        buttons = list()
        buttons.append(Button("Play"))
        buttons.append(Button("Quit"))
        return buttons


class PauseMenuBuilder(MenuBuilder):
    def get_text(self):
        return """Game paused."""

    def get_buttons(self):
        buttons = list()
        buttons.append(Button("Continue"))
        buttons.append(Button("Restart"))
        buttons.append(Button("Quit"))
        return buttons


class NewGameMenuBuilder(MenuBuilder):
    def get_text(self):
        return f"""Your score is {int (stats.last_score)}!"""

    def get_buttons(self):
        buttons = list()
        buttons.append(Button("Play"))
        buttons.append(Button("Quit"))
        return buttons


class ChoosingGameTypeMenuBuilder(MenuBuilder):
    def get_text(self):
        return """Choose game mode"""

    def get_buttons(self):
        buttons = list()
        buttons.append(Button("One player"))
        buttons.append(Button("Two players"))
        buttons.append(Button("Back"))
        return buttons


class Button:
    def __init__(self, msg):
        """Инициализирует атрибуты кнопки."""
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

    def set_msg(self, msg):
        """Преобразует msg в прямоугольник и выравнивает текст по центру."""
        self.msg_image = self.font.render(msg, True, self.text_color,
                                            self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def set_y(self, y):
        self.rect.y = y

    def draw(self):
        # Отображение пустой кнопки и вывод сообщения.
        screen.fill(self.button_color, self.rect)
        screen.blit(self.msg_image, self.msg_image_rect)
