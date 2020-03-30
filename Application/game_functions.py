import sys
import pygame
from Application.powerball import Powerball


def check_events(settings, screen, unicorn, powerballs):
    """Respond to key presses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_key_down_events(event, settings, screen, unicorn, powerballs)
        elif event.type == pygame.KEYUP:
            check_key_up_events(event, unicorn)


def check_key_down_events(event, settings, screen, unicorn, powerballs):
    """Respond to key presses."""
    if event.key == pygame.K_SPACE:
        fire_powerball(settings, screen, unicorn, powerballs)
    if event.key == pygame.K_UP:
        unicorn.moving_up = True
    elif event.key == pygame.K_DOWN:
        unicorn.moving_down = True
    elif event.key == pygame.K_LEFT:
        unicorn.moving_left = True
    elif event.key == pygame.K_RIGHT:
        unicorn.moving_right = True

def check_key_up_events(event, unicorn):
    """Respond to key unpresses."""
    if event.key == pygame.K_UP:
        unicorn.moving_up = False
    elif event.key == pygame.K_DOWN:
        unicorn.moving_down = False
    elif event.key == pygame.K_LEFT:
        unicorn.moving_left = False
    elif event.key == pygame.K_RIGHT:
        unicorn.moving_right = False

def fire_powerball(settings, screen, unicorn, powerballs):
    if len(powerballs) < settings.powerballs_limit:
        new_powerball = Powerball(settings, screen, unicorn)
        powerballs.add(new_powerball)


def update_powerballs(powerballs, settings):
    """Обновляет позиции пуль и уничтожает старые пули."""
    # Обновление позиций пуль.
    powerballs.update()
    # Удаление пуль, вышедших за край экрана.
    for powerball in powerballs.copy():
        if powerball.rect.left > settings.screen_width:
            powerballs.remove(powerball)


def update_screen(settings, screen, unicorn, powerballs):
    """Update images on the screen and flip to the new screen."""
    # Redraw the screen during each pass through the loop.
    screen.fill(settings.bg_color)

    unicorn.draw()  # Redraw unicorn.

    # Redraw all powerballs behind unicorn and aliens.
    for powerball in powerballs.sprites():
        powerball.draw()

    # Make the most recently drawn screen visible.
    pygame.display.flip()
