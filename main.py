import pygame
# This will be used throughout to avoid importing pygame multiple times
from screen import Screen


def main() -> int:
    gameRunning: bool = True

    pygame.init()
    # basic width and height values are passed in these will be changed later
    screen = Screen(640, 480)

    # This will loop will run throughout the playing of the level
    while gameRunning == True:
        screen.clear()

    return 0


if __name__ == "__main__":
    main()
