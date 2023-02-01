# This small class will make the code more readable
class AnimationState():
    def __init__(self) -> None:
        self.IDLE = 0
        self.RUNNINGLEFT = 2
        self.RUNNINGRIGHT = 3
        self.ATTACKLEFT = 4
        self.ATTACKRIGHT = 5


class AnimationManager():
    def __init__(self) -> None:
        self.__state = AnimationState()
        self.__currentState: list = []
        self.__counter: int = 0
        # Lists of the different animations
        self.__idle = []
        self.__runningLeft = []
        self.__runningRight = []
        self.__attackLeft = []
        self.__attackRight = []

    # This method is used to initialise the different animations
    def setupStates(self, animState: int, animations: list):
        if animState == self.__state.IDLE:
            for anim in animations:
                self.__idle.append(anim)

        elif animState == self.__state.RUNNINGLEFT:
            for anim in animations:
                self.__runningLeft.append(anim)

        elif animState == self.__state.RUNNINGRIGHT:
            for anim in animations:
                self.__runningRight.append(anim)

        elif animState == self.__state.ATTACKLEFT:
            for anim in animations:
                self.__attackLeft.append(anim)

        elif animState == self.__state.ATTACKRIGHT:
            for anim in animations:
                self.__attackRight.append(anim)

        else:
            print("UNRECOGNISED ANIMATION STATE")

    # Choses which animation the object will take
    def setAnimation(self, animState: int) -> None:
        if animState == self.__state.IDLE:
            self.__currentState = self.__idle

        elif animState == self.__state.RUNNINGLEFT:
            self.__currentState = self.__runningLeft

        elif animState == self.__state.RUNNINGRIGHT:
            self.__currentState = self.__runningRight

        elif animState == self.__state.ATTACKLEFT:
            self.__currentState = self.__attackLeft

        elif animState == self.__state.ATTACKRIGHT:
            self.__currentState = self.__attackRight

        else:
            print("UNRECOGNISED ANIMATION STATE")

        # Resets the counter when the state is changed
        # So the new animation will start from the start of the list
        self.__counter = 0

    # Cycle to the next animation state
    def changeState(self) -> None:
        self.__counter = self.__counter + 1
        # Ensures that the counter will iterate through the list
        if self.__counter == (len(self.__currentState)):
            self.__counter = 0

    # This will return a pygame image object
    def getCurrentAnimation(self):
        return self.__currentState[self.__counter]

    def getCounter(self) -> int:
        return self.__counter
