from transitions import State

from obshelper import ObsHelper as oh

from safetystatemachine import SafetyStateMachine


class AvoidWater(SafetyStateMachine):
    """ The agent should never step into the water """

    states = [
        'safe',
        'facing_water',
        State(name='block', on_enter=['set_unsafe_actions'])
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
        super().__init__(name, AvoidWater.states, AvoidWater.transitions, notify)

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
        'safe',
        'door_ahead',
        'room_ahead',
        State(name='block', on_enter=['set_unsafe_actions'])
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
         'dest': 'safe',
         'conditions': '[forward, is_light_on]'},

        {'trigger': '*',
         'source': 'room_ahead',
         'dest': 'block',
         'conditions': 'forward',
         'unless': 'is_light_on'},
    ]

    def __init__(self, name, notify):
        # Initializing the SafetyStateMachine
        super().__init__(name, AvoidDark.states, AvoidDark.transitions, notify)

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