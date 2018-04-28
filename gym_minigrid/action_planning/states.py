""""
    dict representing all possible world states in use.
    current_state must initialize all these values
    goal_state use the same naming as reference
    preconditions and effects of actions use the same naming as reference
"""

world_states = {
    'front_is_clear': bool,
    'front_is_safe': bool,
    'right_is_clear': bool,
    'right_is_safe': bool,
    'left_is_clear': bool,
    'left_is_safe': bool
}
