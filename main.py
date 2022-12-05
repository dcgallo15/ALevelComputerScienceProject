import pygame
from screen import Screen
from object import Object, Player
from vector import Vector
from math import pi

from level import testLevel, level1


def main() -> int:
    global testLevel

    # Main variables initialisation
    gameRunning: bool = True
    keysDown = []
    arrowKeys: bool = False

    pygame.init()
    # basic width and height values are passed in these will be changed later
    screen = Screen(640, 480)
    player = Player(40, 40, 10, 10, (255, 0, 255), [], 20, True)
    # NOTE: player must be first object attached to the screen
    screen.attachObject(player)
    screen.parseLevel(level1)
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
            if player.isStoodOnGround(level1, screen.getWidth(), screen.getHeight()) == True:
                player.addVelocity(
                    Vector(player.getSpeed() * player.getSpeed(), 3 * pi / 2))
        if "S" in keysDown:
            pass  # CROUCH
        if "A" in keysDown:
            player.addVelocity(Vector(player.getSpeed(), pi))
        if "D" in keysDown:
            player.addVelocity(Vector(player.getSpeed(), 0))

        player.stopAtBounds(screen.getWidth(), screen.getHeight())

        if player.isStoodOnGround(level1, screen.getWidth(), screen.getHeight()) == False:
            player.addVelocity(Vector(player.getSpeed(), pi / 2))  # Gravity

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
