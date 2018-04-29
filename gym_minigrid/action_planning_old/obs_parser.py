from .states import world_states
from gym_minigrid.extendedminigrid import *

""""
    obs_parser takes agents observation and translates it to world states.
    Output is a current state visible to the agent
"""

AGENT_GRID_LOCATION = 2


class ObservationParser:

    def get_current_state(self, obs) -> dict:

        current_state = world_states

        # check front
        x = math.floor(AGENT_VIEW_SIZE / AGENT_GRID_LOCATION)
        y = AGENT_VIEW_SIZE - AGENT_GRID_LOCATION
        front_tile = obs.get(x, y)
        current_state['front_is_clear'] = self.check_if_clear(front_tile)
        current_state['front_is_safe'] = self.check_if_safe(front_tile)

        # check left
        x = AGENT_GRID_LOCATION
        y = AGENT_VIEW_SIZE - AGENT_GRID_LOCATION + 1
        left_tile = obs.get(x, y)
        current_state['left_is_clear'] = self.check_if_clear(left_tile)
        current_state['left_is_safe'] = self.check_if_safe(left_tile)

        # check right
        x = AGENT_GRID_LOCATION
        y = AGENT_VIEW_SIZE - AGENT_GRID_LOCATION - 1
        right_tile = obs.get(x, y)
        current_state['right_is_clear'] = self.check_if_clear(right_tile)
        current_state['right_is_safe'] = self.check_if_safe(right_tile)

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
