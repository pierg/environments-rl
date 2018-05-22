from .obs_parser import StateEnum

""""
    This file contains goals for action_planner
    Goal defines states, which need to be fulfilled
"""


goal_safe_east = (
    (StateEnum.east_is_safe, True),
    (StateEnum.east_is_clear, True),
    (StateEnum.current_is_clear, True),
    (StateEnum.current_is_safe, True),
    (StateEnum.orientation_east, True)
)

goal_clear_west = (
    (StateEnum.west_is_clear, True),
    (StateEnum.current_is_clear, True),
    (StateEnum.current_is_safe, True),
    (StateEnum.orientation_south, True)
)



