from .states import State


class Parser:

    def get_current_state(self, obs):

        current_state = State()
        current_state.front_is_clear = False
        current_state.front_is_safe = False
        current_state.left_is_clear = False
        current_state.left_is_safe = False
        current_state.right_is_clear = False
        current_state.right_is_safe = False

        return current_state
