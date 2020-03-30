class GameStats:
    """Отслеживание статистики для игры Alien Invasion."""
    def __init__(self, settings):
        """Инициализирует статистику."""
        self.settings = settings
        self.game_over = False
        self.reset_stats()

    def reset_stats(self):
        """Инициализирует статистику, изменяющуюся в ходе игры."""
        self.lifes_left = self.settings.lifes_limit
