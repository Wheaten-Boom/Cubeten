import sys

import level_runner
import main_menu


def main() -> None:
    level, screen = main_menu.main_menu()
    if level is None or screen is None:
        sys.exit()
    level_runner.run_level(level, screen)


if __name__ == "__main__":
    main()
