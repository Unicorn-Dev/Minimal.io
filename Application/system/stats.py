class Statistics:
    """Отслеживание статистики для игры Alien Invasion."""
    __instance = None

    def __init__(self, settings):
        if not Statistics.__instance:
            """Инициализирует статистику."""
            self.settings = settings
            self.game_active = False
            self.pause = False
            self.first_game = True
            self.reset_stats()

            Statistics.__instance = self
        else:
            raise Exception("Statistics is a singleton!")

    def reset_stats(self):
        """Инициализирует статистику, изменяющуюся в ходе игры."""
        self.lifes_left = self.settings.lifes_limit
        self.last_score = 0
