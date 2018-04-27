from .states import State


class GoalMoveAwayFromDanger:
    
    name = "Move away form danger"
    goal_state = State()
    goal_state.front_is_clear = True
    goal_state.front_is_safe = True
    goal_state.left_is_clear = True
    goal_state.left_is_safe = True
    goal_state.right_is_clear = True
    goal_state.right_is_safe = True
