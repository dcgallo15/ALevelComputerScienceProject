from animation import AnimationState


class Attack():
    def __init__(self, range: int, healthCost: int, triggerIndex: int) -> None:
        # This state will be defined in the animation state class
        # There will be a list then created in the animation manager
        # This will then be initialised using different images of the attack
        self.__range: int = range
        self.__healthCost: int = healthCost
        # The point in the animation list where the attack triggers
        self.__triggerIndex: int = triggerIndex

    def getRange(self) -> int:
        return self.__range

    def getHealthCost(self) -> int:
        return self.__healthCost

    def getTriggerIndex(self) -> int:
        return self.__triggerIndex
