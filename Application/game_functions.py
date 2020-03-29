import sys
import pygame
from Application.bullet import Bullet


def check_events(settings, screen, unicorn, bullets):
    """Respond to key presses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_key_down_events(event, settings, screen, unicorn, bullets)
        elif event.type == pygame.KEYUP:
            check_key_up_events(event, unicorn)


def check_key_down_events(event, settings, screen, unicorn, bullets):
    """Respond to key presses."""
    if event.key == pygame.K_SPACE:
        fire_bullet(settings, screen, unicorn, bullets)
    if event.key == pygame.K_UP:
        unicorn.moving_up = True
    elif event.key == pygame.K_DOWN:
        unicorn.moving_down = True


def check_key_up_events(event, unicorn):
    """Respond to key presses."""
    if event.key == pygame.K_UP:
        unicorn.moving_up = False
    elif event.key == pygame.K_DOWN:
        unicorn.moving_down = False


def fire_bullet(settings, screen, unicorn, bullets):
    if len(bullets) < settings.bullets_limit:
        new_bullet = Bullet(settings, screen, unicorn)
        bullets.add(new_bullet)


def update_bullets(bullets, settings):
    """Обновляет позиции пуль и уничтожает старые пули."""
    # Обновление позиций пуль.
    bullets.update()
    # Удаление пуль, вышедших за край экрана.
    for bullet in bullets.copy():
        if bullet.rect.left > settings.screen_width:
            bullets.remove(bullet)


def update_screen(settings, screen, unicorn, bullets):
    """Update images on the screen and flip to the new screen."""
    # Redraw the screen during each pass through the loop.
    screen.fill(settings.bg_color)

    unicorn.draw()  # Redraw unicorn.

    # Redraw all bullets behind unicorn and aliens.
    for bullet in bullets.sprites():
        bullet.draw()

    # Make the most recently drawn screen visible.
    pygame.display.flip()
