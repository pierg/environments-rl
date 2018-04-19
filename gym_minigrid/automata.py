from transitions import State

from fake_obshelper import ObsHelper as oh

from safetystatemachine import SafetyStateMachine, SafetyState


class AlwaysAvoid(SafetyStateMachine):

    states = [
        {'name': 'initial',
         'type': 'inf_ctrl'},

        {'name': 'safe',
         'type': 'inf_ctrl'},

        {'name': 'near',
         'type': 'sys_fin_ctrl'},

        {'name': 'immediate',
         'type': 'sys_urg_ctrl'},

        {'name': 'fail',
         'type': 'violated',
         'on_enter': 'on_violated'}
    ]

    transitions = [
        {'trigger': '*',
         'source': 'initial',
         'dest': '*'},

        {'trigger': '*',
         'source': 'safe',
         'dest': '=',
         'unless': 'obs_near'},

        {'trigger': '*',
         'source': 'safe',
         'dest': 'near',
         'conditions': 'obs_near'},

        {'trigger': '*',
         'source': 'near',
         'dest': 'safe',
         'unless': '[obs_near, obs_immediate]'},

        {'trigger': '*',
         'source': 'near',
         'dest': '=',
         'conditions': 'obs_near',
         'unless': 'obs_immediate'},

        {'trigger': '*',
         'source': 'near',
         'dest': 'immediate',
         'conditions': 'obs_immediate'},

        {'trigger': '*',
         'source': 'immediate',
         'dest': 'near',
         'conditions': 'obs_near',
         'unless': 'obs_immediate'},

        {'trigger': '*',
         'source': 'immediate',
         'dest': '=',
         'conditions': 'obs_immediate'},

        {'trigger': '*',
         'source': 'immediate',
         'dest': 'fail',
         'conditions': 'forward'}
    ]

    def __init__(self, name, worldobj_avoid, notify):
        self.worldobj_avoid = worldobj_avoid
        # Initializing the SafetyStateMachine
        super().__init__(name, self.states, self.transitions, 'initial', notify)

    def _obs_to_state(self, obs):
        near = oh.is_near_to_worldobj(obs, self.worldobj_avoid)
        immediate = oh.is_immediate_to_worldobj(obs, self.worldobj_avoid)
        if immediate:
            return 'immediate'
        elif near and not immediate:
            return 'near'
        else:
            return'safe'

    def obs_near(self):
        return oh.is_near_to_worldobj(self.observations_pre, self.worldobj_avoid)

    def obs_immediate(self):
        return oh.is_immediate_to_worldobj(self.observations_pre, self.worldobj_avoid)



class AvoidWater(SafetyStateMachine):
    """ The agent should never step into the water """

    states = [
        {'name': 'initial',
         'type': 'inf_ctrl'},

        {'name': 'safe',
         'type': 'inf_ctrl'},

        {'name': 'near_water',
         'type': 'inf_ctrl'},

        {'name': 'facing_water',
         'type': 'inf_ctrl'},

        {'name': 'drowning',
         'type': 'violated'},
    ]

    transitions = [

        {'trigger': '*',
         'source': 'initial',
         'dest': '*'},

        {'trigger': '*',
         'source': 'safe',
         'dest': '='},

        {'trigger': '*',
         'source': 'near_water',
         'dest': '='},

        {'trigger': '*',
         'source': 'safe',
         'dest': 'near_water'},

        {'trigger': '*',
         'source': 'near_water',
         'dest': 'safe'},

        {'trigger': '*',
         'source': 'near_water',
         'dest': 'facing_water'},

        {'trigger': '*',
         'source': 'facing_water',
         'dest': 'near_water'},

        {'trigger': '*',
         'conditions': 'forward',
         'source': 'facing_water',
         'dest': 'drowning'}
    ]

    # Convert the observations stored in self.current_obs in a state a saves the state in current_state
    def _obs_to_state(self, obs):
        if oh.is_near_water(obs):
            return 'near_water'
        elif oh.is_facing_water(obs):
            return 'facing_water'
        elif oh.is_inside_water(obs):
            return 'drowning'
        else:
            return'safe'


    def __init__(self, name, notify):
        # Initializing the SafetyStateMachine
        super().__init__(name, AvoidWater.states, AvoidWater.transitions, 'initial', notify)

    def set_unsafe_actions(self, action):
        # RETURN THE UNSAFE ACTIONS TO BE AVOIDED
        self.unsafe_actions.append(action)
        # RAISE VIOLATION
        self._on_violated()


    """ Conditions """
    def is_water_approaching(self, action):
        return oh.is_water_approaching(self.obs_curr)




