from gym_minigrid.extendedminigrid import ExMiniGridEnv
from .state_property import *
import copy


class Action:

    def __init__(self, name):
        self.name = name
        self.preconditions = []
        self.effects = []
        self.cost = 1

        if name == ExMiniGridEnv.Actions.forward:
            self.preconditions.append(StateProperty(StatePropertyEnum.front_is_clear,True))
            self.preconditions.append(StateProperty(StatePropertyEnum.front_is_safe, True))

        if name == ExMiniGridEnv.Actions.left:
            self.preconditions.append(StateProperty(StatePropertyEnum.left_is_clear, True))
            self.preconditions.append(StateProperty(StatePropertyEnum.left_is_safe, True))

            self.effects = Action(ExMiniGridEnv.Actions.forward).preconditions

        if name == ExMiniGridEnv.Actions.right:
            self.preconditions.append(StateProperty(StatePropertyEnum.right_is_clear, True))
            self.preconditions.append(StateProperty(StatePropertyEnum.right_is_safe, True))

            self.effects = Action(ExMiniGridEnv.Actions.forward).preconditions

    def get_as_int(self):
        return

    @staticmethod
    def get_possible_actions() -> list:
        action_list = []
        for action in ExMiniGridEnv.Actions:
            action_list.append(Action(action))
        return action_list

    @staticmethod
    def get_states_after_action(state_original, action) -> list:
        state_changed = copy.deepcopy(state_original)
        for state_property in state_changed:
            for effect_property in action.effects:
                if state_property.property == effect_property.property:
                    state_property.value = effect_property.value
        return state_changed


    @staticmethod
    def available_actions_for_state(state : list) ->  list:
        state_changed = copy.deepcopy(state)
        allActions = Action.get_possible_actions()
        availableActions = []
        for action in allActions:
            preconditions_total = len(action.preconditions)
            preconditions_met = 0
            for precondition in action.preconditions:
                for property in state_changed:
                    if precondition.property == property.property:
                        if precondition.value == property.value:
                            preconditions_met = preconditions_met + 1
            if preconditions_met == preconditions_total:
                availableActions.append(action)

                return availableActions

        return []

