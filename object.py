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

    def translate(self, vec: Vector) -> None:
        self.__xPos += vec.getX()
        self.__yPos += vec.getY()

    # This method is for when the player is to be translated by an amount that is not in vector form
    def translateCartesian(self, x, y) -> None:
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
        for i in range(len(self.__velocities)):
            totalX += self.__velocities[i].getX()
            totalY += self.__velocities[i].getY()
        self.translateCartesian(totalX, totalY)

    def getSpeed(self) -> int:
        return self.__speed

    def stopAtBounds(self, width: int, height: int) -> None:
        if self.getYPos() <= 0:
            self.addVelocity(Vector(self.__speed, -1 * 3 * pi / 2))
        elif self.getYPos() + self.getHeight() >= height:
            self.addVelocity(Vector(self.__speed, -1 * pi / 2))

        if self.getXPos() <= 0:
            self.addVelocity(Vector(self.__speed, 0))
        elif self.getXPos() + self.getWidth() >= width:
            self.addVelocity(Vector(self.__speed, pi))

    def collides(self, object: Object, deltaTime: float) -> None:
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
        """
        for i in range(self.getWidth()):
            if(self.getXPos() + i > object.getXPos() and self.getXPos() + i < object.getXPos() + object.getWidth()):
                # Top side
                if self.getYPos() < object.getXPos():
                    if self.getYPos() + self.getHeight() >= object.getYPos() and self.getYPos() <= object.getYPos() + object.getHeight():
                        self.addVelocity(
                            Vector(self.__speed * self.__speed * deltaTime, 3 * pi / 2))
                        break
        """

    # Check the positions of the platforms placed in the level
    def isStoodOnGround(self, level: list, width: int, height: int) -> bool:
        # then compare these with player positions to see if the player
        # is stood on them
        for x in range(len(level[0])):
            for y in range(len(level)):
                if level[y][x] != "0":
                    objXpos = (width // len(level[y])) * x
                    objYpos = (height // len(level)) * y
                    objWidth = (width // len(level[y]))
                    for i in range(objWidth):
                        if self.getYPos() + self.getHeight() == objYpos and self.getXPos() == objXpos + i:
                            print("@")
                            return True
        return False
