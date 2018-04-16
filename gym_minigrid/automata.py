from transitions import State

from obshelper import ObsHelper as oh

from safetystatemachine import SafetyStateMachine, SafetyState


class AvoidWater(SafetyStateMachine):
    """ The agent should never step into the water """

    states = [
        'safe',
        'facing_water',
        {'name': 'block',
         'type': 'violated',
         'on_enter': 'set_unsafe_actions'}
    ]

    transitions = [
        {'trigger': '*',
         'source': '*',
         'dest': 'safe',
         'unless': 'is_water_approaching'},

        {'trigger': '*',
         'source': 'safe',
         'conditions': 'forward',
         'dest': 'facing_water'},

        {'trigger': '*',
         'source': 'facing_water',
         'conditions': 'forward',
         'dest': 'block'},
    ]

    def __init__(self, name, notify):
        # Initializing the SafetyStateMachine
        super().__init__(name, AvoidWater.states, AvoidWater.transitions, 'safe', notify)

    def set_unsafe_actions(self, action):
        # RETURN THE UNSAFE ACTIONS TO BE AVOIDED
        self.unsafe_actions.append(action)
        # RAISE VIOLATION
        self._on_block()


    """ Conditions """
    def is_water_approaching(self, action):
        return oh.is_water_approaching(self.obs)




class AvoidDark(SafetyStateMachine):
    """ The agent should not enter a room without first turning the lights on """

    states = [

        {'name': 'safe',
         'type': 'inf_ctrl'},

        {'name': 'door_ahead',
         'type': 'inf_ctrl'},

        {'name': 'room_ahead',
         'type': 'inf_ctrl',
         'children': [

             {'name': 'light',
              'type': 'inf_ctrl'},

             {'name': 'dark',
              'type': 'inf_ctrl'},
         ]},

        {'name': 'block',
         'type': 'violated',
         'on_enter': 'set_unsafe_actions'}
    ]

    transitions = [
        {'trigger': '*',
         'source': 'safe',
         'conditions': 'is_light_on',
         'dest': 'safe'},

        {'trigger': '*',
         'source': 'safe',
         'conditions': 'is_door_closed_ahead',
         'dest': 'door_ahead'},

        {'trigger': '*',
         'source': 'door_ahead',
         'dest': 'door_ahead',
         'conditions': 'toggle'},

        {'trigger': '*',
         'source': 'door_ahead',
         'dest': 'room_ahead',
         'conditions': 'toggle',
         'unless': '[is_empty_ahead]'},

        {'trigger': '*',
         'source': 'room_ahead',
         'dest': 'room_ahead_light',
         'conditions': 'is_light_on'},

            {'trigger': '*',
             'source': 'room_ahead',
             'dest': 'room_ahead_dark',
             'unless': 'is_light_on'},

            {'trigger': '*',
             'source': 'room_ahead_light',
             'dest': 'safe',
             'conditions': 'forward'},

        {'trigger': '*',
         'source': 'room_ahead_dark',
         'dest': 'block',
         'conditions': 'forward'},

    ]

    def __init__(self, name, notify):
        # Initializing the SafetyStateMachine
        super().__init__(name, AvoidDark.states, AvoidDark.transitions, 'safe', notify)

    def set_unsafe_actions(self, action):
        # RETURN THE UNSAFE ACTIONS TO BE AVOIDED
        self.unsafe_actions.append(self.actions.forward)
        # RAISE VIOLATION
        self._on_block()


    """ Conditions """
    def is_light_on(self, action):
        return oh.is_light_on(self.obs)

    def is_door_closed_ahead(self, action):
        return oh.is_door_closed_ahead(self.obs)

    def is_empty_ahead(self, action):
        return oh.is_empty_ahead(self.obs)



class TestStateTypes(SafetyStateMachine):
    """ Testing """

    states = [

        {'name': 'satisfied',
         'type': 'satisfied'},

        {'name': 'inf_ctrl',
         'type': 'inf_ctrl'},

        {'name': 'sys_fin_ctrl',
         'type': 'sys_fin_ctrl'},

        {'name': 'sys_urg_ctrl',
         'type': 'sys_urg_ctrl'},

        {'name': 'env_fin_ctrl',
         'type': 'env_fin_ctrl'},

        {'name': 'env_urg_ctrl',
         'type': 'env_urg_ctrl'},

        {'name': 'violated',
         'type': 'violated'}
    ]

    transitions = []

    def __init__(self, name, notify):
        # Initializing the SafetyStateMachine
        super().__init__(name, TestStateTypes.states, TestStateTypes.transitions, 'satisfied', notify)

