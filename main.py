import pygame
from screen import Screen
from object import Object, Player, Enemy
from animation import AnimationState, AnimationManager
from attack import Attack
from vector import Vector
from math import pi

from level import testLevel, level1


def main() -> int:
    global testLevel

    # Main variables initialisation
    gameRunning: bool = True
    state = AnimationState()
    keysDown = []  # keeps track of the keys that are pressed down

    # this will be used later and be controlled by the menu to ensure that
    # either arrow keys or WASD keys can be used by the player
    arrowKeys: bool = False

    pygame.init()

    # Player setup
    # Loading Player Images
    PL_IDLE0 = pygame.image.load("img/IDLE0.png")
    PL_RUNNINGRIGHT0 = pygame.image.load("img/RUNNINGRIGHT0.png")
    PL_RUNNINGRIGHT1 = pygame.image.load("img/RUNNINGRIGHT1.png")
    PL_RUNNINGLEFT0 = pygame.image.load("img/RUNNINGLEFT0.png")
    PL_RUNNINGLEFT1 = pygame.image.load("img/RUNNINGLEFT1.png")
    PL_ATTACKLEFT0 = pygame.image.load("img/ATTACKLEFT0.png")
    PL_ATTACKRIGHT0 = pygame.image.load("img/ATTACKRIGHT0.png")

    # basic width and height values are passed in these will be changed later
    screen = Screen(640, 480)
    player = Player(10, 0, PL_IDLE0, [], 20)
    #player.initAnimStates(state.IDLE, PL_IDLE0)
    player.initAnimStates(state.RUNNINGLEFT, [
                          PL_RUNNINGLEFT0, PL_RUNNINGLEFT1])
    player.initAnimStates(state.RUNNINGRIGHT,
                          [PL_RUNNINGRIGHT0, PL_RUNNINGRIGHT1])
    player.initAnimStates(state.ATTACKLEFT, [PL_ATTACKLEFT0, PL_IDLE0])
    player.initAnimStates(state.ATTACKRIGHT, [PL_ATTACKRIGHT0, PL_IDLE0])
    # Attacks initialisation
    # This attack will be executed when the player reaches back to it's IDLE state
    player.initAttacks(Attack(20, 10, 1))
    # player must be first object attached to the screen
    screen.attachObject(player)

    # TODO:
    # Finish adding the rest of the animations
    # Add more attacks

    # Enemy Setup:
    enemy = Enemy(400, 0, PL_IDLE0, [], 10)
    enemy.initAnimStates(state.RUNNINGLEFT, [
        PL_RUNNINGLEFT0, PL_RUNNINGLEFT1])
    enemy.initAnimStates(state.RUNNINGRIGHT,
                         [PL_RUNNINGRIGHT0, PL_RUNNINGRIGHT1])
    enemy.initAnimStates(state.ATTACKLEFT, [PL_ATTACKLEFT0, PL_IDLE0])
    enemy.initAnimStates(state.ATTACKRIGHT, [PL_ATTACKRIGHT0, PL_IDLE0])
    enemy.initAttacks(Attack(20, 10, 1))

    screen.attachObject(enemy)
    screen.parseLevel(level1)
    clock = pygame.time.Clock()

    # This will loop will run throughout the playing of the level
    while gameRunning == True:
        if clock.get_fps() > 0:  # ensures that velocity is dependent on time
            deltaTime: float = (clock.get_time()) / clock.get_fps()
        else:
            deltaTime: float = 0

        # Event handling loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # For the quit button
                gameRunning = False

            # Keyboard events:
            if arrowKeys == False:
                # Keydown
                # By appending and removing from a list this ensures that when keys are held down
                # the correct velocities are properly applied
                if event.type == pygame.KEYDOWN:
                    # Left
                    if event.key == pygame.K_a:
                        keysDown.append("A")
                        player.setFacingRight(False)
                        player.setAnimState(state.RUNNINGLEFT)
                    # Right
                    elif event.key == pygame.K_d:
                        keysDown.append("D")
                        player.setFacingRight(True)
                        player.setAnimState(state.RUNNINGRIGHT)
                    # Jump
                    elif event.key == pygame.K_w:
                        # Fixes infinite jump
                        # this makes it so that jump cannot be held down
                        if player.isStoodOnGround(level1, screen.getWidth(), screen.getHeight()) == True:
                            player.addVelocity(
                                Vector(player.getSpeed() * player.getSpeed(), 3 * pi / 2))
                    # Down
                    elif event.key == pygame.K_s:
                        keysDown.append("S")
                # Keyup
                elif event.type == pygame.KEYUP:
                    # Left
                    if event.key == pygame.K_a:
                        keysDown.remove("A")
                        if len(keysDown) == 0:
                            player.setAnimState(state.IDLE)
                    # Right
                    elif event.key == pygame.K_d:
                        keysDown.remove("D")
                        if len(keysDown) == 0:
                            player.setAnimState(state.IDLE)
                    # Down
                    elif event.key == pygame.K_s:
                        keysDown.remove("S")

            if event.type == pygame.MOUSEBUTTONDOWN:
                # left mouse click
                if event.button == 1:
                    if player.getFacingRight() == True:
                        player.setAnimState(state.ATTACKRIGHT)
                    else:
                        player.setAnimState(state.ATTACKLEFT)
                    player.setCurrentAttackIndex(0)
                    player.toggleAttack()

            if event.type == pygame.MOUSEBUTTONUP:
                # Left mouse release
                if event.button == 1:
                    player.setAnimState(state.IDLE)

        # Attack Handling
        player.attack(enemy)

        # Player Gravity
        # When the player is not stood on ground then there will be a gravity velcoity added
        if player.isStoodOnGround(level1, screen.getWidth(), screen.getHeight()) == False:
            # When the player is stood on top of the enemy there will be no gravity added
            # This acts as a reaction force from the enemy and stops the player from falling through the enemy
            if player.collidesObjectY(enemy) == False:
                # Gravity Velocity
                player.addVelocity(Vector(player.getSpeed(), pi / 2))

        # Adds player movement vectors
        # Checks which keys are in the list and are held down
        if "S" in keysDown:
            pass  # CROUCH
        if "A" in keysDown:
            player.addVelocity(Vector(player.getSpeed(), pi))
        if "D" in keysDown:
            player.addVelocity(Vector(player.getSpeed(), 0))

        # If any keys have been pressed
        if len(keysDown) > 0:
            player.collidesObjectX(enemy)
            screen.objectCollsion(player)
        screen.objectCollsion(enemy)
        # NOTE: enemy will not collide yet
        # NOTE: enemy can push player through blocks

        player.stopAtBounds(screen.getWidth(), screen.getHeight())
        enemy.stopAtBounds(screen.getWidth(), screen.getHeight())

        # Enemy Gravity
        if enemy.isStoodOnGround(level1, screen.getWidth(), screen.getHeight()) == False:
            # Gravity Velocity
            enemy.addVelocity(Vector(enemy.getSpeed(), pi / 2))

        enemy.moveTowardsPlayer(player)
        enemy.attackPlayer(player, deltaTime)
        player.resolveVelocities(deltaTime)
        enemy.resolveVelocities(deltaTime)

        # Progress the animation every 2 seconds
        player.nextAnimation(2)
        enemy.nextAnimation(2)
        # Increments the animation timer counter
        player.incrementAnimCounter(deltaTime)
        enemy.incrementAnimCounter(deltaTime)

        # Resets the velocities so that they can be recalculated each frame
        player.resetVelocities()
        enemy.resetVelocities()
        # Renders the attached objects
        screen.render()
        # Clears the screen
        screen.clear()
        clock.tick(60)

    return 0


if __name__ == "__main__":
    main()
