import pygame
from object import Object


class Screen():
    # Contructor:
    def __init__(self, w: int, h: int, attachedObjects: list = []) -> None:
        # Member variable initialisation
        self.__w = w
        self.__h = h
        self.__objects = attachedObjects
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

        # This will clear the screen (by default to black)
    def clear(self, color: tuple = (0, 0, 0)) -> None:
        self.__screen.fill(color)
