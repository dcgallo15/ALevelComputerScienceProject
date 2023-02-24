from math import atan, tan, sqrt, pi
from random import randint
from vector import Vector
from animation import AnimationState, AnimationManager
from attack import Attack, BlockState


class Object():
    def __init__(self, width: int, height: int, xPos: int, yPos: int, color: tuple, collision: bool = False) -> None:
        # Variable Initialisation
        self._w = width
        self._h = height
        self.__xPos = xPos
        self.__yPos = yPos
        self.__color = color
        self.__collision = collision

    def getWidth(self) -> int:
        return self._w

    def getHeight(self) -> int:
        return self._h

    def getXPos(self) -> int:
        return self.__xPos

    def getYPos(self) -> int:
        return self.__yPos

    def getColor(self) -> tuple:
        return self.__color

    def getCollision(self) -> bool:
        return self.__collision

    # Tranlates the player by a vector
    def translate(self, vec: Vector) -> None:
        self.__xPos += vec.getX()
        self.__yPos += vec.getY()

    # This method is for when the player is to be translated by an amount that is not in vector form
    def translateCartesian(self, x: int, y: int) -> None:
        self.__xPos += x
        self.__yPos += y

    # If this object is printed (for testing)
    def __repr__(self) -> str:
        return ("OBJECT WIDTH: " + str(self.__w) + " OBJECT HEIGHT: " + str(self.__h))


