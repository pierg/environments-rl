from enum import Enum

class StatePropertyEnum(Enum):
    front_is_safe = 1
    front_is_clear = 2
    right_is_safe = 3
    right_is_clear = 4
    left_is_safe = 5
    left_is_clear = 6

class StateProperty:

    def __init__(self, stateproperty_Enum : StatePropertyEnum , value : bool):
        self.property = stateproperty_Enum
        self.value = value

