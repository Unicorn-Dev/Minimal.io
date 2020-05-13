import traceback
from Application.system.game_functions import try_wrapper

def run_game():
    from Application.system.engine import Engine

    game = Engine()
    while True:  # Start the main loop for the game.
        try_wrapper(
            'Текущая игра была неожиданно прерванна. Нам жаль...',
            10, game.run, *()
        )


if __name__ == "__main__":
    try_wrapper(
        'Все ваши данные и прогресс в игре были уничтожены. Нам очень жаль...',
        1, run_game, *()
    )
