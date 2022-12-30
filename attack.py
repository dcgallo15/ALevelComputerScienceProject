from animation import AnimationState


class Attack():
    def __init__(self, state: AnimationState, range: int, healthCost: int) -> None:
        # This state will be defined in the animation state class
        # There will be a list then created in the animation manager
        # This will then be initialised using different images of the attack
        self.__state: AnimationState = state
        self.__range: int = range
        self.__healthCost: int = healthCost

    def getAnimation(self) -> AnimationState:
        return self.__state

    def getRange(self) -> int:
        return self.__range

    def getHealthCost(self) -> int:
        return self.__healthCost
