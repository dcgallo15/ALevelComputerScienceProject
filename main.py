import pygame
from screen import Screen
from object import Object


def main() -> int:
    gameRunning: bool = True

    pygame.init()
    # basic width and height values are passed in these will be changed later
    screen = Screen(640, 480)
    # Temporary object to test the rendering system
    tempObj = Object(20, 20, 10, 10, (255, 255, 255))
    screen.attachObject(tempObj)

    # This will loop will run throughout the playing of the level
    while gameRunning == True:
        screen.render()
        screen.clear()

    return 0


if __name__ == "__main__":
    main()
