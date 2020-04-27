class Settings:
    """A class to store all settings for Alien Invasion."""
    __instance = None

    def __init__(self):
        if not Settings.__instance:
            from Application.objects import bullet
            from pygame import font

            """Initialize the game's settings."""
            # Screen settings
            # Screen_width and screen_height - dimensions of application screen.
            # Added for more easiest ability to resize window.
            self.screen_width = 800
            self.screen_height = 480
            self.battle_screen_width = 800
            self.battle_screen_height = 480
            self.screen_dimensions = (self.screen_width, self.screen_height)
            self.bg_color = (242, 235, 227)
            self.name = "Minimal.io"
            self.favicon = "Application/static/favicon.png"
            # User for update screen, inner for inner calculations
            self.userFPS = 30
            self.innerFPS = 200

            # Hero settings
            self.lives_limit = 3
            self.hero_radius = self.battle_screen_height // 12
            self.hero_color = (201, 160, 138)
            self.hero_speed = 700 / self.innerFPS
            self.hero_border = self.battle_screen_width // 5

            # Bullet settings
            self.bullet_radius = self.hero_radius // 8
            self.bullet_speed = 600 / self.innerFPS
            # For function that create bullets each next bullet_create_frame frame
            # 10 - for Bullet, 13 - for FastBullet
            self.BulletPerSecond = {
                "Bullet": 6,
                "EnemyBullet": 2,
                "FastBullet": 6,
                "BigBullet": 4
            }
            # Create an list of copy constructors for bullets
            self.bullet_constructors = {
                "Bullet": bullet.Bullet,
                "EnemyBullet": bullet.EnemyBullet,
                "FastBullet": bullet.FastBullet,
                "BigBullet": bullet.BigBullet
            }

            # Enemy settings
            self.enemy_radius = self.battle_screen_height // 15
            self.shield_thickness = self.battle_screen_height // 50
            self.enemy_color = (76, 76, 76)
            self.enemy_shield_color = (50, 50, 50)
            self.enemy_horizontal_speed = 60 / self.innerFPS
            self.enemy_vertical_speed = 450 / self.innerFPS
            self.number_enemies_in_row = 2
            self.number_rows_of_enemies = 4

            # Menu settings
            self.menu_text_color = (94, 82, 86)
            self.menu_font_height = 60
            self.menu_font = font.Font('Application/static/Evogria.otf', self.menu_font_height)
            self.button_color = (214, 168, 142)
            self.button_text_color = (255, 255, 255)
            self.button_font_height = 40
            self.button_font = font.Font('Application/static/Delvon.ttf', self.button_font_height)

            Settings.__instance = self
        else:
            raise Exception("Settings is a singleton!")
