import pygame
from object import Object


# NOTE: UI objects must have render methods as they will not be attached to the screen
class horizontalBar():
    def __init__(self, width: int, height: int, xPos: int, yPos: int, color: tuple, amountOfObj: int = 10) -> None:
        self.__percent = 100
        self.__objList = []
        for i in range(amountOfObj):
            self.__objList.append(Object(
                width // amountOfObj, height, xPos + (i*(width // amountOfObj)), yPos, color))

    # Must be from 0 -> 100
    def setPercent(self, percent: int) -> None:
        self.__percent = percent

    # NOTE: this must ba called before 'screen.render()'
    def render(self, screen) -> None:
        amountToBeRendered = len(self.__objList) * (self.__percent / 100)
        for i in range(int(amountToBeRendered)):
            obj = self.__objList[i]
            pygame.draw.rect(screen, obj.getColor(),
                             pygame.Rect(obj.getXPos(), obj.getYPos(), obj.getWidth(), obj.getHeight()))
