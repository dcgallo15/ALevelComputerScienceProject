from vector import Vector
from math import atan, tan, sqrt, pi


class Object():
    def __init__(self, width: int, height: int, xPos: int, yPos: int, color: tuple, collision: bool = False) -> None:
        # Variable Initialisation
        self.__w = width
        self.__h = height
        self.__xPos = xPos
        self.__yPos = yPos
        self.__color = color
        self.__collision = collision

    def getWidth(self) -> int:
        return self.__w

    def getHeight(self) -> int:
        return self.__h

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
    def __init__(self, width: int, height: int, xPos: int, yPos: int, color: tuple, velocities: list, speed: int, collision: bool = False) -> None:
        # Calls object's constructor
        super().__init__(width, height, xPos, yPos, color, collision)
        self.__speed = speed
        self.__velocities = velocities  # List of Vector objects

    # This method will add another velocity to the end of the list
    def addVelocity(self, vel: Vector) -> None:
        self.__velocities.append(vel)

    # This method will remove the first occurence of the velocity in the velocities list
    def removeVelocity(self, vel: Vector) -> None:
        self.__velocities.remove(vel)

    def resetVelocities(self) -> None:
        self.__velocities = []

    def getVelocities(self) -> list:
        return self.__velocities

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

    # TODO: finish and test
    def collides(self, object: Object, deltaTime: float) -> None:  # VERSION 2.7
        for i in range(self.getHeight()):
            if (self.getYPos() + i > object.getYPos() and self.getYPos() + i < object.getYPos() + object.getHeight()):
                # Left side
                if self.getXPos() < object.getXPos():
                    if self.getXPos() + self.getWidth() >= object.getXPos() and self.getXPos() <= object.getXPos() + object.getWidth():
                        self.addVelocity(
                            Vector(deltaTime * self.__speed * self.__speed, pi))
                        break  # so the velocity is not applied multiple times
                # Right side
                if self.getXPos() > object.getXPos():
                    if self.getXPos() >= object.getXPos() and self.getXPos() <= object.getXPos() + object.getWidth():
                        self.addVelocity(
                            Vector(deltaTime * self.__speed * self.__speed, 0))
                        break

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


# Version 3.1
class Enemy(Player):
    def __init__(self, width: int, height: int, xPos: int, yPos: int, color: tuple, velocities: list, speed: int, collision: bool = False) -> None:
        super().__init__(width, height, xPos, yPos, color, velocities, speed, collision)

    # playerPosition = (player.getXpos(), player.getYpos())
    def moveTowardsPlayer(self, playerPosition: tuple):
        # list of available positions relative to where the enemy is such as: platform positions and ground level positions
        # position of the player
        # then move the player in a direction and the enemy's speed

        # Algorithm:
        # start position
        # end position
        # incrementally moves the enemy towards the player
        startPos = (self.getXPos(), self.getYPos())
        endPos = (playerPosition[0], playerPosition[1])
        pass


if __name__ == "__main__":
    enemy = Enemy(10, 10, 0, 0, (0, 0, 0), [], 5, True)
    enemy.moveTowardsPlayer(100, 100)
