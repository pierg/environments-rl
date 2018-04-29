from gym_minigrid.extendedminigrid import ExMiniGridEnv
from .state_property import *

class Action:

    def __init__(self, name):
        self.name = name
        self.preconditions = []
        self.effects = []
        self.cost = 1

        if name == "front":
            self.preconditions.append(StateProperty(StatePropertyEnum.front_is_clear,True))
            self.preconditions.append(StateProperty(StatePropertyEnum.front_is_safe, True))

        if name == "left":
            self.preconditions.append(StateProperty(StatePropertyEnum.left_is_clear, True))
            self.preconditions.append(StateProperty(StatePropertyEnum.left_is_safe, True))

            self.effects = Action(ExMiniGridEnv.Actions.forward).preconditions

        if name == "right":
            self.preconditions.append(StateProperty(StatePropertyEnum.right_is_clear, True))
            self.preconditions.append(StateProperty(StatePropertyEnum.right_is_safe, True))

            self.effects = Action(ExMiniGridEnv.Actions.forward).preconditions

    @staticmethod
    def getAllPossibleActions() -> list:
        action_list = []
        for action in ExMiniGridEnv.Actions:
            action_list.append(Action(action))
        return action_list

    @staticmethod
    def getStateAfterAction(state_original, action) -> list:
        state_changed = list(state_original)
        for state_property in state_changed:
            for effect_property in action.effects:
                if(state_property.property == effect_property.property):
                    state_property.value = effect_property.value


    @staticmethod
    def availableActions(state : list) ->  list:
        allActions = Action.getAllPossibleActions()
        availableActions = []
        for action in allActions:
            preconditions_total = len(action.preconditions)
            preconditions_met = 0
            for precondition in action.preconditions:
                for property in state:
                    if precondition.property == property.property:
                        if precondition.value == property.value:
                            preconditions_met = preconditions_met + 1
            if preconditions_met == preconditions_total:
                return availableActions

        return []

