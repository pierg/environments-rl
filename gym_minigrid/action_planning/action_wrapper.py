from .states import States


class ActionObject(object):
    def __init__(self, name: str, preconditions: list, effects: list, cost: int):
        self.name = name
        self.preconditions = preconditions
        self.effects = effects
        self.cost = cost


class ActionWrapper:

    # returns an ActionObject provided Actions enum value
    def action(self, actionInt: int) -> ActionObject:
        method_name = '_action_' + str(actionInt)
        method = getattr(self, method_name, lambda: "No such action: " + str(actionInt))
        return method()

    @staticmethod
    def _action_0() -> ActionObject:
        preconditions = []
        effects = []
        left = ActionObject("left", preconditions, effects, cost=1)
        return left

    @staticmethod
    def _action_1() -> ActionObject:
        preconditions = []
        effects = []
        left = ActionObject("right", preconditions, effects, cost=1)
        return left

    @staticmethod
    def _action_2() -> ActionObject:
        preconditions = [{'front_is_clear': True}, {'front_is_safe': True}]
        effects = []
        left = ActionObject("forward", preconditions, effects, cost=1)
        return left

    @staticmethod
    def _action_3() -> ActionObject:
        preconditions = []
        effects = []
        left = ActionObject("pickup", preconditions, effects, cost=1)
        return left

    @staticmethod
    def _action_4() -> ActionObject:
        preconditions = []
        effects = []
        left = ActionObject("drop", preconditions, effects, cost=1)
        return left

    @staticmethod
    def _action_5() -> ActionObject:
        preconditions = []
        effects = []
        left = ActionObject("toggle", preconditions, effects, cost=1)
        return left

    @staticmethod
    def _action_6() -> ActionObject:
        preconditions = []
        effects = []
        left = ActionObject("wait", preconditions, effects, cost=1)
        return left


a = ActionWrapper()
b = a.action(2)
print(b.preconditions)
