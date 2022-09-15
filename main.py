import sys

import level_runner
import main_menu

if __name__ == "__main__":
    level, screen = main_menu.main_menu()
    if level is None or screen is None:
        sys.exit()
    level_runner.run_level(level, screen)
