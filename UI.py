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
        if amountToBeRendered > len(self.__objList):
            amountToBeRendered = len(self.__objList)
        for i in range(int(amountToBeRendered)):
            obj = self.__objList[i]
            pygame.draw.rect(screen, obj.getColor(),
                             pygame.Rect(obj.getXPos(), obj.getYPos(), obj.getWidth(), obj.getHeight()))


# will be rendered when attached to the screen since it inhertis from object
class pygameButton(Object):
    def __init__(self, width: int, height: int, xPos: int, yPos: int, color: tuple) -> None:
        super().__init__(width, height, xPos, yPos, color)

    # Returns true if mouse position within bounds of the button
    # Retuns False if the mouse position out of bounds of the button
    def isClicked(self, mouseX: int, mouseY: int) -> bool:
        if mouseX in range(self.getXPos(), self.getXPos() + self.getWidth()) and mouseY in range(self.getYPos(), self.getYPos() + self.getHeight()):
            return True
        return False
