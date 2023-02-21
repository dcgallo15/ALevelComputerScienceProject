from vector import Vector
from math import atan, tan, sqrt, pi
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
        # Protected as it will be used in enemy class
        self._block: BlockState = BlockState().NONE
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

    def setBlock(self, blockState: BlockState) -> None:
        self.__block = blockState

    def resetBlock(self) -> None:
        self.__block = BlockState().NONE

    # Will perform the attack move
    # This will check if the player instance passed in will be affected by this attack
    def attack(self, player) -> None:
        # Check if an attack should be carried out
        if self.__isAttacking == True:
            # Assigns the current attack
            currentAttack: Attack = self.__attacks[self.__currentAttackIndex]
            if self.__block == currentAttack.getAttackPoint():
                print("ATTACK BLOCKED")
                return
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
                    else:
                        # Checks if the left side of the player is within attack range of the enemy
                        # Bug fix here that ensures range is properly calculated
                        if self.getXPos() - currentAttack.getRange() in range(player.getXPos(),
                                                                              player.getXPos() + player.getWidth()):
                            player.decrementHealth(
                                currentAttack.getHealthCost())
                    # To track changes in health
                    print(player.getHealth())
                # The attack has been carried out
                self.toggleAttack()

    def setCurrentAttackIndex(self, index: int) -> None:
        self.__currentAttackIndex = index

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
        self.__currentAnimState: AnimationState = 0
        self.__attackTimer: float = 0

    # Will control wether the enemy attempts to find the player or not
    def setFind(self, newFind: bool) -> None:
        self.__find = newFind

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

    def __selectAnimationState(self):
        state = AnimationState()
        if self.getFacingRight() == False:
            if self.__currentAnimState != state.ATTACKLEFT:
                self.setAnimState(state.ATTACKLEFT)
                self.__currentAnimState = state.ATTACKLEFT
        else:
            if self.__currentAnimState != state.ATTACKRIGHT:
                self.setAnimState(state.ATTACKRIGHT)
                self.__currentAnimState = state.ATTACKRIGHT

    def attackPlayer(self, player: Player, deltatime: float):
        self.__attackTimer += deltatime
        # Selects the attack:
        self.setCurrentAttackIndex(0)

        if self.getIsAttacking() == True:
            if self.__attackTimer > 0.5:  # Max 2 attacks per second
                self.attack(player)  # is attacking is reset here
                self.__attackTimer = 0

        else:  # Determining whether to attack
            # An attack will only be attempted when in range of player and find is true
            if self.getFacingRight() == True:
                # Left side of player and right side of enemy
                if sqrt((player.getXPos() - (self.getXPos() + self.getWidth())) ** 2) < self.getCurrentAttack().getRange() + self.getWidth():
                    if self.__find == True:
                        self.toggleAttack()
                        self.__selectAnimationState()
            else:
                # Right side of player and left side of enemy
                if sqrt(((player.getXPos() + player.getWidth()) - self.getXPos()) ** 2) < self.getCurrentAttack().getRange():
                    if self.__find == True:
                        self.toggleAttack()
                        self.__selectAnimationState()
