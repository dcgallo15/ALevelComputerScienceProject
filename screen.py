import pygame
from object import Object


class Screen():
    # Contructor:
    def __init__(self, w: int, h: int, attachedObjects: list = []) -> None:
        # Member variable initialisation
        self.__w = w
        self.__h = h
        self.__objects = attachedObjects
        self.__backgroundColor = (0, 0, 0)
        # Initialises the pygame screen
        self.__screen = pygame.display.set_mode((w, h))

    def attachObject(self, newObject: Object) -> None:
        self.__objects.append(newObject)

    # This will render all of the objects attached
    def render(self) -> None:
        for i in range(len(self.__objects)):
            obj: Object = self.__objects[i]
            pygame.draw.rect(self.__screen, obj.getColor(), pygame.Rect(
                obj.getXPos(), obj.getYPos(), obj.getWidth(), obj.getHeight()))
        pygame.display.flip()
        pygame.display.update()

    def _mapColors(self, n: int) -> tuple:
        if n == 0:
            return (0, 0, 0)
        elif n == 1:
            return (255, 255, 255)
        elif n == 2:
            return (255, 0, 0)
        elif n == 3:
            return (0, 255, 0)
        elif n == 4:
            return (0, 0, 255)
        elif n == 5:
            return (255, 0, 0)
        elif n == 6:
            return (255, 0, 255)
        elif n == 7:
            return (0, 255, 255)
        else:
            print("SCREEN CLASS: This character cannot be parsed for")
            return (-1, -1, -1)

    def parseLevel(self, level: list):
        for x in range(len(level[0])):
            for y in range(len(level)):
                objWidth = self.__w // len(level[0])
                objHeight = self.__h // len(level)
                color: tuple = self._mapColors(int(level[y][x]))
                if color != self.__backgroundColor:
                    self.__objects.append(
                        Object(objWidth, objHeight, x * objWidth,
                               y * objHeight, color, True))

    # This will clear the screen (by default to black)
    def clear(self) -> None:
        self.__screen.fill(self.__backgroundColor)
