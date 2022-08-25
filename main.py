import main_menu
import level_runner


if __name__ == "__main__":
    level, screen = main_menu.main_menu()
    if level is None or screen is None:
        quit()
    level_runner.run_level(level, screen)
