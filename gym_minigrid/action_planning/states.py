from .action import *
from typing import List, Dict
import copy
from enum import IntEnum


class StateNameEnum(IntEnum):
    north_is_safe = 1
    north_is_clear = 2
    east_is_safe = 3
    east_is_clear = 4
    west_is_safe = 5
    west_is_clear = 6
    current_is_clear = 7
    current_is_safe = 8


class WorldState:
    """
        WorldState represents the state of the world
    """
    def __init__(self, states: Dict[StateNameEnum, bool]):
        self.states: Dict[StateNameEnum, bool] = states

    def get_available_actions(self) -> Tuple[Action, ...]:
        """
        Returns all possible actions that can take place in the current state
        :return: Actions whose prerequisites match the current state
        """
        resulting_worldstate = copy.deepcopy(self.states)
        possible_actions = Action.get_possible_actions()
        available_actions: List[Action] = []
        for action in possible_actions:
            preconditions_total = len(action.preconditions)
            preconditions_met = 0
            for precondition_name, precondition_value in action.preconditions:
                for state_name, state_value in resulting_worldstate.items():
                    if precondition_name == state_name:
                        if precondition_value == state_value:
                            preconditions_met += 1
            if preconditions_met == preconditions_total:
                available_actions.append(action)

        return tuple(available_actions)

    def apply_action(self, action: Action) -> 'WorldState':
        """
        Returns a worldstate containing the current state affected by the effects of an action
        :param action: Action to be executed
        :return: WorldState after action was executed
        """
        resulting_state: Dict[StateNameEnum, bool] = copy.deepcopy(self.states)

        # First check if this worldstate has the preconditions for the action
        preconditions_met = 0
        for precondition_name, precondition_value in action.preconditions:
            if precondition_name in resulting_state and \
                    resulting_state[precondition_name] == precondition_value:
                preconditions_met += 1
            else:
                raise KeyError('Tried to apply action when preconditions where not met: ' + Action)

        # Create new worldstate containing effects of action
        for effect_name, effect_value in action.effects:
            resulting_state[effect_value] = effect_value

        return WorldState(resulting_state)

    def get_tuple(self) -> Tuple[StateNameEnum, ...]:
        """
        Returns the dict of states as a tuple, to be used when you need a hashable worldState
        :return: Tuple containing the individual states
        """
        return tuple(self.states)
