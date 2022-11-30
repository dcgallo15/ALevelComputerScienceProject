import pygame
from screen import Screen
from object import Object, Player
from vector import Vector
from math import pi

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

    keysDown = []

    arrowKeys: bool = False

    pygame.init()
    # basic width and height values are passed in these will be changed later
    screen = Screen(640, 480)
    player = Player(40, 40, 10, 10, (255, 0, 255), [], playerSpeed, True)
    print(player.getCollision())
    # NOTE: player must be first object attached to the screen
    screen.attachObject(player)
    tempObject = Object(10, 10, 100, 100, (255, 0, 255), True)
    screen.attachObject(tempObject)
    tempObject2 = Object(150, 200, 300, 300, (255, 0, 255), True)
    screen.attachObject(tempObject2)
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
                        keysDown.append("A")
                    # Right
                    elif event.key == pygame.K_d:
                        keysDown.append("D")
                    # Up
                    elif event.key == pygame.K_w:
                        keysDown.append("W")
                    # Down
                    elif event.key == pygame.K_s:
                        keysDown.append("S")
                # Keyup
                elif event.type == pygame.KEYUP:
                    # Left
                    if event.key == pygame.K_a:
                        keysDown.remove("A")
                    # Right
                    elif event.key == pygame.K_d:
                        keysDown.remove("D")
                    # Up
                    elif event.key == pygame.K_w:
                        keysDown.remove("W")
                    # Down
                    elif event.key == pygame.K_s:
                        keysDown.remove("S")

        if "W" in keysDown:
            player.addVelocity(playerUp)
        if "S" in keysDown:
            player.addVelocity(playerDown)
        if "A" in keysDown:
            player.addVelocity(playerLeft)
        if "D" in keysDown:
            player.addVelocity(playerRight)

        player.stopAtBounds(screen.getWidth(), screen.getHeight())
        screen.objectCollsion()

        if clock.get_fps() > 0:
            deltaTime: float = (clock.get_time()) / clock.get_fps()
        else:
            deltaTime: float = 0

        player.resolveVelocities(deltaTime)
        player.resetVelocities()
        screen.render()
        screen.clear()
        clock.tick(60)

    return 0


if __name__ == "__main__":
    main()
