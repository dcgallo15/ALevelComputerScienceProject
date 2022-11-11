class Object():
    def __init__(self, width: int, height: int, xPos: int, yPos: int, color: tuple) -> None:
        # Variable Initialisation
        self.__w = width
        self.__h = height
        self.__xPos = xPos
        self.__yPos = yPos
        self.__color = color

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

    # If this object is printed (for testing)
    def __repr__(self) -> str:
        return ("OBJECT WIDTH: " + str(self.__w) + " OBJECT HEIGHT: " + str(self.__h))
