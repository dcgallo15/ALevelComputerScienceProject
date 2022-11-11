import pygame


class Screen():
    # Contructor:
    def __init__(self, w: int, h: int) -> None:
        # Member variable initialisation
        self.__w = w
        self.__h = h
        # Initialises the pygame screen
        self.__screen = pygame.display.set_mode((w, h))

    # This will clear the screen (by default to black)
    def clear(self, color: tuple = (0, 0, 0)) -> None:
        self.__screen.fill(color)
        pygame.display.update()
