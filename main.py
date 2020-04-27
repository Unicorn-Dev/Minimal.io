def run_game():
    from Application.system.engine import Engine

    game = Engine()
    while True:  # Start the main loop for the game.
        game.run()


if __name__ == "__main__":
    run_game()