class AvoidDark(SafetyStateMachine):
    """ The agent should not enter a room without first turning the lights on """

    states = [

        {'name': 'safe',
         'type': 'inf_ctrl'},

        {'name': 'door_ahead',
         'type': 'sys_fin_ctrl',
         'children': [
            {'name': 'closed',
             'type': 'sys_fin_ctrl'},

            {'name': 'open',
             'type': 'sys_fin_ctrl'},
         ]},
        {'name': 'entering_room',
         'type': 'sys_urg_ctrl',
         'children': [
             {'name': 'bright',
              'type': 'sys_fin_ctrl'},

             {'name': 'dark',
              'type': 'sys_fin_ctrl'},
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

            # The door is locked
            {'trigger': '*',
             'source': 'door_ahead',
             'dest': 'door_ahead_closed',
             'conditions': 'toggle'},

            # The door is open
            {'trigger': '*',
             'source': 'door_ahead',
             'dest': 'door_ahead_open',
             'conditions': 'toggle'},

        {'trigger': '*',
         'source': 'door_ahead_open',
         'dest': 'entering_room',
         'conditions': 'obs_entering_room'},

            # The room is bright
            {'trigger': '*',
             'source': 'entering_room',
             'dest': 'entering_room_bright',
             'conditions': 'toggle'},

            # The room is dark
            {'trigger': '*',
             'source': 'entering_room',
             'dest': 'entering_room_dark',
             'conditions': 'toggle'},

        # The room is bright
        {'trigger': '*',
         'source': 'entering_room',
         'dest': 'safe',
         'conditions': '[forward, is_room_bright]'},

        # The room is dark
        {'trigger': '*',
         'source': 'entering_room',
         'dest': 'block',
         'conditions': 'forward',
         'unless': 'is_room_bright'},

        {'trigger': '*',
         'source': 'block',
         'dest': 'block',
         'conditions': ''},

    ]

    # Convert the observations stored in self.current_obs in a state a saves the state in current_state
    def _obs_to_state(self, obs):
        self.curret_state = ''

    def __init__(self, name, notify):
        # Initializing the SafetyStateMachine
        super().__init__(name, AvoidDark.states, AvoidDark.transitions, 'safe', notify)

    def set_unsafe_actions(self, action):
        # RETURN THE UNSAFE ACTIONS TO BE AVOIDED
        self.unsafe_actions.append(self.actions.forward)
        # RAISE VIOLATION
        self._on_violated()


    """ Conditions """
    def is_light_on(self, action):
        return oh.is_light_on(self.obs_curr)

    def is_door_closed_ahead(self, action):
        return oh.is_door_closed_ahead(self.obs_curr)

    def is_empty_ahead(self, action):
        return oh.is_empty_ahead(self.obs_curr)




# Example with hierarchical state machines
class AvoidDarkChildren(SafetyStateMachine):
    """ The agent should not enter a room without first turning the lights on """

    states = [

        {'name': 'safe',
         'type': 'inf_ctrl'},

        {'name': 'door_ahead',
         'type': 'sys_fin_ctrl'},

        {'name': 'room_ahead',
         'type': 'sys_urg_ctrl',
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

        # The door is locked
        {'trigger': '*',
         'source': 'door_ahead',
         'dest': 'door_ahead',
         'conditions': 'toggle'},

        # The door opens
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

    # Convert the observations stored in self.current_obs in a state a saves the state in current_state
    def _obs_to_state(self, obs):
        self.curret_state = ''

    def __init__(self, name, notify):
        # Initializing the SafetyStateMachine
        super().__init__(name, self.states, self.transitions, 'safe', notify)

    def set_unsafe_actions(self, action):
        # RETURN THE UNSAFE ACTIONS TO BE AVOIDED
        self.unsafe_actions.append(self.actions.forward)
        # RAISE VIOLATION
        self._on_violated()


    """ Conditions """
    def is_light_on(self, action):
        return oh.is_light_on(self.obs_curr)

    def is_door_closed_ahead(self, action):
        return oh.is_door_closed_ahead(self.obs_curr)

    def is_empty_ahead(self, action):
        return oh.is_empty_ahead(self.obs_curr)



class TestStateTypes(SafetyStateMachine):
    """ Testing """

    states = [

        {'name': 'initial',
         'type': 'inf_ctrl'},

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

    # Convert the observations stored in self.current_obs in a state a saves the state in current_state
    def _obs_to_state(self, obs):
        self.curret_state = ''

    def __init__(self, name, notify):
        # Initializing the SafetyStateMachine
        super().__init__(name, self.states, self.transitions, 'initial', notify)