class Player(Object):
    # the sprite passed in here is the first sprite that the player will be rendered as
    # it will be added to the IDLE list in the animation manager
    def __init__(self, xPos: int, yPos: int, sprite, velocities: list, speed: int) -> None:
        self.__speed = speed
        self.__velocities = velocities  # List of Vector objects

        state = AnimationState()
        self.__playerAnimManager = AnimationManager()
        self.__playerAnimCounter: float = 0
        self.__playerAnimManager.setupStates(state.IDLE, [sprite])
        self.__playerAnimManager.setAnimation(
            state.IDLE)  # Start in IDLE state
        # Start in first IDLE animation
        self.__sprite = sprite
        # Calls object's constructor
        super().__init__(self.__sprite.get_width(), self.__sprite.get_height(),
                         xPos, yPos, (255, 255, 255), True)

        self.__attacks: list = []
        self.__facingRight: bool = True  # This is so that the attack directions are correct
        self.__health: int = 100
        self.__isAttacking = False
        self.__block: BlockState = BlockState().NONE
        self.__blockTimer: float = 0
        self.__blockTimeLimit: float = 10
        # Protected:
        self._collisionX: bool = False

    # Takes in all the attacks that the player can perform
    def initAttacks(self, *args: Attack) -> None:
        for attack in args:
            self.__attacks.append(attack)

    def getFacingRight(self) -> bool:
        return self.__facingRight

    def setFacingRight(self, right: bool) -> None:
        self.__facingRight = right

    def decrementHealth(self, damage: int) -> None:
        self.__health -= damage
        if self.__health <= 0:
            print("Game Over")

    def getHealth(self) -> int:
        return self.__health

    def getBlock(self) -> BlockState:
        return self.__block

    def setBlock(self, blockState: BlockState) -> None:
        self.__block = blockState

    def incrementBlockTimer(self, deltaTime: float) -> None:
        if self.__block == BlockState().NONE and self.__blockTimer > 0:
            self.__blockTimer -= deltaTime  # When not blocking the timer increases
        elif self.__blockTimer < self.__blockTimeLimit:
            self.__blockTimer += deltaTime

    def getBlockTimer(self) -> float:
        return self.__blockTimer

    def getBlockTimeLimit(self) -> float:
        return self.__blockTimeLimit

    def resetBlock(self) -> None:
        self.__block = BlockState().NONE

    def getAttacks(self):
        return self.__attacks

    # Will perform the attack move
    # This will check if the player instance passed in will be affected by this attack
    def attack(self, player) -> bool:
        # Check if an attack should be carried out
        if self.getIsAttacking() == True:
            # Assigns the current attack
            currentAttack: Attack = self.getAttacks()[
                self.getCurrentAttackIndex()]
            if player.getBlock() == currentAttack.getAttackPoint() and player.getBlockTimer() < player.getBlockTimeLimit():
                print("ATTACK BLOCKED")
                return False
            # Check if animation is in correct state
            if self.__playerAnimManager.getCounter() == currentAttack.getTriggerIndex():
                # Check if the player is within vertical range of the object passed in
                if self.getYPos() in range(player.getYPos() - player.getHeight(), player.getYPos()):
                    if self.__facingRight == True:
                        # Checks if the right side of the player is within attack range of the enemy
                        if self.getXPos() + self.getWidth() in range(player.getXPos(),
                                                                     player.getXPos() + currentAttack.getRange()):
                            # If it is then subtract the attack's health cost
                            player.decrementHealth(
                                currentAttack.getHealthCost())
                            # To track changes in health
                            print(player.getHealth())
                            return True
                    else:
                        # Checks if the left side of the player is within attack range of the enemy
                        # Bug fix here that ensures range is properly calculated
                        if self.getXPos() - currentAttack.getRange() in range(player.getXPos(),
                                                                              player.getXPos() + player.getWidth()):
                            player.decrementHealth(
                                currentAttack.getHealthCost())
                            # To track changes in health
                            print(player.getHealth())
                            return True
                # The attack has been carried out
                self.toggleAttack()

    def setCurrentAttackIndex(self, index: int) -> None:
        self.__currentAttackIndex = index

    def getCurrentAttackIndex(self) -> int:
        return self.__currentAttackIndex

    def toggleAttack(self) -> None:
        # Will change isAttacking to False when True and True when False
        self.__isAttacking = not self.__isAttacking

    def getIsAttacking(self) -> bool:
        return self.__isAttacking

    def getCurrentAttack(self) -> Attack:
        return self.__attacks[self.__currentAttackIndex]

    # Animation Manager Methods:
    def initAnimStates(self, state: AnimationState, animations: list) -> None:
        self.__playerAnimManager.setupStates(state, animations)

    def setAnimState(self, state: AnimationState) -> None:
        self.__playerAnimManager.setAnimation(state)

    def _getAnimManager(self) -> AnimationManager:
        return self.__playerAnimManager

    # Checks the time since the change of the last animation
    # It will chnage animation if the duration is larger than the time passed in
    def nextAnimation(self, time: int) -> None:
        if self.__playerAnimCounter > time:
            self.__playerAnimManager.changeState()
            self.__sprite = self.__playerAnimManager.getCurrentAnimation()
            # Resets the animation counter
            self.__playerAnimCounter = 0

    def incrementAnimCounter(self, amount: float) -> None:
        self.__playerAnimCounter += amount

    def getAnimCounter(self) -> float:
        return self.__playerAnimCounter

    def getAnimIndex(self) -> int:
        # Returns the index of the list that the animation is on
        return self.__playerAnimManager.getCounter()

    # This method will add another velocity to the end of the list
    def addVelocity(self, vel: Vector) -> None:
        self.__velocities.append(vel)

    def resetVelocities(self) -> None:
        self.__velocities = []

    def getVelocities(self) -> list:
        return self.__velocities

    def getSprite(self):
        return self.__sprite

    def resolveVelocities(self, deltaTime: int) -> None:
        totalX: int = 0
        totalY: int = 0
        # Sums each of the X and Y components
        for i in range(len(self.__velocities)):
            totalX += self.__velocities[i].getX()
            totalY += self.__velocities[i].getY()
        # Translates the player in the direction of these velocities multiplied by the change in time
        self.translateCartesian(int(totalX * deltaTime),
                                int(totalY * deltaTime))

    def getSpeed(self) -> int:
        return self.__speed

    def stopAtBounds(self, width: int, height: int) -> None:
        # if the player is trying to go past any bounds of the screen then an opposite velocity is applied
        # Top bound
        if self.getYPos() <= 0:
            self.addVelocity(Vector(self.__speed, -1 * 3 * pi / 2))
        # Bottom Bound
        elif self.getYPos() + self.getHeight() >= height:
            self.addVelocity(Vector(self.__speed, -1 * pi / 2))
        # Left Bound
        if self.getXPos() <= 0:
            self.addVelocity(Vector(self.__speed, 0))
        # Right Bound
        elif self.getXPos() + self.getWidth() >= width:
            self.addVelocity(Vector(self.__speed, pi))

    # This procedure will handle only horizontal collisions
    def collidesObjectX(self, obj: Object) -> None:
        # This causes the object to push the player when the player isn't moving
        # So this is only called when the player is pressing a movement key
        # This change ensures that bounds properly work
        # Player's speed is subtracted to stop weird clipping
        if self.getYPos() in range(obj.getYPos(), obj.getYPos() + obj.getHeight() - self.getSpeed()) or obj.getYPos() in range(self.getYPos(), self.getYPos() + self.getHeight() - self.getSpeed()):
            # The // 2 is to determine which side the player is on of the object so that an opposite velocity can be properly applied
            # Moves the player right since the left side has collided
            if self.getXPos() in range(obj.getXPos() + (obj.getWidth() // 2), obj.getXPos() + obj.getWidth()):
                self.addVelocity(Vector(self.__speed, 0))
                self._collisionX = True
            # Moves the player left since the right side has collided
            if self.getXPos() + self.getWidth() in range(obj.getXPos(), obj.getXPos() + (obj.getWidth() // 2)):
                self.addVelocity(Vector(self.__speed, pi))
                self._collisionX = True

    def collidesObjectY(self, obj: Object) -> bool:
        # Checks if the X of the player is within the X of the Enemy
        # This accounts for both the player's and Object's widths
        if self.getXPos() in range(obj.getXPos(), obj.getXPos() + obj.getWidth()) or self.getXPos() + self.getWidth() in range(obj.getXPos(), obj.getXPos() + obj.getWidth()):
            # If the player's Y from the bottom of the player is within the range of the Object's Height
            if self.getYPos() + self.getHeight() in range(obj.getYPos(), obj.getYPos() + obj.getHeight()):
                return True
        return False

    def isStoodOnGround(self, level: list, width: int, height: int) -> bool:
        # Check the positions of the platforms placed in the level
        # then compare these with player positions to see if the player
        # is stood on them
        objWidth = (width / len(level[0]))
        objHeight = (height / len(level))
        for y in range(len(level)):
            for x in range(len(level[0])):
                if level[y][x] != "0":
                    # recalculates the postion of each platform
                    objXpos = (objWidth) * x
                    objYpos = (objHeight) * y
                    # For more consistency in the loops
                    for i in range(int(objWidth)):
                        for j in range(int(objHeight)):
                            # checks if the player is stood on the platforms
                            # checks if both the height and width are in range
                            if self.getYPos() + self.getHeight() == objYpos + j and (self.getXPos() + i == objXpos or self.getXPos() - (self.getWidth() // 2) + i == objXpos):
                                # added the addition or to fix overhang bug and the player falling into the floor
                                return True
        return False


class Enemy(Player):
    def __init__(self, xPos: int, yPos: int, sprite, velocities: list, speed: int) -> None:
        super().__init__(xPos, yPos,
                         sprite, velocities, speed)
        # This will control if the enemy should find the player or avoid them
        self.__find: bool = True
        self.__currentAnimState: AnimationState = AnimationState().IDLE
        self.__attackTimer: float = 0
        # This will track the time since the enemy has last been hit by the player has been no hits at start so set to a very large number
        self.__recentHitTimer: float = 10000
        self.__incrementingRecentHitTimer: bool = False

    # This will more the enemy in the direction of the player but is one dimensional and only takes
    # into account the horizontal direction
    def moveTowardsPlayer(self, player: Player):
        state = AnimationState()
        endPos = (player.getXPos(), player.getYPos())
        currentPos = (self.getXPos(), self.getYPos())

        # This takes into account of the X direction
        xDistance = ((endPos[0] - currentPos[0]))

        # Doesn't move when attacking or animations cancelled
        if self.getIsAttacking() == True:
            return

        # This ensures that the enemy does not walk into the player
        # However, this does not ensure that the player cannot walk into the enemy
        if sqrt(xDistance ** 2) < self.getWidth():
            if self.__currentAnimState != state.IDLE:  # Resets Animation state when next to the player
                self.setAnimState(state.IDLE)
                self.__currentAnimState = state.IDLE
            return

        # Will check if the enemy should move towards the player in the X direction
        # Calculates the correct direction to move
        if self._collisionX == True:
            # Jump
            self.addVelocity(
                Vector(self.getSpeed() * self.getSpeed(), 3 * pi / 2))
            # After the jump has been completed this ensures that another jump is not repeated
            if self.__currentAnimState != state.IDLE:
                self.setAnimState(state.IDLE)
                self.__currentAnimState = state.IDLE
            self._collisionX = False
            return

        if xDistance < 0:
            if self.__find == True:
                self.addVelocity(Vector(self.getSpeed(), pi))
                if self.__currentAnimState != state.RUNNINGLEFT:
                    self.setAnimState(state.RUNNINGLEFT)
                    self.__currentAnimState = state.RUNNINGLEFT
                self.setFacingRight(False)
                return

            if self.__find == False:
                self.addVelocity(Vector(self.getSpeed(),  0))
                if self.__currentAnimState != state.RUNNINGRIGHT:
                    self.setAnimState(state.RUNNINGRIGHT)
                    self.__currentAnimState = state.RUNNINGRIGHT
                self.setFacingRight(True)
                return

        else:
            if self.__find == True:
                self.addVelocity(Vector(self.getSpeed(),  0))
                if self.__currentAnimState != state.RUNNINGRIGHT:
                    self.setAnimState(state.RUNNINGRIGHT)
                    self.__currentAnimState = state.RUNNINGRIGHT
                self.setFacingRight(True)
                return

            # Bug fix
            if self.__find == False:
                self.addVelocity(Vector(self.getSpeed(), pi))
                if self.__currentAnimState != state.RUNNINGLEFT:
                    self.setAnimState(state.RUNNINGLEFT)
                    self.__currentAnimState = state.RUNNINGLEFT
                self.setFacingRight(False)
                return
        return

    def __selectAttackAnimationState(self):
        state = AnimationState()
        if self.getFacingRight() == False:
            if self.__currentAnimState != state.ATTACKLEFT:
                self.setAnimState(state.ATTACKLEFT)
                self.__currentAnimState = state.ATTACKLEFT
        else:
            if self.__currentAnimState != state.ATTACKRIGHT:
                self.setAnimState(state.ATTACKRIGHT)
                self.__currentAnimState = state.ATTACKRIGHT

    def setIncrementRecentHitTimer(self) -> None:
        self.__incrementingRecentHitTimer = True
        # Timer starts at 0
        self.__recentHitTimer = 0

    # Will control wether the enemy attempts to find the player or not
    def __setFind(self, playerHealth: int, playerBlockTimer: float, playerBlockTime: float):
        # If the enemy is on very low health but players health is much higher set find to false
        if self.getHealth() < 20 and playerHealth > 40:
            self.__find = False
            return

        # If the enemy block timer is low and player has more than half their block set find to false
        if self.getBlockTimer() < self.getBlockTimeLimit() * 0.2 and playerBlockTimer > playerBlockTime * 0.5:
            self.__find = False
            return

        # If there has been a recent hit set find to false
        if self.__recentHitTimer < 10:
            self.__find = False
            return

        else:
            self.__find = True

    # This will set the current attack index
    # TODO: Code the attack selection algorithm
    def __selectAttack() -> int:  # Will return an int from 0 -> 4
        # 0 is basic attack
        # 1 is top attack
        # 2 is bottom attack
        # 3 is long range attack
        # 4 is short range attack

        pass

    def attackPlayer(self, player: Player, deltatime: float, playerPrevAttack: Attack):
        if self.__incrementingRecentHitTimer == True:
            self.__recentHitTimer += deltatime
        self.__attackTimer += deltatime
        # Selects the attack:
        #currentAttack: Attack = self.getAttacks()[self.__selectAttack]
        self.setCurrentAttackIndex(0)
        currentAttack: Attack = self.getAttacks()[self.getCurrentAttackIndex()]

        self.__setFind(player.getHealth(), player.getBlockTimer(),
                       player.getBlockTimeLimit())

        # Determines whether player is within range of enemy
        # Vertical Range:
        # If top of enemy between half of player and top of the player
        # Or if top of player between half of enemy and top of enemy
        if (self.getYPos() in range(player.getYPos() - (player.getHeight() // 2), player.getYPos()) or
                player.getYPos() in range(self.getYPos() - (self.getHeight() // 2), self.getYPos())):
            # Left side of enemy with right side of player + range of attack
            # Right side of enemy with left side of player
            if (self.getXPos() in range(player.getXPos(), player.getXPos() + player.getWidth() + currentAttack.getRange()) or
                    self.getXPos() in range(player.getXPos() - currentAttack.getRange() - self.getWidth(), player.getXPos())):

                # Find is false so no attack but is within range of player so must block
                if self.__find == False:
                    if playerPrevAttack.getAttackPoint() != BlockState().NONE:  # Should always be True
                        # Will always execute for current attacks
                        self.setBlock(playerPrevAttack.getAttackPoint())
                    return  # No attack if find is false so return

                if self.__attackTimer > 5:  # To ensure attacks dont occur too frequently
                    if self.getIsAttacking() == False:
                        self.toggleAttack()  # Set attacking to true
                    print(self.__attackTimer)
                    self.__selectAttackAnimationState()  # Start animation execution
                    self.__attackTimer = 0  # Reset timer

        if self.getIsAttacking() == True:  # Here this ensures that animation changes wont stop the attack
            if self._getAnimManager().getCounter() == currentAttack.getTriggerIndex():
                if player.getBlock() != currentAttack.getAttackPoint():  # Checks if attack is blocked
                    player.decrementHealth(currentAttack.getHealthCost())
                # To keep track of player health
                print("Player health: ", player.getHealth())
                self.toggleAttack()  # Sets 'isAttacking' back to False
                # Resets animation after attack is complete
                self.setAnimState(AnimationState().IDLE)
            self.__attackTimer = 0  # Keeps timer at 0 while animation is being executed


"""
    enemyAttacks = [
        Attack(20, 10, blockState.MIDDLE, 0),  # Basic attack
        Attack(20, 10, blockState.TOP, 0),  # Top attack
        Attack(20, 10, blockState.BOTTOM, 0),  # Bottom attack
        Attack(30, 5, blockState.MIDDLE, 0),  # Long range lower damage
        Attack(15, 15, blockState.MIDDLE, 0),  # Short range higher damage
    ]
"""
