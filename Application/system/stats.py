from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'


class Statistics:
    """Tracking statistics."""
    __instance = None

    def __init__(self):
        if not Statistics.__instance:
            """Statistics initialization."""

            self.game_active = False
            self.pause = False
            self.first_game = True
            self.single_player = True
            self.choosing_game_type = False
            self.last_score = 0
            self.reset_stats()

            Statistics.__instance = self
        else:
            raise Exception("Statistics is a singleton!")

    def reset_stats(self):
        """Инициализирует статистику, изменяющуюся в ходе игры."""
        self.last_score = 0
