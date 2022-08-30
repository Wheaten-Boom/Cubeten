import json
import pygame
from pygame.locals import *
import os
import level_loader


if __name__ == "__main__":
    level, screen = main_menu.main_menu()
    if level is None or screen is None:
        quit()
    level_runner.run_level(level, screen)
