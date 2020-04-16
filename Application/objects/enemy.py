import math
from pygame.sprite import Sprite
import pygame.draw as draw
from random import uniform, randint

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


class EnemyDirector:
    """"Class for user friendly work with Enemy. Have most popular in game templates for enemy.
    In the begin Enemy director initialize self.enemy_cash so every enemy created with less calculations."""
    enemy_cash = None

    def __init__(self):
        self.__set_enemy_cash()

    def __set_enemy_cash(self):
        pass

    # templates
    @staticmethod
    def ShieldEnemy(builder, row: int):
        """Create and return a standard enemy with shield."""
        builder.reset()
        builder.set_raw(row)
        builder.set_shield()
        builder.set_reward()
        return builder.get_enemy()

    @staticmethod
    def ShootingEnemy(builder, row: int):
        """Create and return a standard shooting enemy."""
        builder.reset()
        builder.set_raw(row)
        builder.set_bullets()
        builder.set_reward()
        return builder.get_enemy()

    @staticmethod
    def RandomEnemy(builder, row: int, radius_mult: float = 1,
                    shield_probability: float = 0.15, shooting_probability: float = 0.15):
        """Create and return an enemy. Enemy strength can be regulate with shield_probability and
        shooting_probability parameters"""
        assert isinstance(row, int) and (isinstance(radius_mult, int) or isinstance(radius_mult, float)) and \
            (isinstance(shield_probability, int) or isinstance(shield_probability, float)) and \
            (isinstance(shooting_probability, int) or isinstance(shooting_probability, float)) and \
            0 <= shield_probability <= 1 and 0 <= shooting_probability <= 1
        builder.reset()
        builder.set_raw(row)
        builder.set_radius(settings.enemy_radius * radius_mult)
        if randint(0, 100) <= shield_probability * 100:
            builder.set_shield()
        if randint(0, 100) <= shooting_probability * 100:
            builder.set_bullets()
        builder.set_reward()
        return builder.get_enemy()


class EnemyBuilder:
    def __init__(self):
        self.__enemy = Enemy()
        self.shield_thickness = settings.shield_thickness

    def reset(self):
        self.__enemy = Enemy()

    def get_enemy(self):
        return self.__enemy

    # options
    def set_raw(self, row):
        self.__enemy.raw = row

    def set_radius(self, radius: int):
        assert (isinstance(radius, int) or isinstance(radius, float)) and radius > 0
        self.__enemy.radius = int(radius)
        self.__enemy.set_lifes()

    def set_reward(self):
        self.__enemy.set_reward()

    def set_bullets(self, bullet_type: str = 'EnemyBullet'):
        self.__enemy.bullet_type = bullet_type
        self.__enemy.shoot_freq = settings.innerFPS / settings.BulletPerSecond[self.__enemy.bullet_type]
        self.__enemy.shoot_frame_cnt = randint(0, 100) % self.__enemy.shoot_freq

    def set_shield(self, shield_thickness: float = None) -> None:
        if shield_thickness is None:
            self.__enemy.shield_thickness = self.shield_thickness
        else:
            self.__enemy.shield_thickness = int(shield_thickness)
        self.__enemy.set_lifes()


class Enemy(Sprite):
    """Класс, представляющий одного пришельца."""

    def __init__(self, row=0):
        """Инициализирует пришельца и задает его начальную позицию."""
        super().__init__()
        self.screen = screen
        self.settings = settings

        # enemy base parameters
        self.radius = randint(settings.enemy_radius // 2, settings.enemy_radius)
        # life is area of ball (in pixels^2 of course)
        self.life = self.radius * self.radius * 3.14
        # reward for killing this enemy. It is equal to self.life point in the begin
        self.reward = self.life
        self.color = settings.enemy_color
        self.speed_x = settings.enemy_horizontal_speed
        self.speed_y = uniform(0, settings.enemy_vertical_speed)
        self.direction = -1

        self.shield_thickness = 0
        self.shield_life = 0
        self.bullet_type = None
        self.shoot_freq = None
        self.shoot_frame_cnt = None

        # Сохранение точной позиции of enemy ball.
        self.cx = settings.battle_screen_width - self.radius * 2
        self.cy = float(self.radius)

        self.row = row

    def check_edges(self):
        """Возвращает True, если пришелец находится у края экрана."""
        height = self.settings.battle_screen_height
        if height - self.radius <= self.cy:
            self.direction *= -1
            self.cy = height - self.radius
        elif self.cy <= self.radius:
            self.direction *= -1
            self.cy = self.radius

    def update(self):
        self.cx -= self.speed_x
        self.cy += self.speed_y * self.direction

    def draw(self):
        """Выводит пришельца в текущем положении."""
        coordinates = (int(self.cx), int(self.cy))
        draw.circle(screen, settings.enemy_shield_color, coordinates, self.radius + self.shield_thickness)
        draw.circle(screen, self.color, coordinates, self.radius)

    def set_reward(self):
        self.reward = self.life + self.shield_life
        # reward add if enemy can shoot is equivalent to his full life
        # The meaning of it is that enemy with bigger life shoot bigger amount of bullets
        if self.bullet_type is not None:
            self.reward += self.life + self.shield_life

    def set_radiuses(self):
        """Set enemy shield and body radiuses (uses after bullet smashed enemy)"""
        if self.life > 0:
            self.radius = int(math.sqrt(self.life / 3.14))
            if self.shield_life:
                self.shield_thickness = int(math.sqrt(self.shield_life / 20))
            else:
                self.shield_thickness = 0
        else:
            self.radius = 0
            self.shield_life = 0
            self.shield_thickness = 0

    def set_lifes(self):
        """Set enemy shield and body radiuses (uses after bullet smashed enemy)"""
        if self.radius > 0:
            self.life = self.radius ** 2 * 3.14
            if self.shield_thickness > 0:
                self.shield_life = self.shield_thickness * self.shield_thickness * 20
                assert self.shield_life >= 0
        else:
            self.life = 0
            self.shield_life = 0
            self.shield_thickness = 0

    def fire_bullet(self, bullets):
        """"Create an bullet if frame number is big enough."""
        if self.bullet_type is not None:
            assert self.shoot_freq >= 1
            if self.shoot_frame_cnt >= self.shoot_freq:
                self.shoot_frame_cnt -= self.shoot_freq
                bullets.add(settings.bullet_constructors[self.bullet_type](self))
            self.shoot_frame_cnt += 1

    def receive_damage(self, bullets, bullet):
        """Control how enemies receive damage from bullets"""
        if bullet.father == 'Hero':
            if self.shield_life > 0:
                self.shield_life -= bullet.damage
                if self.shield_life <= 0:
                    self.life += self.shield_life
                    self.shield_life = 0
            else:
                self.life -= bullet.damage
            self.set_radiuses()
            bullets.remove(bullet)
