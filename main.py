import pygame
from screen import Screen
from object import Object, Player
from vector import Vector
from math import pi
import time

from level import testLevel


def main() -> int:
    global testLevel
    gameRunning: bool = True

    pygame.init()
    # basic width and height values are passed in these will be changed later
    screen = Screen(640, 480)
    player = Player(40, 40, 10, 10, (255, 0, 255), [])
    screen.attachObject(player)
    player.addForce(Vector(5, pi / 2))

    clock = pygame.time.Clock()

    # This will loop will run throughout the playing of the level
    while gameRunning == True:
        # Event handling loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # For the quit button
                gameRunning = False

        if clock.get_fps() > 0:
            deltaTime: float = (clock.get_time()) / clock.get_fps()
        else:
            deltaTime: float = 0

        player.processForces(deltaTime)
        screen.render()
        screen.clear()
        clock.tick(60)

    return 0


if __name__ == "__main__":
    main()
