from math import cos, sin


class Vector():
    # NOTE: direction is in radians
    def __init__(self, magnitude: float, direction: float) -> None:
        self.__mod = magnitude  # mod is the modulus of the vector
        self.__direction = direction  # this direction that the vector is pointing

    # Will return the X component of the vector
    def getX(self) -> float:
        return self.__mod * cos(self.__direction)

    # Will return the Y component of the vector
    def getY(self) -> float:
        return self.__mod * sin(self.__direction)

    def setMagnitude(self, magnitude: float) -> None:
        self.__mod = magnitude

    def setDirection(self, direction: float) -> None:
        self.__direction = direction

    def __repr__(self):
        return str(self.__mod) + " * " + str(self.__direction)
