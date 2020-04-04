import pygame.image as image
from Application.objects import bullet


class Settings:
    """A class to store all settings for Alien Invasion."""
    __instance = None

    def __init__(self):
        if not Settings.__instance:
            """Initialize the game's settings."""
            # Screen settings
            # app_screen - width of application screen, battle_screen - battle field screen
            # added for more easiest ability to resize window
            self.app_screen_width = 800
            self.app_screen_height = 480
            self.battle_screen_width = 800
            self.battle_screen_height = 480
            self.app_screen_dimensions = (self.app_screen_width, self.app_screen_height)
            self.bg_color = (242, 235, 227)
            self.name = "Minimal.io"
            self.FPS = 60

            # hero settings
            self.lifes_limit = 3
            self.hero_radius = self.battle_screen_height // 12
            self.hero_color = (201, 160, 138)
            self.hero_speed = self.FPS // 8
            self.hero_border = self.battle_screen_width // 5

            # bullet settings
            self.bullet_radius = self.hero_radius // 8
            self.bullet_speed = self.FPS / 6
            # for function that create bullets each next bullet_create_frame frame
            # 10 - for Bullet, 13 - for FastBullet
            self.bullet_create_frame = {"Bullet": 10, "FastBullet": 10, "BigBullet": 15}
            # Create an list of copy constructors for bullets
            self.bullet_constructors = {
                "Bullet": bullet.Bullet,
                "FastBullet": bullet.FastBullet,
                "BigBullet": bullet.BigBullet
            }

            # enemy settings
            self.enemy_radius = self.battle_screen_height // 15
            self.enemy_color = (76, 76, 76)
            self.enemy_horizontal_speed = self.FPS / 60
            self.enemy_vertical_speed = self.FPS / 7

            Settings.__instance = self
        else:
            raise Exception("Settings is a singleton!")
