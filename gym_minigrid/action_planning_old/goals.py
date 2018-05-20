from .state_property import *
""""
    This file contains goals for action_planner
    Goal defines states, which need to be fulfilled
"""

move_away_from_danger = [
    StateProperty(StatePropertyEnum.front_is_safe, True),
    StateProperty(StatePropertyEnum.front_is_clear, True)
]

