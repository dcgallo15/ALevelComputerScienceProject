from vector import Vector
from math import atan, sqrt, pi


class Object():
    def __init__(self, width: int, height: int, xPos: int, yPos: int, color: tuple, collision: bool = False) -> None:
        # Variable Initialisation
        self.__w = width
        self.__h = height
        self.__xPos = xPos
        self.__yPos = yPos
        self.__color = color
        self.collision = collision

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

    # If this object is printed (for testing)
    def __repr__(self) -> str:
        return ("OBJECT WIDTH: " + str(self.__w) + " OBJECT HEIGHT: " + str(self.__h))


class Player(Object):
    def __init__(self, width: int, height: int, xPos: int, yPos: int, color: tuple, velocities: list, collision: bool = False) -> None:
        # Calls object's constructor
        super().__init__(width, height, xPos, yPos, color, collision)
        self.__velocities = velocities  # List of Vector objects

    # This method will add another velocity to the end of the list
    def addVelocity(self, vel: Vector) -> None:
        self.__velocities.append(vel)

    # This method will remove the first occurence of the velocity in the velocities list
    def removeVelocity(self, vel: Vector) -> None:
        self.__velocities.remove(vel)

    def getVelocities(self) -> list:
        return self.__velocities

    def resolveVelocities(self, deltaTime: int) -> None:
        totalX = 0
        totalY = 0
        for i in range(len(self.__velocities)):
            totalX += self.__velocities[i].getX()
            totalY += self.__velocities[i].getY()
        # NOTE: only did this because python is stupid and cannot overload constructors
        mod: float = (sqrt((totalX * totalX) + (totalY * totalY))) * deltaTime
        if totalX != 0:
            direction: float = atan(totalY / totalX)
        else:  # cannot divide by 0
            direction: float = pi / 2  # vertical direction if 0 horizontal component
        self.translate(Vector(mod, direction))