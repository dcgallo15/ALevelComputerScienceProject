import pygame
from object import Object, Player, Enemy
from vector import Vector
from math import pi


class Screen():
    # Constructor:
    def __init__(self, w: int, h: int, attachedObjects: list = []) -> None:
        # Member variable initialisation
        self.__w = w
        self.__h = h
        self.__objects = attachedObjects
        self.__backgroundColor = (0, 0, 0)
        # Initialises the pygame screen
        self.__screen = pygame.display.set_mode((w, h))

    def getHeight(self) -> int:
        return self.__h

    def getWidth(self) -> int:
        return self.__w

    # So that UI elements can be rendered seperatly
    def getPygameScreen(self):
        return self.__screen

    def attachObject(self, newObject: Object) -> None:
        self.__objects.append(newObject)

    def removeObject(self, objToRemove: Object) -> None:
        self.__objects.remove(objToRemove)

    # Clears the object list
    def resetObjects(self) -> None:
        self.__object = []

    # This will render all of the objects attached
    def render(self) -> None:
        for i in range(len(self.__objects)):
            obj: Object = self.__objects[i]
            # CHecks if there is a player object so that it will render the sprite differently
            if isinstance(obj, Player) == True:
                self.__screen.blit(
                    obj.getSprite(), (obj.getXPos(), obj.getYPos()))
            else:
                # creates a pygame rect object then draws it to the correct position on the screen
                pygame.draw.rect(self.__screen, obj.getColor(), pygame.Rect(
                    obj.getXPos(), obj.getYPos(), obj.getWidth(), obj.getHeight()))
        pygame.display.flip()
        pygame.display.update()

    def clear(self) -> None:
        pygame.display.fill((0, 0, 0))
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

    # This takes a list of strings and then converts it into objects
    # It doesn't generate an object when the colour of the square is
    # the same as the background color of the screen
    def parseLevel(self, level: list) -> None:
        # Loops through each element of the string
        # The through each chracter in each string
        for x in range(len(level[0])):
            for y in range(len(level)):
                # This make it proportional to the screen size
                objWidth = self.__w // len(level[0])
                objHeight = self.__h // len(level)
                color: tuple = self._mapColors(int(level[y][x]))
                # Checks if the color is the same as the background color
                if color != self.__backgroundColor:
                    # Generates and object and the correct positions
                    self.__objects.append(
                        Object(objWidth, objHeight, x * objWidth,
                               y * objHeight, color, True))

    # For object collision handling
    def objectCollsion(self, player: Player) -> None:
        # Starts from 2 as player and enemy are first 2 objects always
        for i in range(2, len(self.__objects)):
            player.collidesObjectX(self.__objects[i])

    # This will clear the screen (by default to black)
    def clear(self) -> None:
        self.__screen.fill(self.__backgroundColor)
