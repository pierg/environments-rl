from gym_minigrid.extendedminigrid import *
from .state_property import *

""""
    obs_parser takes agents observation and translates it to world states.
    Output is a current state visible to the agent
"""

AGENT_GRID_LOCATION = 2


class ObservationParser:

    def get_current_state(self, obs) -> dict:

        current_state = []

        # check front
        x = math.floor(AGENT_VIEW_SIZE / AGENT_GRID_LOCATION)
        y = AGENT_VIEW_SIZE - AGENT_GRID_LOCATION
        front_tile = obs.get(x, y)
        if self.check_if_clear(front_tile):
            current_state.append(StateProperty(StatePropertyEnum.front_is_clear,True))
        else:
            current_state.append(StateProperty(StatePropertyEnum.front_is_clear,False))

        if self.check_if_safe(front_tile):
            current_state.append(StateProperty(StatePropertyEnum.front_is_safe,True))
        else:
            current_state.append(StateProperty(StatePropertyEnum.front_is_safe,False))

        # check left
        x = AGENT_GRID_LOCATION
        y = AGENT_VIEW_SIZE - AGENT_GRID_LOCATION + 1
        left_tile = obs.get(x, y)
        if self.check_if_clear(left_tile):
            current_state.append(StateProperty(StatePropertyEnum.left_is_clear,True))
        else:
            current_state.append(StateProperty(StatePropertyEnum.left_is_clear,False))

        if self.check_if_safe(left_tile):
            current_state.append(StateProperty(StatePropertyEnum.left_is_safe,True))
        else:
            current_state.append(StateProperty(StatePropertyEnum.left_is_safe,False))

        # check right
        x = AGENT_GRID_LOCATION
        y = AGENT_VIEW_SIZE - AGENT_GRID_LOCATION - 1
        right_tile = obs.get(x, y)

        if self.check_if_clear(right_tile):
            current_state.append(StateProperty(StatePropertyEnum.right_is_clear,True))
        else:
            current_state.append(StateProperty(StatePropertyEnum.right_is_clear,False))

        if self.check_if_safe(right_tile):
            current_state.append(StateProperty(StatePropertyEnum.right_is_safe, True))
        else:
            current_state.append(StateProperty(StatePropertyEnum.right_is_safe, False))

        return current_state

    # needs improvement
    @staticmethod
    def check_if_clear(tile):
        if isinstance(tile, WorldObj) and isinstance(tile, Wall):
            return False
        return True

    # needs improvement
    @staticmethod
    def check_if_safe(tile):
        if isinstance(tile, WorldObj) and isinstance(tile, Hazard):
            return False
        return True
