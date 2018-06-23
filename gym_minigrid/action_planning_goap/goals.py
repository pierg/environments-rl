from .obs_parser import StateEnum

""""
    This file contains goals for action_planner
    Goal defines states which need to be fulfilled
"""


goal_safe_east = [
    (StateEnum.east_is_safe, True),
    (StateEnum.east_is_clear, True),
    (StateEnum.orientation_east, True)
]

goal_clear_west = [
    (StateEnum.west_is_clear, True),
    (StateEnum.orientation_south, True)
]

goal_safe_zone = [
    (StateEnum.west_is_safe, True),
    (StateEnum.east_is_safe, True),
    (StateEnum.north_is_safe, True),
    (StateEnum.south_is_safe, True)
]

goal_green_square = [
    (StateEnum.current_is_goal, True),
]

goal_turn_around = [
    (StateEnum.orientation_west, True),
    (StateEnum.orientation_north, True),
    (StateEnum.orientation_south, True),
    (StateEnum.orientation_east, True)
    ]

