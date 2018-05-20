from .states import *
""""
    This file contains goals for action_planner
    Goal defines states, which need to be fulfilled
"""

move_away_from_danger = (
    (StateNameEnum.front_is_safe, True),
    (StateNameEnum.front_is_clear, True)
)

