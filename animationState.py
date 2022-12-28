# This small class will make the code more readable
class animationState():
    def __init__(self) -> None:
        self.IDLE = 0
        self.RUNNING = 1
        self.ATTACK = 2


class animationManager():
    def __init__(self) -> None:
        self.__state = animationState()
        self.__currentState: list = []
        self.__counter: int = 0
        self.__idle = []
        self.__running = []
        self.__attack = []

    def setupStates(self, animState: int, *args):
        if animState == self.__state.IDLE:
            for arg in args:
                self.__idle.append(arg)

        elif animState == self.__state.RUNNING:
            for arg in args:
                self.__running.append(arg)

        elif animState == self.__state.ATTACK:
            for arg in args:
                self.__running.append(arg)

        else:
            print("UNRECOGNISED ANIMATION STATE")

    # Choses which animation the object will take
    def setAnimation(self, animState: int) -> None:
        if animState == self.__state.IDLE:
            self.__currentState = self.__idle

        elif animState == self.__state.RUNNING:
            self.__currentState = self.__running

        elif animState == self.__state.ATTACK:
            self.__currentState = self.__attack

        else:
            print("UNRECOGNISED ANIMATION STATE")

    # Cycle to the next animation state
    def changeState(self) -> None:
        self.__counter = self.__counter + 1
        # Ensures that the counter will iterate through the list
        if self.__counter == (len(self.__currentState)):
            self.__counter = 0

    def getCurrentAnimation(self):
        return self.__currentState[self.__counter]
