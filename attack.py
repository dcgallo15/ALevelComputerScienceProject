from animation import AnimationState


class BlockState():
    # There will be 3 areas that can be blocked or attacked
    def __init__(self) -> None:
        self.TOP = 3
        self.MIDDLE = 2
        self.BOTTOM = 1
        self.NONE = 0


class Attack():
    def __init__(self, range: int, healthCost: int, attackPoint: BlockState, triggerIndex: int) -> None:
        # This state will be defined in the animation state class
        # There will be a list then created in the animation manager
        # This will then be initialised using different images of the attack
        self.__range: int = range
        self.__healthCost: int = healthCost
        # The point in the animation list where the attack triggers
        self.__triggerIndex: int = triggerIndex
        self.__attackPoint: BlockState = attackPoint

    def getRange(self) -> int:
        return self.__range

    def getHealthCost(self) -> int:
        return self.__healthCost

    def getAttackPoint(self) -> int:
        return self.__attackPoint

    def getTriggerIndex(self) -> int:
        return self.__triggerIndex
