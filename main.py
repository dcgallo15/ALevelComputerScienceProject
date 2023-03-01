import pygame
from screen import Screen
from object import Object, Player, Enemy
from animation import AnimationState, AnimationManager
from attack import Attack, BlockState
from vector import Vector
from UI import horizontalBar, pygameButton
from math import pi

from level import testLevel, level1, level2, level3, level4, level5


def main() -> int:
    global testLevel

    # Main variables initialisation
    gameRunning: bool = True
    state = AnimationState()
    blockState = BlockState()
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
    PL_BLOCKDOWNLEFT = pygame.image.load("img/BLOCKDOWNLEFT.png")
    PL_BLOCKDOWNRIGHT = pygame.image.load("img/BLOCKDOWNRIGHT.png")
    PL_BLOCKMIDDLELEFT = pygame.image.load("img/BLOCKMIDDLELEFT.png")
    PL_BLOCKMIDDLERIGHT = pygame.image.load("img/BLOCKMIDDLERIGHT.png")
    PL_BLOCKTOPLEFT = pygame.image.load("img/BLOCKTOPLEFT.png")
    PL_BLOCKTOPRIGHT = pygame.image.load("img/BLOCKTOPRIGHT.png")

    playerAttacks = [
        Attack(20, 10, blockState.MIDDLE, 1),  # Basic attack
        Attack(20, 10, blockState.TOP, 1),  # Top attack
        Attack(20, 10, blockState.BOTTOM, 1),  # Bottom attack
        Attack(30, 5, blockState.MIDDLE, 1),  # Long range lower damage
        Attack(15, 15, blockState.MIDDLE, 1),  # Short range higher damage
    ]

    enemyAttacks = [
        Attack(20, 10, blockState.MIDDLE, 2),  # Basic attack
        Attack(20, 10, blockState.TOP, 2),  # Top attack
        Attack(20, 10, blockState.BOTTOM, 2),  # Bottom attack
        Attack(30, 5, blockState.MIDDLE, 2),  # Long range lower damage
        Attack(15, 15, blockState.MIDDLE, 2),  # Short range higher damage
    ]

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
    player.initAnimStates(state.BLOCKDOWNLEFT, [PL_BLOCKDOWNLEFT])
    player.initAnimStates(state.BLOCKDOWNRIGHT, [PL_BLOCKDOWNRIGHT])
    player.initAnimStates(state.BLOCKMIDDLELEFT, [PL_BLOCKMIDDLELEFT])
    player.initAnimStates(state.BLOCKMIDDLERIGHT, [PL_BLOCKMIDDLERIGHT])
    player.initAnimStates(state.BLOCKTOPLEFT, [PL_BLOCKTOPLEFT])
    player.initAnimStates(state.BLOCKTOPRIGHT, [PL_BLOCKTOPRIGHT])
    # Attacks initialisation
    for attack in playerAttacks:
        player.initAttacks(attack)
    # player must be first object attached to the screen

    # TODO:
    # Finish adding the rest of the animations
    # Add more attacks

    # Enemy Setup:
    enemy = Enemy(400, 300, PL_IDLE0, [], 10)
    enemy.initAnimStates(state.RUNNINGLEFT, [
        PL_RUNNINGLEFT0, PL_RUNNINGLEFT1])
    enemy.initAnimStates(state.RUNNINGRIGHT,
                         [PL_RUNNINGRIGHT0, PL_RUNNINGRIGHT1])
    enemy.initAnimStates(state.ATTACKLEFT, [
                         PL_ATTACKLEFT0, PL_IDLE0, PL_ATTACKLEFT0])
    enemy.initAnimStates(state.ATTACKRIGHT, [
                         PL_ATTACKRIGHT0, PL_IDLE0, PL_ATTACKRIGHT0])
    for attack in enemyAttacks:
        enemy.initAttacks(attack)

    clock = pygame.time.Clock()

    playerHealthBar = horizontalBar(100, 20, 30, 0, (255, 0, 0))
    enemyHealthBar = horizontalBar(100, 20, 300, 0, (255, 0, 0))

    playerBlockBar = horizontalBar(100, 20, 30, 20, (0, 0, 255), 100)
    enemyBlockBar = horizontalBar(100, 20, 300, 20, (0, 0, 255))

    currentLevel: list = level1  # This will be changed throughout the start menu
    # Start screen logic
    startScreenRunning: bool = True
    startButton = pygameButton(100, 80, 100, 300, (0, 255, 0))
    quitButton = pygameButton(50, 40, 100, 100, (255, 0, 0))
    levelButtons = [pygameButton(30, 30, 300, 50, (0, 255, 0)),
                    pygameButton(30, 30, 300, 100, (0, 255, 0)),
                    pygameButton(30, 30, 300, 150, (0, 255, 0)),
                    pygameButton(30, 30, 300, 200, (0, 255, 0)),
                    pygameButton(30, 30, 300, 250, (0, 255, 0))]
    keybindsButton = pygameButton(70, 70, 290, 300, (255, 0, 255))
    screen.attachObject(startButton)
    screen.attachObject(quitButton)
    screen.attachObject(keybindsButton)
    for levelButton in levelButtons:
        screen.attachObject(levelButton)
    while startScreenRunning == True:
        # Event Handling:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                startScreenRunning = False
                gameRunning = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Left mouse button
                if event.button == 1:
                    mousePos = pygame.mouse.get_pos()
                    # If start button is clicked
                    if startButton.isClicked(mousePos[0], mousePos[1]) == True:
                        # Removes menu objects so they are not rendered on the game screen
                        screen.removeObject(startButton)
                        screen.removeObject(quitButton)
                        screen.removeObject(keybindsButton)
                        for levelButton in levelButtons:
                            screen.removeObject(levelButton)
                        startScreenRunning = False

                    # If quit button is clicked
                    if quitButton.isClicked(mousePos[0], mousePos[1]) == True:
                        # Game isn't run and the start screen also isnt run
                        startScreenRunning = False
                        gameRunning = False

                    for i in range(len(levelButtons)):
                        if levelButtons[i].isClicked(mousePos[0], mousePos[1]) == True:
                            if i == 0:
                                currentLevel = level1
                            elif i == 1:
                                currentLevel = level2
                            elif i == 2:
                                currentLevel = level3
                            elif i == 3:
                                currentLevel = level4
                            elif i == 4:
                                currentLevel = level5
                            print("Level:", i + 1)

                    if keybindsButton.isClicked(mousePos[0], mousePos[1]) == True:
                        print("""
                                Jump - W \n
                                Left - A \n
                                Right - D \n
                                Basic Attack - Left mouse button \n
                                Top Attack - W + Left mouse button \n
                                Bottom Attack - S + Left mouse button \n
                                Short Range Attack - Middle mouse button \n
                                Long Range Attack - Right mouse button \n
                                Top Block - C \n
                                Middle Block - V \n
                                Bottom Block - B \n
                                """)

        screen.render()

    # Attaches game screen objects
    screen.attachObject(player)
    screen.attachObject(enemy)
    screen.parseLevel(currentLevel)

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
                        if player.isStoodOnGround(currentLevel, screen.getWidth(), screen.getHeight()) == True:
                            player.addVelocity(
                                Vector(player.getSpeed() * player.getSpeed(), 3 * pi / 2))
                        keysDown.append("W")
                    # Down
                    elif event.key == pygame.K_s:
                        keysDown.append("S")

                    # BLOCKS
                    elif event.key == pygame.K_c:
                        player.setBlock(blockState.TOP)
                        if player.getFacingRight() == False:
                            player.setAnimState(state.BLOCKTOPLEFT)
                        else:
                            player.setAnimState(state.BLOCKTOPRIGHT)

                    elif event.key == pygame.K_v:
                        player.setBlock(blockState.MIDDLE)
                        if player.getFacingRight() == False:
                            player.setAnimState(state.BLOCKMIDDLELEFT)
                        else:
                            player.setAnimState(state.BLOCKMIDDLERIGHT)

                    elif event.key == pygame.K_b:
                        player.setBlock(blockState.BOTTOM)
                        if player.getFacingRight() == False:
                            player.setAnimState(state.BLOCKDOWNLEFT)
                        else:
                            player.setAnimState(state.BLOCKDOWNRIGHT)

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

                    elif event.key == pygame.K_w:
                        keysDown.remove("W")

                    # Block reset
                    elif event.key == pygame.K_c or event.key == pygame.K_v or event.key == pygame.K_b:
                        player.resetBlock()
                        player.setAnimState(state.IDLE)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if player.getFacingRight() == True:
                    player.setAnimState(state.ATTACKRIGHT)
                else:
                    player.setAnimState(state.ATTACKLEFT)
                # left mouse click
                if event.button == 1:
                    if "W" in keysDown:  # Top attack
                        player.setCurrentAttackIndex(1)
                    elif "S" in keysDown:  # Bottom attack
                        player.setCurrentAttackIndex(2)
                    else:
                        player.setCurrentAttackIndex(0)
                    player.toggleAttack()

                # Middle mouse button
                elif event.button == 2:
                    player.setCurrentAttackIndex(2)
                    player.toggleAttack()

                # Right mouse click
                elif event.button == 3:
                    player.setCurrentAttackIndex(3)  # Long range attack
                    player.toggleAttack()

            if event.type == pygame.MOUSEBUTTONUP:
                # Left mouse release
                if event.button == 1:
                    player.setAnimState(state.IDLE)

        # Attack Handling
        if player.attack(enemy) == True:
            enemy.setIncrementRecentHitTimer()

        # Resets the state when the block time has run out
        if player.getBlockTimer() >= player.getBlockTimeLimit():
            player.setAnimState(state.IDLE)

        # Player Gravity
        # When the player is not stood on ground then there will be a gravity velcoity added
        if player.isStoodOnGround(currentLevel, screen.getWidth(), screen.getHeight()) == False:
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
        if enemy.isStoodOnGround(currentLevel, screen.getWidth(), screen.getHeight()) == False:
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
        # Increments the block timer
        player.incrementBlockTimer(deltaTime)
        enemy.incrementBlockTimer(deltaTime)

        # Resets the velocities so that they can be recalculated each frame
        player.resetVelocities()
        enemy.resetVelocities()
        # Render UI elements
        playerHealthBar.setPercent(player.getHealth())
        enemyHealthBar.setPercent(enemy.getHealth())
        playerBlockBar.setPercent(100 -
                                  int(player.getBlockTimer() * player.getBlockTimeLimit()))
        enemyBlockBar.setPercent(100 -
                                 int(enemy.getBlockTimer() * enemy.getBlockTimeLimit()))
        playerHealthBar.render(screen.getPygameScreen())
        enemyHealthBar.render(screen.getPygameScreen())
        playerBlockBar.render(screen.getPygameScreen())
        enemyBlockBar.render(screen.getPygameScreen())
        screen.render()
        # Clears the screen
        screen.clear()
        clock.tick(60)

    # Game over or game won screen
    # First 'screen.resetObjects()'
    # Then add game won or game lost sprite

    return 0


if __name__ == "__main__":
    main()
