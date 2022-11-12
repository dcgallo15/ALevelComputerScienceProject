import pygame
from screen import Screen
from object import Object

from level import testLevel


def main() -> int:
    global testLevel
    gameRunning: bool = True

    pygame.init()
    # basic width and height values are passed in these will be changed later
    screen = Screen(640, 480)
    screen.parseLevel(testLevel)

    # This will loop will run throughout the playing of the level
    while gameRunning == True:
        # Event handling loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # For the quit button
                gameRunning = False

        screen.render()
        screen.clear()

    return 0


if __name__ == "__main__":
    main()
