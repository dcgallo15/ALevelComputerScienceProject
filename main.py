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

    # Standard Velocities
    playerSpeed: int = 5
    playerLeft = Vector(playerSpeed, pi)
    playerRight = Vector(playerSpeed, 0)
    playerUp = Vector(playerSpeed, 3 * pi / 2)
    playerDown = Vector(playerSpeed, pi / 2)

    arrowKeys: bool = False

    pygame.init()
    # basic width and height values are passed in these will be changed later
    screen = Screen(640, 480)
    player = Player(40, 40, 10, 10, (255, 0, 255), [])
    screen.attachObject(player)
    clock = pygame.time.Clock()

    # This will loop will run throughout the playing of the level
    while gameRunning == True:
        # Event handling loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # For the quit button
                gameRunning = False

            # Keyboard events:
            if arrowKeys == False:
                # Keydown
                if event.type == pygame.KEYDOWN:
                    # Left
                    if event.key == pygame.K_a:
                        player.addVelocity(playerLeft)
                    # Right
                    elif event.key == pygame.K_d:
                        player.addVelocity(playerRight)
                    # Up
                    elif event.key == pygame.K_w:
                        player.addVelocity(playerUp)
                    # Down
                    elif event.key == pygame.K_s:
                        player.addVelocity(playerDown)
                # Keyup
                elif event.type == pygame.KEYUP:
                    # Left
                    if event.key == pygame.K_a:
                        player.removeVelocity(playerLeft)
                    # Right
                    elif event.key == pygame.K_d:
                        player.removeVelocity(playerRight)
                    # Up
                    elif event.key == pygame.K_w:
                        player.removeVelocity(playerUp)
                    # Down
                    elif event.key == pygame.K_s:
                        player.removeVelocity(playerDown)

        if clock.get_fps() > 0:
            deltaTime: float = (clock.get_time()) / clock.get_fps()
        else:
            deltaTime: float = 0

        player.resolveVelocities(deltaTime)
        screen.render()
        screen.clear()
        clock.tick(60)

    return 0


if __name__ == "__main__":
    main()
