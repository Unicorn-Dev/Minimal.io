class Statistics:
    """Отслеживание статистики для игры Alien Invasion."""
    def __init__(self, settings):
        """Инициализирует статистику."""
        self.settings = settings
        self.game_active = False
        self.first_game = True
        self.lifes_left = self.settings.lifes_limit

    def reset_stats(self):
        """Инициализирует статистику, изменяющуюся в ходе игры."""
        self.lifes_left = self.settings.lifes_limit
